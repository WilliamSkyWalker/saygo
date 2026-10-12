"""Shared light palette for the desktop shell and its dialogs."""

STYLESHEET = '''
QWidget { color: #25352f; font-size: 14px; }
QMainWindow, QDialog, QScrollArea, QWidget#welcomeBody { background: #ffffff; }
QLabel { background: transparent; }
QFrame#sidebar { background: #f3f5f4; border-right: 1px solid #e3e9e5; }
QLabel#brand { font-size: 30px; font-weight: 700; color: #234d3e; padding-bottom: 18px; }
QLabel#title { font-size: 22px; font-weight: 600; }
QLabel#muted { color: #6e7e76; font-size: 12px; }
QLabel#badge { color: #526b60; background: #eef4f0; border-radius: 8px; padding: 8px 12px; }
QLabel#welcomeMark { background: #265c46; color: white; border-radius: 16px; font-size: 28px; font-weight: 600; }
QLabel#welcomeTitle { font-size: 28px; font-weight: 600; padding-top: 8px; }
QPushButton { background: #f3f5f4; border: 1px solid #e4eae6; border-radius: 9px; padding: 10px 14px; text-align: left; }
QPushButton:hover { background: #e9efeb; border-color: #c6d6cc; }
QPushButton:pressed { background: #dce8e0; }
QPushButton:focus { border: 1px solid #38785b; }
QPushButton:disabled { background: #f4f5f4; color: #9aa69f; border-color: #edf0ee; }
QPushButton#primary, QPushButton#send { background: #265c46; color: white; border: 1px solid #265c46; font-weight: 600; }
QPushButton#primary:hover, QPushButton#send:hover { background: #337757; }
QPushButton#primary:disabled, QPushButton#send:disabled { background: #b5c7bc; border-color: #b5c7bc; color: white; }
QPushButton#send { text-align: center; padding: 10px 22px; }
QPushButton#welcomeCard { background: #f8faf9; padding: 8px 20px; text-align: left; }
QPushButton#welcomeCard:hover { background: #eef5f0; border-color: #b7cebf; }
QLineEdit, QPlainTextEdit, QComboBox { background: #fafcfb; border: 1px solid #dbe4de; border-radius: 8px; padding: 10px; selection-background-color: #d1e6d9; selection-color: #20372a; }
QLineEdit:focus, QPlainTextEdit:focus, QComboBox:focus { border-color: #38785b; background: white; }
QLineEdit:disabled, QPlainTextEdit:disabled, QComboBox:disabled { color: #89968e; background: #f2f5f3; }
QComboBox::drop-down { border: 0; width: 26px; }
QListWidget { background: #f3f5f4; border: 0; outline: 0; padding: 4px; }
QListWidget::item { padding: 12px 8px; margin-bottom: 4px; border-radius: 8px; }
QListWidget::item:hover { background: #e9efeb; }
QListWidget::item:selected { background: #dfeae3; color: #244e39; }
QListWidget:focus { border: 1px solid #b7cebf; }
QTextBrowser { background: white; border: 0; padding: 8px; selection-background-color: #d1e6d9; }
QFrame#composer { background: white; border: 1px solid #c9d9ce; border-radius: 16px; }
QFrame#composer QPlainTextEdit { background: transparent; border: 0; padding: 6px; }
QLabel#feedback { background: #eef4f0; color: #355b47; border-radius: 10px; padding: 16px; }
QCheckBox { spacing: 8px; padding: 4px 0; }
QStatusBar { background: #fafcfb; color: #738178; font-size: 12px; border-top: 1px solid #edf1ee; }
QScrollBar:vertical { background: transparent; width: 8px; margin: 2px; }
QScrollBar::handle:vertical { background: #cbd5ce; border-radius: 3px; min-height: 30px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }
QToolTip { background: #253d30; color: white; border: 0; padding: 6px; }
'''
