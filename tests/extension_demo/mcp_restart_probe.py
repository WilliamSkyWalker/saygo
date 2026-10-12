"""Real MCP stdio lifecycle against the live test extension (no mocked transport)."""
import asyncio
import base64
import io
import json
import os
from pathlib import Path
import sys

from PIL import Image
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def exercise(root, bridge, page_id):
    env = {**os.environ, 'SAYGO_HOME_DIR':str(root), 'SAYGO_RUNTIME_DIR':str(root / 'runtime')}
    env.pop('SAYGO_INSTALL_ROOT', None)
    parameters = StdioServerParameters(command=sys.executable,
        args=['-m', 'saygo.mcp.server', '--profile', 'device'], env=env)
    observations = []
    for phase in range(2):
        async with stdio_client(parameters) as (reader, writer):
            async with ClientSession(reader, writer) as client:
                await client.initialize()

                async def call(name, arguments):
                    result = await client.call_tool(name, arguments)
                    value = next(json.loads(item.text) for item in result.content if item.type == 'text')
                    assert not getattr(result, 'is_error', getattr(result, 'isError', False)), value
                    assert value.get('ok') is not False, value
                    return value, result

                if phase == 0:
                    bound, _ = await call('device_connect', {'platform':'browser','session':'restart-fixture',
                        'options':{'backend':'extension','bridge_directory':str(bridge),'page_id':page_id}})
                    assert bound['connected'], bound
                sessions, _ = await call('device_sessions', {})
                saved = next(row for row in sessions['sessions'] if row['session'] == 'restart-fixture')
                assert saved['page_id'] == page_id, saved
                pages, _ = await call('device_command', {'command':'pages','session':'restart-fixture'})
                assert any(row['page_id'] == page_id for row in pages['pages']), pages
                observation, result = await call('device_observe', {'session':'restart-fixture'})
                pictures = [item for item in result.content if item.type == 'image']
                assert pictures and observation['page_id'] == page_id, observation
                with Image.open(io.BytesIO(base64.b64decode(pictures[0].data))) as picture:
                    picture.verify()
                observations.append(observation['id'])
                acted, _ = await call('device_act', {'session':'restart-fixture',
                    'observation_id':observation['id'], 'action':{'type':'tap','x':190,'y':25}})
                assert acted['dispatched'], acted
                await call('device_input', {'serial':'restart-fixture','text':f'-mcp{phase}'})
    assert len(set(observations)) == 2, observations
    print(json.dumps({'restarts':1, 'observations':observations,'page_id':page_id}), flush=True)


if __name__ == '__main__':
    asyncio.run(asyncio.wait_for(exercise(Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]), timeout=60))
