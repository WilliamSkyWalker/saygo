"""Background update integration: real threads, cache files and MCP result path."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

from saygo import updates as u

BDD = []


def scenario(requirement, given, when, then):
    def decorate(test):
        BDD.append(dict(id='UP-'+str(len(BDD)+1).zfill(3), requirement=requirement,
                        family=test.__name__,given=given,when=when,then=then))
        return test
    return decorate


class PackageUpdateTests(unittest.TestCase):
    def setUp(self):
        temporary=tempfile.TemporaryDirectory(); self.addCleanup(temporary.cleanup)
        self.root=Path(temporary.name)
        self.installed={'python':sys.executable,'version':'0.4.12','runtime_mode':'package'}
        u.write(self.root/'installation.json',self.installed)
        current=patch.object(u,'current',return_value=self.installed)
        current.start(); self.addCleanup(current.stop)
        self.output=io.StringIO()
        stderr=contextlib.redirect_stderr(self.output); stderr.__enter__()
        self.addCleanup(stderr.__exit__,None,None,None)
        # Always release and join background workers before mocks/directories disappear.
        self.release=threading.Event()
        self.addCleanup(self.join_worker)

    def join_worker(self):
        self.release.set()
        with u._CHECK_THREADS_LOCK: worker=u._CHECK_THREADS.get(str(self.root))
        if worker: worker.join(3); self.assertFalse(worker.is_alive())

    def payload(self):
        return json.dumps({'releases':{'0.4.13':[{'yanked':False}]}}).encode()

    @scenario('UPDATE-007','无更新缓存，版本源响应被闸门阻塞','读取 notice 后再释放版本源',
              '首次立即返回 checking，完成后返回 v0.4.13；所有网络工作发生在后台线程')
    def test_notice_refresh_nonblocking(self):
        entered=threading.Event()
        def fetch(url):
            self.assertNotEqual(threading.current_thread(),threading.main_thread())
            entered.set(); self.release.wait(3); return self.payload()
        with patch.object(u,'fetch',side_effect=fetch) as call:
            info=u.notice(self.root)
            self.assertTrue(info['checking']); self.assertTrue(entered.wait(2))
            self.assertNotIn('available',info)
            self.join_worker()
            self.assertEqual(u.notice(self.root)['available'],'v0.4.13')
            call.assert_called_once_with(u.PACKAGE_API)

    @scenario('UPDATE-013','版本检查正在进行，另有八次客户端通知请求','并发读取同一安装的 notice',
              '只启动一次版本查询，所有请求返回而不等待网络')
    def test_notice_coalesces_inflight_requests(self):
        entered=threading.Event()
        def fetch(url): entered.set(); self.release.wait(3); return self.payload()
        with patch.object(u,'fetch',side_effect=fetch) as call:
            u.notice(self.root); self.assertTrue(entered.wait(2))
            clients=[threading.Thread(target=u.notice,args=(self.root,)) for _ in range(8)]
            for client in clients: client.start()
            for client in clients: client.join(2); self.assertFalse(client.is_alive())
            self.join_worker(); self.assertEqual(call.call_count,1)

    @scenario('UPDATE-006','MCP 仍由跳过检查的旧 package launcher 启动且没有缓存','两次调用 device_sessions，中间等待新模块后台检查完成',
              '第一次包含 checking，第二次 updates 明确包含新版本及 pipx 命令')
    def test_mcp_sessions_repairs_old_launcher_gap(self):
        from saygo.mcp import server
        with patch.dict('os.environ',{'SAYGO_INSTALL_ROOT':str(self.root)}), patch('saygo.devices.control.sessions',return_value=[]), patch.object(u,'fetch',return_value=self.payload()):
            first=server.device_sessions(); self.assertTrue(first['updates']['checking'])
            self.join_worker()
            second=server.device_sessions()['updates']
            self.assertEqual(second['available'],'v0.4.13')
            self.assertIn('pipx upgrade saygo-agent-control',second['message'])
            self.assertIs(second['automatic'],False)

    @scenario('UPDATE-012','已有 v0.4.13 检查结果，版本源随后离线','再次强制检查并读取提醒',
              '保留已知新版本并同时报告离线错误，安装信息不变')
    def test_offline_preserves_known_release_and_reports_error(self):
        with patch.object(u,'fetch',return_value=self.payload()):u.check(self.root,True)
        with patch.object(u,'fetch',side_effect=OSError('offline')) as call:
            u.check(self.root,True)
            info=u.notice(self.root)
            self.assertEqual(info['available'],'v0.4.13'); self.assertIn('offline',info['error'])
            call.assert_called_once()
        self.assertEqual(u.read(self.root/'installation.json'),self.installed)

    @scenario('UPDATE-011','旧缓存提示 0.4.13，实际包已升级为 0.4.13','读取更新通知',
              '不再提示同版本，并触发与新版本匹配的缓存更新')
    def test_upgrade_invalidates_cache(self):
        with patch.object(u,'fetch',return_value=self.payload()):u.check(self.root,True)
        self.installed['version']='0.4.13'
        with patch.object(u,'start_check',return_value=True) as start:
            self.assertNotIn('available',u.notice(self.root)); start.assert_called_once()

    @scenario('UPDATE-012','包版本元数据读取失败','客户端读取 notice',
              '返回结构化错误而非抛异常阻断设备工具')
    def test_version_read_error_is_nonfatal(self):
        with patch.object(u,'current',side_effect=OSError('metadata unavailable')):
            info=u.notice(self.root); self.assertIn('metadata unavailable',info['error'])

    @scenario('UPDATE-004','package 安装有可用更新且旧配置 automatic=true','直接调用 apply(stage_only=True)',
              '明确拒绝且不下载资源、不创建 managed runtime 指针')
    def test_apply_cannot_bypass_package_policy(self):
        with patch.object(u,'asset') as asset:
            with self.assertRaisesRegex(ValueError,'pipx upgrade'):
                u.apply(self.root,{'available':True},stage_only=True)
            asset.assert_not_called()
        self.assertFalse((self.root/'active-runtime.json').exists())

    @scenario('UPDATE-002','package 启动且版本源离线','启动 MCP 并等待后台失败',
              'MCP 子进程仍启动，stdout 没有诊断文本，stderr 有更新错误')
    def test_startup_offline_does_not_block_or_pollute_stdout(self):
        with patch.object(u,'fetch',side_effect=OSError('offline')), patch.object(u,'run_server',return_value=0) as server, contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(u.serve(self.root,[]),0); self.join_worker()
            server.assert_called_once(); self.assertEqual(out.getvalue(),'')
            self.assertIn('offline',self.output.getvalue())

    @scenario('UPDATE-012','线程资源耗尽导致 Thread.start 失败','读取通知后重试调度',
              '通知返回错误，未遗留阻止未来重试的运行标记')
    def test_thread_start_failure_clears_marker(self):
        with patch.object(u.threading.Thread,'start',side_effect=RuntimeError('thread unavailable')):
            info=u.notice(self.root); self.assertIn('thread unavailable',info['error'])
        self.assertNotIn(str(self.root),u._CHECK_THREADS)

    @scenario('UPDATE-014','缓存文件可读取，但原子写入因只读文件系统失败','后台刷新版本检查',
              '线程正常结束并记录错误，MCP 通知不抛异常')
    def test_readonly_cache_failure_is_contained(self):
        with patch.object(u,'fetch',return_value=self.payload()), patch.object(u,'write',side_effect=OSError('read only')):
            u.notice(self.root); self.join_worker()
            self.assertIn('read only',self.output.getvalue())

    @scenario('UPDATE-009','PyPI 高版本只有 yanked 文件，中间版本有可用 wheel，预发布和空文件版本并存','强制检查 package 更新',
              '选择最高有未撤回文件的稳定版本，不选择空文件或预发布版本')
    def test_pypi_files_and_numeric_ordering(self):
        payload={'releases':{'0.4.13':[{'yanked':False}], '0.10.0':[{'yanked':True},{'yanked':False}],
                             '1.0.0':[{'yanked':True}], '2.0.0':[], '3.0.0rc1':[{'yanked':False}]}}
        with patch.object(u,'fetch',return_value=json.dumps(payload).encode()):
            self.assertEqual(u.check(self.root,True)['release']['tag_name'],'v0.10.0')

    @scenario('UPDATE-003','installation.json 版本陈旧且残留 active-runtime.json','读取实际 package 版本',
              '版本取自 pipx 解释器的包元数据，忽略 managed 指针')
    def test_package_current_uses_installed_interpreter(self):
        # The setup patch is bypassed here to exercise the production function.
        u.write(self.root/'active-runtime.json',{'python':sys.executable,'version':'9.0.0'})
        with patch.object(u.subprocess,'check_output',return_value='0.4.13\n') as call:
            actual=ORIGINAL_CURRENT(self.root)
            self.assertEqual(actual['version'],'0.4.13')
            self.assertEqual(call.call_args.args[0][0],sys.executable)


ORIGINAL_CURRENT=u.current


class PackageBridgeSyncTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.installed = {'python':sys.executable, 'version':'0.4.14', 'browser':'chrome',
                          'extension_id':'a' * 32, 'bridge':{'directory':'old/Saygo/browser-bridge'}}
        u.write(self.root/'installation.json', self.installed)

    @scenario('UPDATE-019','Python 包版本相同，但桌面版在线 bridge 与安装记录不同','同步 package bridge',
              '先发现共享目录再修复注册与安装记录，不因版本相同跳过')
    def test_same_package_version_still_repairs_a_changed_shared_directory(self):
        repaired = {'directory':'shared/.saygo/browser-bridge', 'installed':True}
        with patch.object(u.subprocess, 'check_output', side_effect=[json.dumps(repaired), json.dumps(repaired)]) as call:
            u.synchronize_package_bridge(self.root, self.installed)
        self.assertEqual(call.call_count, 2)
        self.assertIn('--resolve-only', call.call_args_list[0].args[0])
        self.assertNotIn('--resolve-only', call.call_args_list[1].args[0])
        self.assertEqual(u.read(self.root/'installation.json')['bridge'], repaired)

    @scenario('UPDATE-019','包版本、共享目录、实际注册与安装记录全部一致','同步 package bridge',
              '只执行只读发现，不重复安装 native host 或改写安装记录')
    def test_matching_shared_directory_and_package_version_do_not_reinstall(self):
        resolved = {**self.installed['bridge'], 'registered_directory':self.installed['bridge']['directory']}
        with patch.object(u.subprocess, 'check_output', return_value=json.dumps(resolved)) as call:
            u.synchronize_package_bridge(self.root, self.installed)
        self.assertEqual(call.call_count, 1)
        self.assertEqual(u.read(self.root/'installation.json'), self.installed)

    @scenario('UPDATE-019','包版本与在线目录一致，但浏览器实际注册指向另一目录','同步 package bridge',
              '修复实际注册，避免下次插件连接进入另一套 bridge')
    def test_matching_version_and_live_directory_still_repair_stale_registration(self):
        resolved = {**self.installed['bridge'], 'registered_directory':'another/bridge'}
        with patch.object(u.subprocess, 'check_output', side_effect=[json.dumps(resolved), json.dumps(self.installed['bridge'])]) as call:
            u.synchronize_package_bridge(self.root, self.installed)
        self.assertEqual(call.call_count, 2)

    @scenario('UPDATE-019','外部升级 Python 包后共享 bridge 目录不变','同步 package bridge',
              '更新 host 安装及版本记录，不因目录相同漏掉升级')
    def test_package_upgrade_updates_host_even_when_directory_is_unchanged(self):
        current = dict(self.installed, version='0.4.15')
        with patch.object(u.subprocess, 'check_output', return_value=json.dumps(self.installed['bridge'])) as call:
            u.synchronize_package_bridge(self.root, current)
        self.assertEqual(call.call_count, 2)
        self.assertEqual(u.read(self.root/'installation.json')['version'], '0.4.15')

    @scenario('UPDATE-019','共享 bridge 发现失败或繁忙','同步 package bridge',
              '保留原安装记录并报告更新待完成，不擅自建立第二套 bridge')
    def test_discovery_failure_preserves_installation_and_reports_pending(self):
        with patch.object(u.subprocess, 'check_output', side_effect=OSError('bridge busy')) as call, \
             contextlib.redirect_stderr(io.StringIO()) as errors:
            u.synchronize_package_bridge(self.root, self.installed)
        self.assertEqual(call.call_count, 1)
        self.assertEqual(u.read(self.root/'installation.json'), self.installed)
        self.assertIn('Native host update pending', errors.getvalue())
