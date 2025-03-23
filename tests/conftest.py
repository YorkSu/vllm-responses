from collections.abc import AsyncIterator

import pytest
from httpx import AsyncClient
from litestar import Litestar
from litestar.testing import AsyncTestClient


pytestmark = pytest.mark.anyio


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(name="app")
def fx_app() -> Litestar:
    from vllm_responses.asgi import create_app

    return create_app()


@pytest.fixture(name="client")
async def fx_client(app: Litestar) -> AsyncIterator[AsyncClient]:
    async with AsyncTestClient(app) as client:
        yield client
