"""Project-only MCP entry point. Never registered in the user's global config."""
import os
from pathlib import Path
import runpy
import sys


def main():
    root = Path(__file__).resolve().parents[1]
    if not Path.cwd().resolve().is_relative_to(root):
        raise SystemExit('The development MCP can only run inside its Saygo checkout.')
    os.environ.pop('SAYGO_INSTALL_ROOT', None)
    os.environ['SAYGO_HOME_DIR'] = str(root / '.saygo-dev' / 'state')
    # Only this explicit, project-scoped entry point may import checkout code.
    sys.path.insert(0, str(root))
    runpy.run_module('saygo.mcp.server', run_name='__main__')


if __name__ == '__main__':
    main()
