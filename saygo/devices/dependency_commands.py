"""Read-only mobile dependency checks and commands for the current interpreter."""
import importlib.metadata
import importlib.util
import json
import os
from pathlib import Path
import re
import shlex
import sys
import sysconfig


def format_command(argv):
    """Render literal arguments for the client's shell, without executing them."""
    if not argv or any(not isinstance(arg, str) or not arg or
                       any(char in arg for char in '\x00\r\n') for arg in argv):
        raise ValueError('Command arguments must be nonempty single-line strings')
    if sys.platform == 'win32':
        quoted = ["'" + arg.replace("'", "''") + "'" for arg in argv]
        return {'command': '& ' + ' '.join(quoted), 'shell': 'powershell'}
    return {'command': shlex.join(argv), 'shell': 'posix'}


def _available(module):
    try:
        return importlib.util.find_spec(module) is not None
    except (ImportError, ValueError):
        return False


def _mobile_requirements():
    # A checkout's declaration wins over any older wheel in this interpreter.
    project = Path(__file__).resolve().parents[2] / 'pyproject.toml'
    source = project.is_file()
    if source:
        try:
            import tomllib
        except ImportError:  # Python 3.10; pip is a declared core dependency.
            from pip._vendor import tomli as tomllib
        with project.open('rb') as stream:
            data = tomllib.load(stream)['project']
        if not isinstance(data, dict) or data.get('name') != 'saygo-agent-control':
            raise ValueError('The source project does not declare Saygo')
        extras = data.get('optional-dependencies', {})
        if not isinstance(extras, dict):
            raise ValueError('The source project has an invalid optional dependency declaration')
        declared = extras.get('mobile')
        if not isinstance(declared, list) or not declared:
            raise ValueError('The source project has no mobile dependency declaration')
    else:
        declared = importlib.metadata.distribution('saygo-agent-control').requires or []
    try:
        from packaging.requirements import Requirement
    except ImportError:
        from pip._vendor.packaging.requirements import Requirement
    requirements = []
    for value in declared:
        requirement = Requirement(value)
        marker = requirement.marker
        if source:
            if marker and not marker.evaluate({'extra': 'mobile'}):
                continue
        elif not marker or not marker.evaluate({'extra': 'mobile'}) or marker.evaluate({'extra': ''}):
            # Select only requirements enabled by the mobile extra, not core deps.
            continue
        if re.sub(r'[-_.]+', '-', requirement.name).lower() == 'saygo-agent-control':
            raise ValueError('Mobile dependency repair must not reinstall Saygo')
        # Extra markers are already evaluated. Keeping them would make standalone
        # pip arguments skip these dependencies, since no extra is active there.
        requirement.marker = None
        rendered = str(requirement)
        if rendered not in requirements:
            requirements.append(rendered)
    if not requirements:
        raise ValueError('No mobile dependencies apply to this interpreter')
    return requirements


def _managed_note():
    root = os.environ.get('SAYGO_INSTALL_ROOT')
    if not root:
        return None
    try:
        record = json.loads((Path(root).expanduser() / 'installation.json').read_text())
        if not isinstance(record, dict):
            raise ValueError('Expected installation metadata object')
    except (OSError, ValueError):
        return 'Managed installation metadata could not be read; this command only repairs the current interpreter.'
    if record.get('runtime_mode', 'managed') == 'managed':
        return ('This repairs only the current managed runtime. Future managed updates must retain '
                'the mobile configuration; this command does not update installation metadata.')
    return None


def mobile_python_check(*, force=False):
    """Describe manual repair; force guidance after a reported dependency import failure."""
    result = {'id': 'python_mobile', 'status': 'ready', 'message': '', 'commands': [], 'notes': []}
    if not force and _available('appium'):
        result['message'] = 'The Appium Python client is available in the running interpreter.'
        return result
    result['status'] = 'blocked'
    if getattr(sys, 'frozen', False):
        result['message'] = ('This packaged application is missing the Appium Python client. '
                             'Use a build with mobile dependencies or a separate Python CLI installation; '
                             'the packaged executable cannot run pip.')
        return result
    if not sys.executable or not _available('pip'):
        result['message'] = ('The Appium Python client is missing, and pip is unavailable in the running '
                             'interpreter. Restore pip for this installation before repairing dependencies.')
        return result
    try:
        requirements = _mobile_requirements()
        # Preserve the environment's executable path, including pipx/venv symlinks.
        argv = [sys.executable, '-m', 'pip', 'install']
        externally_managed = (sys.prefix == sys.base_prefix and
            (Path(sysconfig.get_path('stdlib')) / 'EXTERNALLY-MANAGED').is_file())
        if externally_managed:
            argv.append('--break-system-packages')
            result['notes'].append(
                'Manual confirmation required: PEP 668 marks this Python as externally managed. '
                '--break-system-packages overrides that protection and may change or conflict with '
                'system-managed Python packages. Use this option only if you intend to modify this global installation.')
        argv.extend(requirements)
        command = {'argv': argv, **format_command(argv), 'run_on': 'client',
                   'label': 'Install mobile Python dependencies in the running Saygo interpreter',
                   'manual_confirmation': externally_managed}
    except (ImportError, OSError, ValueError, KeyError, TypeError) as exc:
        result['message'] = 'Cannot determine a safe mobile dependency repair command: ' + str(exc)
        return result
    message = ('The Appium Python client or one of its dependencies could not be imported by the running Saygo interpreter.'
               if force else 'The Appium Python client is missing from the running Saygo interpreter.')
    result.update(status='missing', message=message, commands=[command])
    result['notes'].append(
        'Run this command on the client running Saygo, including WSL when Android runs on a Windows host. '
        'It installs declared dependencies only; it does not reinstall Saygo, create an environment, or register plugins. '
        'Dependency resolution can still change Python dependency versions.')
    managed = _managed_note()
    if managed:
        result['notes'].append(managed)
    return result
