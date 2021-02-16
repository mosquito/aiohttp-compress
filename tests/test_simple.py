from types import MappingProxyType

import pytest
from aiohttp import web, test_utils, hdrs
from aiohttp.web import json_response, Response
from aiohttp_compress import compress_middleware


DATA = MappingProxyType({str(i): i for i in range(100000)})


async def get_data(_):
    return json_response(dict(DATA))


@pytest.fixture
def aiohttp_app():
    return web.Application()


@pytest.fixture
async def client(loop, aiohttp_app):
    aiohttp_app.router.add_route("GET", "/data", get_data)

    aiohttp_app.middlewares.append(compress_middleware)

    test_server = test_utils.TestServer(aiohttp_app, port=8090)
    test_client = test_utils.TestClient(test_server)

    await test_client.start_server()

    try:
        yield test_client
    finally:
        await test_server.close()
        await test_client.close()


@pytest.mark.parametrize("compressor", ["gzip", "deflate"])
async def test_simple(compressor, client: test_utils.TestClient):
    headers = {hdrs.ACCEPT_ENCODING: compressor}

    async with client.get("/data", headers=headers) as response:
        response.raise_for_status()
        body = await response.json()
        assert compressor in response.headers[hdrs.CONTENT_ENCODING]
        assert isinstance(body, dict)
