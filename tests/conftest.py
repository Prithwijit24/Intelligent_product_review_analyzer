import pytest
from httpx import ASGITransport, AsyncClient

from review_analyzer.api.dependencies import get_analyzer
from review_analyzer.api.main import app
from review_analyzer.pipeline.analyzer import ReviewAnalyzer


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(autouse=True)
def analyzer_override() -> None:
    async def override() -> ReviewAnalyzer:
        return ReviewAnalyzer()

    app.dependency_overrides[get_analyzer] = override
    yield
    app.dependency_overrides.clear()


@pytest.fixture
async def client() -> AsyncClient:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client
