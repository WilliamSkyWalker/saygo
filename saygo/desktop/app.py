"""Qt Widgets shell. Network and device operations run off the GUI thread."""
import json
from html import escape
from pathlib import Path
import sys
import threading


def main():
    # Frozen native-messaging entry runs without loading Qt or opening a window.
    flag = next((item for item in ('--native-host','--native-host-uninstall') if item in sys.argv), None)
    if flag:
        from saygo.integrations.browser_bridge import main as host_main
        sys.argv = [sys.argv[0], 'host' if flag == '--native-host' else 'uninstall', *sys.argv[sys.argv.index(flag)+1:]]
        return host_main()
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setApplicationName('Saygo Desktop')
    app.setApplicationDisplayName('Saygo Desktop')
    app.setOrganizationName('Saygo')
    window = make_window(auto_connect='--smoke-test' not in sys.argv)
    window.show()
    if '--smoke-test' in sys.argv:
        from PySide6.QtCore import QTimer
        QTimer.singleShot(300, app.quit)
    return app.exec()


def make_window(auto_connect=True):
    from PySide6.QtCore import Qt, QThread, Signal, QTimer
    from PySide6.QtGui import QPixmap, QDesktopServices
    from PySide6.QtCore import QUrl
    from PySide6.QtWidgets import (QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QFormLayout,
        QTabWidget,QLineEdit,QPushButton,QLabel,QPlainTextEdit,QCheckBox,QComboBox,
        QListWidget,QListWidgetItem,QAbstractItemView,QSplitter,QFileDialog,QInputDialog,QMessageBox,
        QDialog,QTextBrowser,QFrame,QStackedWidget,QScrollArea,QLayout)
    from saygo.desktop.model import load_settings, load_key, save_settings, VisionModel
    from saygo.desktop.runner import TaskLoop
    from saygo.runtime import interactive
    from saygo.devices import control, service
    from saygo.desktop import connections

    class Composer(QPlainTextEdit):
        submitted = Signal()

        def keyPressEvent(self, event):
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter) and not event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                self.submitted.emit()
            else:
                super().keyPressEvent(event)

    class Worker(QThread):
        result = Signal(object)
        update = Signal(object)
        failed = Signal(str)
        def __init__(self, function):
            super().__init__(); self.function = function
        def run(self):
            try:
                self.result.emit(self.function(self.update.emit))
            except Exception as exc:
                self.failed.emit(str(exc))

    class Window(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle('Saygo'); self.resize(1220,840); self.setMinimumSize(900,640)
            self.worker = None; self.task_id = None; self.task_state = None
            self.pause_event = threading.Event(); self.stop_event = threading.Event()
            self.buttons = []; self.dialogs = {}; self.last_transcript = ''
            self.model_job = None; self.saved_model = None
            self.connection_worker = None; self.computer_ready = False; self.browser_ready = False
            self.disabled_auto = set(); self.browser_pages = []; self.task_minimized = False
            shell=QWidget(); self.setCentralWidget(shell)
            body=QHBoxLayout(shell); body.setContentsMargins(0,0,0,0); body.setSpacing(0)
            self.sidebar=QFrame(); self.sidebar.setObjectName('sidebar'); self.sidebar.setFixedWidth(224)
            self.side=QVBoxLayout(self.sidebar); self.side.setContentsMargins(18,24,18,18); self.side.setSpacing(12)
            brand=QLabel('saygo'); brand.setObjectName('brand'); self.side.addWidget(brand)
            self.button('＋  新任务',self.new_chat,self.side).setObjectName('primary')
            section=QLabel('最近任务'); section.setObjectName('muted'); self.side.addWidget(section)
            self.tasks=QListWidget(); self.tasks.setObjectName('history'); self.side.addWidget(self.tasks,1)
            self.tasks.itemClicked.connect(lambda item:self.load_task())
            self.model_summary=QLabel('尚未配置模型'); self.model_summary.setWordWrap(True); self.model_summary.setObjectName('muted'); self.side.addWidget(self.model_summary)
            self.button('设备与连接',lambda:self.dialogs['设备连接'].show(),self.side)
            self.button('模型设置',lambda:self.dialogs['模型设置'].show(),self.side)
            body.addWidget(self.sidebar)
            self.chat=QWidget(); body.addWidget(self.chat,1)
            self.settings_page(); self.devices_page(); self.task_page()
            from saygo.desktop.theme import STYLESHEET
            self.setStyleSheet(STYLESHEET)
            try:
                data = load_settings(); self.base.setText(data['base_url']); self.model.setText(data['model'])
                self.remember.setChecked(data.get('remember',False)); self.key.setText(load_key(data))
                self.saved_model=self.model_snapshot()
                self.model_feedback.setText('已加载配置。可以测试连接，确认当前服务可用。' if data.get('model') else '填写服务地址、模型和 API Token，开始配置。')
            except Exception as exc:
                self.statusBar().showMessage(str(exc)); self.model_feedback.setText(str(exc))
            self.update_model_summary()
            self.refresh_sessions(); self.refresh_tasks()
            self.connection_timer = QTimer(self); self.connection_timer.setInterval(5000)
            self.connection_timer.timeout.connect(self.poll_connections)
            if auto_connect:
                self.connection_timer.start(); QTimer.singleShot(0, self.poll_connections)

        def page(self, name, heading, description):
            dialog=QDialog(self); dialog.setWindowTitle(name); dialog.resize(820,560)
            self.dialogs[name]=dialog
            layout=QVBoxLayout(dialog); layout.setContentsMargins(24,24,24,24); layout.setSpacing(18)
            title=QLabel(heading); title.setObjectName('title'); layout.addWidget(title)
            subtitle=QLabel(description); subtitle.setWordWrap(True); layout.addWidget(subtitle)
            return layout

        def button(self, text, callback, layout):
            button=QPushButton(text); button.clicked.connect(lambda checked=False: callback())
            layout.addWidget(button); self.buttons.append(button); return button

        def settings_page(self):
            layout=self.page('模型设置','连接你的模型','填写支持图像输入的 OpenAI 兼容接口。任务截图会发送到这个服务。')
            form=QFormLayout(); form.setSpacing(16); layout.addLayout(form)
            self.base=QLineEdit(); self.base.setPlaceholderText('https://api.example.com/v1')
            self.model=QLineEdit(); self.model.setPlaceholderText('填写服务商提供的视觉模型 ID')
            self.key=QLineEdit(); self.key.setEchoMode(QLineEdit.EchoMode.Password)
            self.key.setPlaceholderText('粘贴 API Token / API Key'); self.key.setAccessibleName('API Token')
            token_row=QHBoxLayout(); token_row.addWidget(self.key,1)
            self.reveal_key=QPushButton('显示'); self.reveal_key.setCheckable(True)
            self.reveal_key.toggled.connect(self.toggle_key); token_row.addWidget(self.reveal_key)
            self.remember=QCheckBox('安全保存 Token，下次启动自动加载')
            form.addRow('服务地址',self.base); form.addRow('模型名称',self.model)
            form.addRow('API Token',token_row); form.addRow('',self.remember)
            help_text=QLabel('服务地址通常以 /v1 结尾，无需填写 /chat/completions。\n不勾选安全保存时，Token 仅保留在本次运行内存中。')
            help_text.setObjectName('muted'); help_text.setWordWrap(True); layout.addWidget(help_text)
            self.model_feedback=QLabel('填写配置后，可以发送一张测试图片检查连接。')
            self.model_feedback.setObjectName('feedback'); self.model_feedback.setWordWrap(True); layout.addWidget(self.model_feedback)
            row=QHBoxLayout(); layout.addLayout(row)
            self.button('保存配置',self.save_model,row).setObjectName('primary')
            self.button('测试图像连接',self.test_model,row)
            self.button('删除已保存的 Token',self.delete_key,row)
            note=QLabel('连接测试会发送一张生成的测试图片，可能产生少量模型费用。')
            note.setObjectName('muted'); note.setWordWrap(True); layout.addWidget(note); layout.addStretch()
            self.model_fields=(self.base,self.model,self.key,self.remember,self.reveal_key)
            for field in (self.base,self.model,self.key):field.textChanged.connect(self.model_edited)
            self.remember.toggled.connect(self.model_edited)
            self.dialogs['模型设置'].finished.connect(lambda _:self.reveal_key.setChecked(False))

        def toggle_key(self, visible):
            self.key.setEchoMode(QLineEdit.EchoMode.Normal if visible else QLineEdit.EchoMode.Password)
            self.reveal_key.setText('隐藏' if visible else '显示')

        def model_values(self):
            return {'base_url':self.base.text().strip(),'model':self.model.text().strip()}, self.key.text().strip()

        def model_snapshot(self):
            settings,key=self.model_values()
            return (settings['base_url'],settings['model'],key,self.remember.isChecked())

        def update_model_summary(self):
            name=self.model.text().strip()
            self.model_summary.setText('当前模型 · '+name if name else '尚未配置模型')
            self.model_summary.setToolTip(name)

        def model_edited(self, *_):
            self.update_model_summary()
            self.model_feedback.setText('配置已修改，尚未保存或测试。' if self.model_snapshot()!=self.saved_model else '与已保存配置一致；连接状态尚未验证。')

        def checked_model_values(self):
            from saygo.desktop.model import validate
            try:
                settings,key=self.model_values(); settings=validate(settings)
                if not key:raise ValueError('请填写 API Token。')
                if any(char.isspace() for char in key):raise ValueError('Token 中包含空白字符，请重新粘贴完整 Token。')
                return settings,key
            except ValueError as exc:
                self.model_feedback.setText(str(exc)); self.dialogs['模型设置'].show()
                return None

        def save_model(self):
            if self.worker or self.connection_worker:return
            values=self.checked_model_values()
            if values is None:return
            settings,key=values; remember=self.remember.isChecked()
            self.model_job='save'; self.model_feedback.setText('正在保存配置…')
            message='配置已保存；Token 已保存到系统密钥存储。' if remember else '配置已保存；Token 仅在本次运行中使用。'
            self.job(lambda emit: (save_settings(settings,key,remember), {'message':message,'model_operation':'save'})[1])

        def test_model(self):
            if self.worker or self.connection_worker:return
            values=self.checked_model_values()
            if values is None:return
            settings,key=values; self.model_job='test'; self.model_feedback.setText('正在发送测试图片，请稍候…')
            self.job(lambda emit: {**VisionModel(settings,key).test(),'model_operation':'test'})

        def delete_key(self):
            if self.worker or self.connection_worker:return
            from saygo.desktop.model import secure_backend, credential_id, validate
            settings,key=self.model_values()
            try:settings=validate(settings)
            except ValueError as exc:
                self.model_feedback.setText(str(exc)); return
            def remove(emit):
                backend=secure_backend(); ident=credential_id(settings)
                if backend.get_password('Saygo Desktop',ident): backend.delete_password('Saygo Desktop',ident)
                save_settings(settings,'',False)
                return {'message':'当前服务的 Token 已从系统存储和输入框中删除。','model_operation':'delete'}
            self.model_job='delete'; self.model_feedback.setText('正在删除当前服务的 Token…'); self.job(remove)

        def devices_page(self):
            layout=self.page('设备连接','这台电脑与浏览器','本机自动连接。Saygo 会根据任务选择应用和操作方式；浏览器连接后自动加入可用目标。')
            self.computer_status=QLabel('本机电脑 · 正在检测…'); self.computer_status.setWordWrap(True); layout.addWidget(self.computer_status)
            self.button('重新检测本机',lambda:self.poll_connections(retry_computer=True),layout)
            self.browser_status=QLabel('Chrome 浏览器 · 尚未连接'); self.browser_status.setWordWrap(True); layout.addWidget(self.browser_status)
            self.button('连接 Chrome / 安装扩展',self.install_bridge,layout).setObjectName('primary')
            help_text=QLabel('首次连接会打开 Chrome 插件安装页。安装后打开 Saygo Browser 扩展，点击 Connect local bridge；连接状态会自动更新。')
            help_text.setWordWrap(True); help_text.setObjectName('muted'); layout.addWidget(help_text)
            self.advanced=QWidget(); advanced_layout=QVBoxLayout(self.advanced)
            self.button('高级连接：指定窗口或其他设备',lambda:self.advanced.setVisible(not self.advanced.isVisible()),layout)
            layout.addWidget(self.advanced); self.advanced.hide()
            form=QFormLayout(); advanced_layout.addLayout(form)
            self.platform=QComboBox(); self.platform.addItems(['desktop','android','ios','browser'])
            self.session=QLineEdit('custom-target'); self.target=QLineEdit(); self.target.setPlaceholderText('窗口标题、App 名或设备 ID')
            self.page_id=QComboBox(); self.page_id.addItem('自动连接的浏览器无需在此配置',None)
            self.background=QCheckBox('后台窗口模式（不支持的动作会报错）')
            form.addRow('平台',self.platform); form.addRow('会话名称',self.session); form.addRow('目标',self.target); form.addRow('网页',self.page_id); form.addRow('',self.background)
            row=QHBoxLayout(); advanced_layout.addLayout(row)
            self.button('扫描设备 / 窗口',lambda:self.job(lambda emit:control.discover('all')),row)
            self.button('连接',self.connect_device,row)
            self.device_output=QPlainTextEdit(); self.device_output.setReadOnly(True); advanced_layout.addWidget(self.device_output)
            layout.addStretch()

        def poll_connections(self, retry_computer=False):
            if self.worker or self.connection_worker:return
            if self.task_state and self.task_state['status'] not in ('succeeded','cancelled','failed'):return
            need_computer=retry_computer or not self.computer_ready
            def poll(emit):
                result={}
                if need_computer:
                    try:
                        value=connections.connect_computer()
                        result['computer_ready']=bool(value.get('connected'))
                        result['computer_message']='本机电脑 · 已连接，可操作整个桌面' if value.get('connected') else value.get('instructions','本机电脑 · 等待连接')
                    except Exception as exc:
                        result.update(computer_ready=False,computer_message='本机电脑 · '+str(exc))
                status=connections.browser_status()
                result['browser_ready']=False
                result['browser_message']=status.get('message','')
                result['pages']=status.get('pages',[])
                if status.get('connected'):
                    try:
                        value=connections.connect_browser(status)
                        result['browser_ready']=bool(value.get('connected') and value.get('page_id'))
                        result['browser_message']='已连接 · '+str(len(status['pages']))+' 个网页，Saygo 可自行切换' if result['browser_ready'] else '扩展已连接 · 请在 Chrome 打开一个网页'
                    except Exception as exc:
                        result['browser_message']='已检测到扩展 · '+str(exc)
                return result
            self.start_connection_job(poll)

        def start_connection_job(self, function):
            if self.worker or self.connection_worker:return
            self.connection_worker=Worker(function)
            self.connection_worker.result.connect(self.connection_result)
            self.connection_worker.failed.connect(lambda message:self.browser_status.setText('Chrome 浏览器 · '+message))
            self.connection_worker.finished.connect(self.connection_done)
            self.send_button.setEnabled(False)
            self.connection_worker.start()

        def connection_result(self, result):
            if 'computer_ready' in result:
                self.computer_ready=result['computer_ready']; self.computer_status.setText(result['computer_message'])
            if 'browser_ready' in result:
                self.browser_ready=result['browser_ready']; self.browser_pages=result.get('pages',[])
                self.browser_status.setText('Chrome 浏览器 · '+result['browser_message'])
            if 'message' in result:self.browser_status.setText(result['message'])
            self.refresh_sessions()

        def connection_done(self):
            worker=self.connection_worker; self.connection_worker=None; worker.deleteLater()
            self.send_button.setEnabled(True)

        def connect_device(self):
            from argparse import Namespace
            kind=self.platform.currentText(); target=self.target.text().strip()
            args=Namespace(platform=kind,session=self.session.text().strip(),app=target or None,
                device=target or None,server_url=None,team_id=None,background=self.background.isChecked(),
                process_name=None,launch=None,new_window=False,new_window_args=[],backend='extension' if kind=='browser' else None,
                bridge_directory=None,page_id=self.page_id.currentData())
            self.job(lambda emit:control.connect(args))

        def install_bridge(self):
            if self.worker or self.connection_worker:return
            self.browser_status.setText('正在准备浏览器连接并打开 Chrome…')
            def install(emit):
                status=connections.browser_status()
                if status.get('connected'):
                    value=connections.connect_browser(status)
                    return {'browser_ready':bool(value.get('connected') and value.get('page_id')),
                            'pages':status.get('pages',[]),'browser_message':'扩展已连接'}
                return {'message':connections.install_browser()}
            self.start_connection_job(install)

        def task_page(self):
            layout=QVBoxLayout(self.chat); layout.setContentsMargins(36,28,36,18); layout.setSpacing(16)
            header=QHBoxLayout(); layout.addLayout(header)
            title=QLabel('任务空间'); title.setObjectName('title'); header.addWidget(title); header.addStretch()
            self.button('操作画面',lambda:self.preview_dialog.show(),header)
            self.button('导出对话',self.export_task,header)
            self.task_status=QLabel('新对话'); self.task_status.setObjectName('badge'); layout.addWidget(self.task_status)
            self.content=QStackedWidget(); layout.addWidget(self.content,1)
            self.timeline=QTextBrowser(); self.timeline.setOpenExternalLinks(False); self.content.addWidget(self.timeline)
            self.build_welcome()
            self.preview_dialog=QDialog(self); self.preview_dialog.setWindowTitle('最新操作画面'); self.preview_dialog.resize(860,600)
            preview_layout=QVBoxLayout(self.preview_dialog)
            self.preview=QLabel('执行任务后，这里显示最新观察画面'); self.preview.setMinimumSize(400,260)
            self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter); preview_layout.addWidget(self.preview)
            actions=QHBoxLayout(); layout.addLayout(actions)
            self.pause_button=QPushButton('暂停'); self.pause_button.clicked.connect(self.request_pause); actions.addWidget(self.pause_button)
            self.stop_button=QPushButton('停止'); self.stop_button.clicked.connect(self.request_stop); actions.addWidget(self.stop_button)
            self.resolve_button=self.button('核对操作结果',self.resolve_task,actions); actions.addStretch()
            self.button('选择操作目标',lambda:self.targets_dialog.show(),actions)
            self.targets_dialog=QDialog(self); self.targets_dialog.setWindowTitle('选择操作目标'); self.targets_dialog.resize(420,400)
            targets=QVBoxLayout(self.targets_dialog); targets.addWidget(QLabel('本机与已连接浏览器默认可用；可取消不希望本次任务操作的目标。'))
            self.sessions=QListWidget(); self.sessions.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection); targets.addWidget(self.sessions)
            self.button('设备与连接',lambda:self.dialogs['设备连接'].show(),targets)
            self.button('完成',self.targets_dialog.accept,targets)
            frame=QFrame(); frame.setObjectName('composer'); composer=QVBoxLayout(frame); composer.setContentsMargins(18,12,18,12); composer.setSpacing(8); layout.addWidget(frame)
            self.goal=Composer(); self.goal.submitted.connect(self.send_message)
            self.goal.setPlaceholderText('给 Saygo 发送任务…'); self.goal.setFixedHeight(80); composer.addWidget(self.goal)
            bottom=QHBoxLayout(); composer.addLayout(bottom)
            self.target_label=QLabel('请先选择操作目标'); self.target_label.setObjectName('muted'); self.target_label.setWordWrap(True); bottom.addWidget(self.target_label,1)
            self.send_button=self.button('发送  ↑',self.send_message,bottom); self.send_button.setObjectName('send')
            self.sessions.itemSelectionChanged.connect(self.target_selection_changed)
            hint=QLabel('Enter 发送 · Shift + Enter 换行 · Saygo 会根据截图操作你选择的设备'); hint.setObjectName('muted')
            hint.setAlignment(Qt.AlignmentFlag.AlignCenter); layout.addWidget(hint)
            self.welcome()

        def build_welcome(self):
            self.welcome_page=QScrollArea(); self.welcome_page.setWidgetResizable(True); self.welcome_page.setFrameShape(QFrame.Shape.NoFrame)
            welcome_body=QWidget(); welcome_body.setObjectName('welcomeBody'); self.welcome_page.setWidget(welcome_body)
            column=QVBoxLayout(welcome_body); column.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
            column.setContentsMargins(24,12,24,12); column.setSpacing(10); column.addStretch()
            mark=QLabel('S'); mark.setObjectName('welcomeMark'); mark.setFixedSize(44,44)
            mark.setAlignment(Qt.AlignmentFlag.AlignCenter); column.addWidget(mark,0,Qt.AlignmentFlag.AlignHCenter)
            title=QLabel('从一个想法，开始行动'); title.setObjectName('welcomeTitle')
            title.setAlignment(Qt.AlignmentFlag.AlignCenter); column.addWidget(title)
            subtitle=QLabel('告诉 Saygo 你想完成什么，随时查看过程、暂停或接管。')
            subtitle.setObjectName('muted'); subtitle.setWordWrap(True)
            subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter); column.addWidget(subtitle)
            column.addSpacing(4)
            for title,detail,callback in [
                ('01   配置模型','连接你的视觉模型，安全管理 API Token',lambda:self.dialogs['模型设置'].show()),
                ('02   电脑与浏览器','本机自动接入，按需连接 Chrome',lambda:self.dialogs['设备连接'].show()),
                ('03   描述任务','从观察当前画面开始',lambda:self.fill_example())]:
                card=self.button(title+'\n'+detail,callback,column); card.setObjectName('welcomeCard'); card.setMinimumHeight(60)
            column.addStretch(); self.content.addWidget(self.welcome_page)

        def fill_example(self):
            self.goal.setPlainText('请观察当前画面，告诉我有哪些可以操作的内容。')
            self.goal.setFocus()

        def welcome(self):
            self.last_transcript=''
            for button in (self.pause_button,self.stop_button,self.resolve_button):button.hide()
            self.content.setCurrentWidget(self.welcome_page)

        def new_chat(self):
            if self.worker or self.connection_worker:return
            if self.task_state and self.task_state['status'] not in ('succeeded','cancelled'):
                QMessageBox.information(self,'任务尚未结束','请先停止当前任务，再开始新对话。'); return
            self.task_id=None; self.task_state=None; self.goal.clear(); self.preview.clear()
            self.task_status.setText('新对话'); self.welcome()

        def target_selection_changed(self):
            for index in range(self.sessions.count()):
                item=self.sessions.item(index); serial=item.data(Qt.ItemDataRole.UserRole)
                if serial in (connections.COMPUTER,connections.BROWSER):
                    if item.isSelected():self.disabled_auto.discard(serial)
                    else:self.disabled_auto.add(serial)
            self.update_target_label()

        def update_target_label(self):
            names=[item.text() for item in self.sessions.selectedItems()]
            self.target_label.setText(' · '.join(names) if names else '请先选择操作目标')

        def refresh_sessions(self):
            selected={item.data(Qt.ItemDataRole.UserRole) for item in self.sessions.selectedItems()}
            self.sessions.blockSignals(True); self.sessions.clear()
            for row in control.sessions():
                serial=row['session']
                if row.get('disconnected') or row.get('error'):continue
                if serial==connections.COMPUTER:
                    if not self.computer_ready:continue
                    label='本机电脑 · 整个桌面'
                elif serial==connections.BROWSER:
                    if not self.browser_ready:continue
                    label='Chrome 浏览器 · '+str(len(self.browser_pages))+' 个网页'
                elif row.get('platform')=='browser':
                    if row.get('backend')!='extension' or not row.get('page_id'):continue
                    label='浏览器 · '+serial+'（已保存）'
                else:
                    label=('窗口 · ' if row.get('app') else '设备 · ')+(row.get('app') or row.get('device') or serial)
                item=QListWidgetItem(label); item.setData(Qt.ItemDataRole.UserRole,serial)
                item.setToolTip(label+'\n会话：'+serial); self.sessions.addItem(item)
                default=serial in (connections.COMPUTER,connections.BROWSER) and serial not in self.disabled_auto
                item.setSelected(serial in selected or default)
            self.sessions.blockSignals(False); self.update_target_label()

        def refresh_tasks(self):
            self.tasks.clear()
            for row in reversed(interactive.call('list')['tasks']):
                state=interactive.call('status',row['id'])
                if not state.get('desktop_goal'):continue
                item=QListWidgetItem(state['desktop_goal'].replace('\n',' ')[:28])
                item.setData(Qt.ItemDataRole.UserRole,row['id']); item.setToolTip(state['desktop_goal'])
                self.tasks.addItem(item)
                if row['id']==self.task_id:self.tasks.setCurrentItem(item)

        def send_message(self):
            if self.worker or self.connection_worker:return
            if not self.goal.toPlainText().strip():return
            if self.task_state and self.task_state['status'] in ('waiting_for_human','idle'):
                self.resume_task(self.goal.toPlainText().strip()); return
            if self.task_state and self.task_state['status']=='needs_review':
                QMessageBox.information(self,'需要核对','请先点击“核对操作结果”，确认上一次动作是否完成。'); return
            self.start_task()

        def start_task(self):
            values=self.checked_model_values()
            if values is None:return
            settings,key=values; goal=self.goal.toPlainText().strip()
            bindings={f'target_{i+1}':item.data(Qt.ItemDataRole.UserRole) for i,item in enumerate(self.sessions.selectedItems())}
            if not bindings:
                self.targets_dialog.show(); self.statusBar().showMessage('选择至少一个操作目标，然后发送任务'); return
            if not settings['model'] or not key:
                self.dialogs['模型设置'].show(); self.statusBar().showMessage('请先填写模型和 API Key'); return
            self.goal.clear()
            self.minimize_for_computer(bindings.values())
            def start(emit):
                loop=TaskLoop(VisionModel(settings,key)); state=loop.create(goal,bindings); emit(state)
                return loop.run(state['id'],self.pause_event,self.stop_event,emit)
            self.job(start,loop=True)

        def load_task(self):
            if self.worker or self.connection_worker:return
            item=self.tasks.currentItem()
            task_id=item.data(Qt.ItemDataRole.UserRole) if item else None
            if task_id: self.job(lambda emit:interactive.call('recover',task_id))

        def resume_task(self, note=None):
            if not self.task_id: return
            values=self.checked_model_values()
            if values is None:return
            settings,key=values; task_id=self.task_id
            if note is None:
                note,ok=QInputDialog.getText(self,'继续任务','人工操作或核对说明：',text='已核对，可以继续')
                if not ok or not note.strip(): return
            self.goal.clear()
            self.minimize_for_computer(spec['session'] for spec in self.task_state['workflow']['resources'].values())
            def resume(emit):
                loop=TaskLoop(VisionModel(settings,key)); state=loop.runtime.store.get(task_id)
                if state['status']=='waiting_for_human': loop.runtime.resume_task(task_id,note)
                else:
                    with loop.runtime.store.guard(task_id):
                        state=loop.runtime.store.get(task_id)
                        loop.runtime.store.save(state,'desktop_user_message',{'note':note})
                return loop.run(task_id,self.pause_event,self.stop_event,emit)
            self.job(resume,loop=True)

        def resolve_task(self):
            if not self.task_id: return
            outcome,ok=QInputDialog.getItem(self,'核对动作','根据实际结果选择：',['completed','not_executed'],0,False)
            if not ok:return
            note,ok=QInputDialog.getText(self,'核对证据','你观察到了什么？')
            if ok and note.strip():
                task_id=self.task_id; self.job(lambda emit:interactive.call('resolve',task_id,outcome=outcome,note=note))

        def export_task(self):
            if not self.task_id:return
            path,_=QFileDialog.getSaveFileName(self,'导出任务证据','saygo-task.zip','ZIP (*.zip)')
            if path:
                task_id=self.task_id; self.job(lambda emit:interactive.call('export',task_id,out=path))

        def request_pause(self):
            if self.worker:
                self.pause_event.set(); self.statusBar().showMessage('正在暂停：等待当前调用结束，之后不会派发新动作')
            elif self.task_id:
                task_id=self.task_id; self.job(lambda emit:interactive.call('handoff',task_id,instructions='用户请求人工接管'))

        def request_stop(self):
            if self.worker:
                self.stop_event.set(); self.statusBar().showMessage('正在停止：等待当前调用结束')
            elif self.task_id:
                task_id=self.task_id; self.job(lambda emit:interactive.call('cancel',task_id,note='用户停止'))

        def minimize_for_computer(self, sessions):
            from saygo.platforms import device_session as ds
            if any((ds.load_state(serial) or {}).get('desktop_scope')=='computer' for serial in sessions):
                for dialog in self.dialogs.values():dialog.hide()
                self.targets_dialog.hide(); self.preview_dialog.hide()
                self.task_minimized=True; self.showMinimized()

        def job(self, function, loop=False):
            if self.worker or self.connection_worker:return
            self.pause_event.clear(); self.stop_event.clear()
            self.goal.setEnabled(False); self.tasks.setEnabled(False)
            for field in self.model_fields:field.setEnabled(False)
            for button in self.buttons:button.setEnabled(False)
            self.pause_button.setEnabled(loop); self.stop_button.setEnabled(loop)
            self.worker=Worker(function); self.worker.result.connect(self.show_result); self.worker.update.connect(self.show_result)
            self.worker.failed.connect(self.show_error); self.worker.finished.connect(self.job_done)
            self.statusBar().showMessage('正在执行…'); self.worker.start()

        def job_done(self):
            worker=self.worker; self.worker=None; worker.deleteLater(); self.model_job=None
            for field in self.model_fields:field.setEnabled(True)
            self.goal.setEnabled(True); self.tasks.setEnabled(True)
            for button in self.buttons:button.setEnabled(True)
            self.pause_button.setEnabled(True);self.stop_button.setEnabled(True)
            self.refresh_sessions();self.refresh_tasks()
            if self.task_minimized:
                self.task_minimized=False; self.showNormal(); self.raise_()

        def show_error(self,message):
            self.statusBar().showMessage(message)
            if self.model_job:
                self.model_feedback.setText('操作未完成：'+message)
                return
            QMessageBox.warning(self,'操作未完成',message)
            if self.task_id:
                self.show_result(interactive.call('status',self.task_id))

        def show_result(self,value):
            if not isinstance(value,dict):return
            if value.get('model_operation'):
                if value['model_operation']=='delete':
                    self.key.clear(); self.remember.setChecked(False)
                if value['model_operation'] in ('save','delete'):self.saved_model=self.model_snapshot()
                self.model_feedback.setText(value['message']); self.statusBar().showMessage(value['message'])
                return
            if value.get('mode')=='interactive':
                self.task_id=value['id']; self.task_state=value
                self.pause_button.setVisible(value['status']=='idle')
                self.stop_button.setVisible(value['status'] not in ('succeeded','cancelled'))
                self.resolve_button.setVisible(value['status']=='needs_review')
                statuses={'idle':'执行中' if self.worker else '可以继续','waiting_for_human':'等待你回复','needs_review':'需要核对操作结果','succeeded':'已完成','cancelled':'已停止'}
                self.task_status.setText(f"{statuses.get(value['status'],value['status'])} · 已记录 {value.get('cursor',0)} 步")
                observations=list(value.get('observations',{}).values())
                if observations:
                    pix=QPixmap(observations[-1]['path']); self.preview.setPixmap(pix.scaled(self.preview.size(),Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation))
                else:
                    self.preview.setText('暂无当前操作画面')
                rows=interactive.call('timeline',self.task_id)['timeline']
                self.render_conversation(value,rows)
                self.statusBar().showMessage(value.get('error') or value.get('human',{}).get('instructions','') if value.get('human') else value.get('error') or value['status'])
            else:
                if 'pages' in value:
                    selected=value.get('page_id') or self.page_id.currentData()
                    self.page_id.clear(); self.page_id.addItem('请选择要操作的网页',None)
                    for page in value['pages']:
                        self.page_id.addItem(page.get('title','网页')+' · '+page.get('url',''),page['page_id'])
                    index=self.page_id.findData(selected)
                    if index>=0:self.page_id.setCurrentIndex(index)
                self.device_output.setPlainText(json.dumps(value,ensure_ascii=False,indent=2))
                self.statusBar().showMessage(value.get('message') or value.get('error') or '操作完成')

        def render_conversation(self,state,rows):
            self.content.setCurrentWidget(self.timeline)
            def bubble(role,text):
                user=role=='你'
                return ('<table width="100%" cellspacing="0" cellpadding="14"><tr>'
                        + ('<td width="16%"></td>' if user else '')
                        + '<td bgcolor="'+('#eaf2ee' if user else '#f4f6f8')+'">'
                        + '<p style="color:#587065;font-size:12px;font-weight:600">'+role+'</p>'
                        + '<p style="line-height:150%">'+escape(str(text)).replace('\n','<br>')+'</p></td></tr></table><br>')
            content=bubble('你',state.get('desktop_goal',''))
            for row in rows:
                if row.get('note'):
                    role='你' if row['kind'] in ('human_returned','desktop_user_message') else 'Saygo'
                    content+=bubble(role,row['note'])
                elif row.get('error'):
                    content+=bubble('Saygo','操作未完成：'+str(row['error']))
            if state.get('human'):
                content+=bubble('Saygo',state['human'].get('instructions','请核对后回复，继续任务。'))
            if state.get('error'):content+=bubble('Saygo',str(state['error']))
            if content!=self.last_transcript:
                self.last_transcript=content; self.timeline.setHtml(content)
                self.timeline.verticalScrollBar().setValue(self.timeline.verticalScrollBar().maximum())
            self.goal.setPlaceholderText('回复 Saygo，补充说明并继续任务…' if state['status'] in ('waiting_for_human','idle') else '给 Saygo 发送新任务…')

        def closeEvent(self,event):
            if self.worker or self.connection_worker:
                self.stop_event.set(); event.ignore()
                self.statusBar().showMessage('正在停止；当前调用结束后可关闭窗口')
            else:event.accept()

    return Window()


if __name__ == '__main__':
    raise SystemExit(main())
