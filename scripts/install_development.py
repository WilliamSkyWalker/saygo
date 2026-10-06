"""Prepare a Codex development MCP in this checkout, never in user configuration."""
import argparse
import json
from pathlib import Path
import shutil
import sys

from install_agent_plugin import prepare_runtime, parse_toml, write_codex_config


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mobile', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if not (root / '.git').exists():
        parser.error('Development installation requires a source checkout')
    config = root / '.codex' / 'config.toml'
    old = config.read_text() if config.exists() else ''
    start = '# BEGIN SAYGO DEVELOPMENT\n'
    end = '# END SAYGO DEVELOPMENT\n'
    if start in old:
        left, tail = old.split(start, 1)
        _, right = tail.split(end, 1)
        clean = left + right
    else:
        clean = old
    existing = parse_toml(clean)
    if 'saygo' in existing.get('mcp_servers', {}) or 'saygo-device@saygo-managed' in existing.get('plugins', {}):
        parser.error('Project already has independent Saygo configuration; left unchanged')
    extras = ['mcp']
    if args.mobile:
        extras.append('mobile')
    if sys.platform == 'win32':
        extras.append('windows')
    elif sys.platform == 'darwin':
        extras.append('mac')
    python = prepare_runtime(root, root / '.saygo-dev', ','.join(extras))
    block = (start + '[plugins."saygo-device@saygo-managed"]\nenabled = false\n\n'
             '[mcp_servers.saygo]\ncommand = ' + json.dumps(str(python)) + '\n'
             'args = ' + json.dumps(['-I', str(root/'scripts/development_mcp.py'), '--profile', 'device']) + '\n' + end)
    updated = clean.rstrip() + '\n\n' + block
    parse_toml(updated)
    write_codex_config(config, old, updated)
    skill = root / '.agents' / 'skills' / 'saygo-device'
    skill.mkdir(parents=True, exist_ok=True)
    shutil.copy2(root/'plugins/saygo-device/skills/device/SKILL.md', skill/'SKILL.md')
    print('Development MCP configured only in ' + str(config))
    print('User MCP, native host registration and browser connection were not changed.')


if __name__ == '__main__':
    main()
