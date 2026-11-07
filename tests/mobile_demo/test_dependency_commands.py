"""Dependency guidance targets the caller without installing or changing bindings."""
import contextlib
import importlib.metadata
import json
from pathlib import Path
import shlex
import tempfile
import unittest
from unittest.mock import patch

from saygo.devices import dependency_commands as commands


class DependencyCommandTests(unittest.TestCase):
    def setUp(self):
        self.stack = contextlib.ExitStack()
        self.addCleanup(self.stack.close)
        self.root = Path(self.stack.enter_context(tempfile.TemporaryDirectory()))
        self.source = self.root / 'checkout'
        self.source.mkdir()
        self.module_file = self.source / 'saygo/devices/dependency_commands.py'
        self.stack.enter_context(patch.object(commands, '__file__', str(self.module_file)))
        self.stack.enter_context(patch.object(commands.sys, 'executable', '/example/env/bin/python'))
        self.stack.enter_context(patch.object(commands.sys, 'platform', 'darwin'))
        self.stack.enter_context(patch.object(commands.sys, 'prefix', '/example/env'))
        self.stack.enter_context(patch.object(commands.sys, 'base_prefix', '/example/base'))
        self.stack.enter_context(patch.object(commands.sys, 'frozen', False, create=True))
        self.stack.enter_context(patch.dict(commands.os.environ, {}, clear=True))
        self.spec = self.stack.enter_context(patch.object(commands.importlib.util, 'find_spec',
            side_effect=lambda name: None if name == 'appium' else object()))
        self.metadata = self.stack.enter_context(patch.object(commands.importlib.metadata, 'distribution'))
        self.metadata.return_value.requires = [
            'Pillow>=10', 'Appium-Python-Client>=4; extra == "mobile"',
            'uiautomator2>=3.5,<4; extra == "mobile"',
            'playwright>=1; extra == "browser"',
        ]
        self.stdlib = self.root / 'stdlib'
        self.stdlib.mkdir()
        self.stack.enter_context(patch.object(commands.sysconfig, 'get_path', return_value=str(self.stdlib)))

    def write_project(self, requirements):
        (self.source / 'pyproject.toml').write_text(
            '[project]\nname = "saygo-agent-control"\n'
            '[project.optional-dependencies]\nmobile = ' + json.dumps(requirements) + '\n')

    def test_ready_requires_no_metadata_or_install_command(self):
        self.spec.side_effect = lambda name: object()
        result = commands.mobile_python_check()
        self.assertEqual(result['id'], 'python_mobile')
        self.assertEqual(result['status'], 'ready')
        self.assertEqual(result['commands'], [])
        self.metadata.assert_not_called()

    def test_forced_check_repairs_import_failure_despite_available_appium_spec(self):
        self.spec.side_effect = lambda name: object()
        result = commands.mobile_python_check(force=True)
        self.assertEqual(result['status'], 'missing')
        command, = result['commands']
        self.assertEqual(command['argv'][:4], ['/example/env/bin/python', '-m', 'pip', 'install'])
        self.assertIn('Appium-Python-Client>=4', command['argv'])
        self.assertIn('dependencies', result['message'])

    def test_pip_and_pipx_repair_only_dependencies_in_the_running_interpreter(self):
        for executable in ('/example/global/python3', '/example/pipx/venvs/saygo-agent-control/bin/python'):
            with self.subTest(executable=executable), patch.object(commands.sys, 'executable', executable):
                result = commands.mobile_python_check()
                self.assertEqual(result['status'], 'missing')
                command, = result['commands']
                self.assertEqual(command['argv'][:4], [executable, '-m', 'pip', 'install'])
                self.assertEqual(set(command['argv'][4:]), {'Appium-Python-Client>=4', 'uiautomator2<4,>=3.5'})
                self.assertEqual(command['run_on'], 'client')
                self.assertFalse(command['manual_confirmation'])
                self.assertNotIn('saygo-agent-control', command['argv'][4:])
                self.assertEqual(shlex.split(command['command']), command['argv'])

    def test_current_source_requirements_override_stale_installed_metadata(self):
        self.write_project(['Appium-Python-Client>=7', 'uiautomator2>=3.8,<4'])
        self.metadata.return_value.requires = ['Appium-Python-Client==1; extra == "mobile"']
        result = commands.mobile_python_check()
        self.assertEqual(set(result['commands'][0]['argv'][4:]),
                         {'Appium-Python-Client>=7', 'uiautomator2<4,>=3.8'})
        self.metadata.assert_not_called()

    def test_invalid_current_source_does_not_fall_back_to_installed_metadata(self):
        for source in ('[invalid', 'project = "invalid"',
                       '[project]\nname = "saygo-agent-control"\noptional-dependencies = []'):
            with self.subTest(source=source):
                (self.source / 'pyproject.toml').write_text(source)
                result = commands.mobile_python_check()
                self.assertEqual(result['status'], 'blocked')
                self.assertEqual(result['commands'], [])
                self.metadata.assert_not_called()

    def test_installed_extra_markers_are_evaluated_before_command_generation(self):
        self.metadata.return_value.requires = [
            'Appium-Python-Client>=4; extra == "mobile"',
            'example-supported>=1; extra == "mobile" and python_version >= "3.10"',
            'example-obsolete>=1; extra == "mobile" and python_version < "3.10"',
            'example-browser>=1; extra == "browser"',
            'Pillow>=10',
        ]
        result = commands.mobile_python_check()
        self.assertEqual(set(result['commands'][0]['argv'][4:]),
                         {'Appium-Python-Client>=4', 'example-supported>=1'})
        self.assertNotIn('extra', result['commands'][0]['command'])

    def test_posix_quotes_spaces_apostrophes_and_shell_expansion_literally(self):
        argv = ["/example/User's env/bin/python", '-m', 'pip', 'install', 'example>=1; x="$(secret)"']
        result = commands.format_command(argv)
        self.assertEqual(result['shell'], 'posix')
        self.assertEqual(shlex.split(result['command']), argv)

    def test_windows_powershell_uses_call_operator_and_single_quote_escaping(self):
        argv = ["C:\\Example User's Env\\python.exe", '-m', 'pip', 'install', 'Appium-Python-Client>=4']
        with patch.object(commands.sys, 'platform', 'win32'):
            result = commands.format_command(argv)
        self.assertEqual(result['shell'], 'powershell')
        self.assertEqual(result['command'],
            "& 'C:\\Example User''s Env\\python.exe' '-m' 'pip' 'install' 'Appium-Python-Client>=4'")

    def test_native_windows_mac_and_wsl_always_target_the_client_interpreter(self):
        for platform, executable, shell in (
            ('win32', 'C:\\Example Env\\python.exe', 'powershell'),
            ('darwin', '/example/mac/bin/python', 'posix'),
            ('linux', '/example/wsl/bin/python', 'posix'),
        ):
            with self.subTest(platform=platform), patch.object(commands.sys, 'platform', platform), \
                    patch.object(commands.sys, 'executable', executable):
                result = commands.mobile_python_check()
                command, = result['commands']
                self.assertEqual(command['argv'][0], executable)
                self.assertEqual(command['shell'], shell)
                self.assertEqual(command['run_on'], 'client')

    def test_interpreter_symlink_is_not_resolved_out_of_its_environment(self):
        base = self.root / 'python'
        base.touch()
        link = self.root / 'venv-python'
        try:
            link.symlink_to(base)
        except OSError:
            self.skipTest('Symlinks unavailable')
        with patch.object(commands.sys, 'executable', str(link)):
            result = commands.mobile_python_check()
        self.assertEqual(result['commands'][0]['argv'][0], str(link))

    def test_frozen_missing_dependency_does_not_offer_pip(self):
        with patch.object(commands.sys, 'frozen', True):
            result = commands.mobile_python_check()
        self.assertEqual(result['status'], 'blocked')
        self.assertEqual(result['commands'], [])
        self.assertIn('packaged', result['message'].lower())
        self.metadata.assert_not_called()

    def test_pep668_global_option_is_explicitly_manual_and_explains_system_impact(self):
        (self.stdlib / 'EXTERNALLY-MANAGED').touch()
        with patch.object(commands.sys, 'prefix', '/example/base'):
            result = commands.mobile_python_check()
        self.assertEqual(result['status'], 'missing')
        command, = result['commands']
        self.assertTrue(command['manual_confirmation'])
        self.assertIn('--break-system-packages', command['argv'])
        self.assertIn('system', ' '.join(result['notes']).lower())
        self.assertIn('PEP 668', ' '.join(result['notes']))
        self.assertNotIn('--user', command['argv'])

    def test_pep668_base_marker_does_not_require_override_inside_venv(self):
        (self.stdlib / 'EXTERNALLY-MANAGED').touch()
        result = commands.mobile_python_check()
        command, = result['commands']
        self.assertFalse(command['manual_confirmation'])
        self.assertNotIn('--break-system-packages', command['argv'])

    def test_managed_repair_discloses_future_mobile_configuration_requirement(self):
        managed = self.root / 'managed'
        managed.mkdir()
        record = managed / 'installation.json'
        record.write_text('{"runtime_mode":"managed","mobile":false}')
        before = record.read_bytes()
        with patch.dict(commands.os.environ, {'SAYGO_INSTALL_ROOT': str(managed)}):
            result = commands.mobile_python_check()
        self.assertIn('future', ' '.join(result['notes']).lower())
        self.assertIn('mobile', ' '.join(result['notes']).lower())
        self.assertEqual(record.read_bytes(), before)
        self.assertNotIn('setup', result['commands'][0]['argv'])

    def test_invalid_managed_metadata_does_not_hide_dependency_guidance(self):
        managed = self.root / 'managed'
        managed.mkdir()
        (managed / 'installation.json').write_text('[]')
        with patch.dict(commands.os.environ, {'SAYGO_INSTALL_ROOT': str(managed)}):
            result = commands.mobile_python_check()
        self.assertEqual(result['status'], 'missing')
        self.assertTrue(result['commands'])
        self.assertIn('metadata', ' '.join(result['notes']))

    def test_missing_pip_or_dependency_metadata_never_proposes_a_broken_command(self):
        self.spec.side_effect = lambda name: None
        result = commands.mobile_python_check()
        self.assertEqual(result['status'], 'blocked')
        self.assertEqual(result['commands'], [])
        self.spec.side_effect = lambda name: None if name == 'appium' else object()
        self.metadata.side_effect = importlib.metadata.PackageNotFoundError('saygo-agent-control')
        result = commands.mobile_python_check()
        self.assertEqual(result['status'], 'blocked')
        self.assertEqual(result['commands'], [])

    def test_self_dependency_cannot_reinstall_or_change_saygo_version(self):
        self.write_project(['saygo-agent-control[mobile]>=99'])
        result = commands.mobile_python_check()
        self.assertEqual(result['status'], 'blocked')
        self.assertEqual(result['commands'], [])


if __name__ == '__main__':
    unittest.main()
