"""Launchable local applications, not UI content or an uninstaller inventory."""
import json
import subprocess
import os
from pathlib import Path
import platform


def installed_applications(system=None):
    system = system or platform.system()
    roots = []
    if system == 'Windows':
        for variable in ('APPDATA', 'PROGRAMDATA'):
            if os.environ.get(variable):
                roots.append(Path(os.environ[variable])/'Microsoft/Windows/Start Menu/Programs')
        suffix = '.lnk'
    elif system == 'Darwin':
        roots = [Path('/Applications'), Path('/System/Applications'), Path.home()/'Applications']
        suffix = '.app'
    else:
        return []
    apps = {}
    for root in roots:
        if not root.is_dir():
            continue
        for directory, folders, files in os.walk(root):
            # Never descend into application bundles or follow directory symlinks.
            candidates = folders[:] if suffix == '.app' else files
            for name in candidates:
                if not name.lower().endswith(suffix):
                    continue
                path = Path(directory)/name
                if suffix == '.app':
                    folders.remove(name)
                apps[str(path)] = {'name': path.stem, 'target': str(path)}
    if system == 'Windows':
        try:
            result = subprocess.run(
                ['powershell.exe', '-NoProfile', '-NonInteractive', '-Command',
                 '[Console]::OutputEncoding=[Text.Encoding]::UTF8; @(Get-StartApps | Select-Object Name,AppID) | ConvertTo-Json -Compress'],
                capture_output=True, text=True, encoding='utf-8', check=True, timeout=15,
                creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
            rows = json.loads(result.stdout.strip().lstrip('\ufeff') or '[]')
            if isinstance(rows, dict):rows=[rows]
            names = {app['name'].casefold() for app in apps.values()}
            for row in rows:
                if row.get('Name') and row.get('AppID') and row['Name'].casefold() not in names:
                    target = 'shell:AppsFolder\\'+row['AppID']
                    apps[target] = {'name': row['Name'], 'target': target}
        except (OSError, ValueError, subprocess.SubprocessError):
            pass  # Start-menu launchers remain available when the catalog is unavailable.
    return sorted(apps.values(), key=lambda app: (app['name'].casefold(), app['target']))
