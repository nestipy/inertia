from typing import (
    AsyncGenerator,
    Union,
)

try:
    import httpx
except (ModuleNotFoundError, ImportError):
    httpx = None  # type: ignore


async def get_httpx_client() -> AsyncGenerator[Union[None, "httpx.AsyncClient"], None]:
    if not httpx:
        yield None
    async with httpx.AsyncClient() as client:
        yield client
