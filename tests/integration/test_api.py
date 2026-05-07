import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_health_endpoint(client: AsyncClient) -> None:
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.anyio
async def test_analyze_endpoint(client: AsyncClient) -> None:
    response = await client.post(
        "/analyze",
        json={
            "product_id": "B001234",
            "review_text": "The price is good but the packaging was damaged.",
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["product_id"] == "B001234"
    assert body["aspects"]["price"] == "positive"
    assert body["aspects"]["packaging"] == "negative"
    assert "complaint" in body["tags"]


@pytest.mark.anyio
async def test_analyze_endpoint_rejects_blank_review(client: AsyncClient) -> None:
    response = await client.post("/analyze", json={"review_text": "   "})

    assert response.status_code == 422
