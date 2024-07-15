import aiohttp
import json


async def _fetch_servers() -> list:
    async with aiohttp.ClientSession() as session:
        async with session.get('https://central.spacestation14.io/hub/api/servers/') as result:
            return json.loads(await result.text())


async def find_server_data(server_address: str) -> dict | None:
    servers = await _fetch_servers()
    for server in servers:
        if server['address'] == server_address:
            return server['statusData']
    return None
