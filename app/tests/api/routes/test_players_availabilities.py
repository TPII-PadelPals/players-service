import uuid

from httpx import AsyncClient

from app.core.config import settings

# from app.utilities.exceptions import NotUniqueException


async def test_create_player_available_days(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    user_public_id = str(uuid.uuid4())
    available_days = [1, 2, 3]

    data = {"available_days": available_days}

    response = await async_client.post(
        f"{settings.API_V1_STR}/players/{user_public_id}/availability",
        headers=x_api_key_header,
        json=data,
    )
    assert response.status_code == 201
    content = response.json()

    assert content["user_public_id"] == user_public_id
    assert content["available_days"] == available_days
