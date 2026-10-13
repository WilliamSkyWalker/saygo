"""Check actual MCP stdio profiles and schemas in the installed SDK environment."""
import asyncio
import json
import os
from pathlib import Path
import sys
import tempfile
from importlib.metadata import version

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from saygo.mcp.server import _DEVICE_PROFILE_KEEP, _RUN_PROFILE_ONLY


async def check():
    with tempfile.TemporaryDirectory(prefix='saygo-mcp-check-') as directory:
        root = Path(directory)
        env = {**os.environ, 'SAYGO_HOME_DIR': str(root), 'SAYGO_RUNTIME_DIR': str(root / 'runtime')}
        env.pop('SAYGO_INSTALL_ROOT', None)
        for profile in ('device', 'full'):
            parameters = StdioServerParameters(command=sys.executable,
                args=['-m', 'saygo.mcp.server', '--profile', profile], env=env)
            async with stdio_client(parameters) as (reader, writer):
                async with ClientSession(reader, writer) as client:
                    await client.initialize()
                    tools = {tool.name: tool for tool in (await client.list_tools()).tools}
                    expected = _DEVICE_PROFILE_KEEP | (_RUN_PROFILE_ONLY if profile == 'full' else set())
                    assert set(tools) == expected, (profile, set(tools) ^ expected)
                    for name in ('device_act', 'device_tap', 'device_input', 'device_key',
                                 'device_swipe', 'device_launch', 'device_type_send'):
                        assert {'observation_id', 'request_id'} <= set(tools[name].inputSchema['properties']), name
                    result = await client.call_tool('device_command', {'command': 'operations', 'session': 'example'})
                    value = next(json.loads(row.text) for row in result.content if row.type == 'text')
                    assert value == {'ok': True, 'operations': []}, value
            print(f'MCP {version("mcp")} {profile}: stdio handshake, tool set, input schemas and request query passed')


if __name__ == '__main__':
    asyncio.run(asyncio.wait_for(check(), timeout=45))
