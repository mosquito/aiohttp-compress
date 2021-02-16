from typing import Any, Callable, Coroutine

from aiohttp import hdrs
from aiohttp.web import (
    middleware, Request, StreamResponse, Response, ContentCoding
)


HandlerType = Callable[[Any], Coroutine[Any, None, Response]]


@middleware
async def compress_middleware(
    request: Request, handler: HandlerType
) -> StreamResponse:

    accept_encoding = request.headers.get(hdrs.ACCEPT_ENCODING, "").lower()

    if ContentCoding.gzip.value in accept_encoding:
        compressor = ContentCoding.gzip.value
    elif ContentCoding.deflate.value in accept_encoding:
        compressor = ContentCoding.deflate.value
    else:
        return await handler(request)

    resp = await handler(request)
    resp.headers[hdrs.CONTENT_ENCODING] = compressor
    resp.enable_compression()
    return resp
