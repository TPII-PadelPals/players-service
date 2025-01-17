import uuid

from httpx import AsyncClient

from app.core.config import settings


async def test_create_user(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    user_public_id = str(uuid.uuid4())
    telegram_id = 10103030

    data = {"user_public_id": user_public_id, "telegram_id": telegram_id}

    response = await async_client.post(
        f"{settings.API_V1_STR}/players/", headers=x_api_key_header, json=data
    )
    assert response.status_code == 201
    content = response.json()

    assert content["user_public_id"] == user_public_id
    assert content["telegram_id"] == telegram_id
    assert content["zone_km"] is None
    assert content["zone_location"] is None
    assert content["latitude"] is None
    assert content["longitude"] is None
    assert content["time_availability"] is None


async def test_create_player_user_public_id_already_exists_responds_409(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    user_public_id = str(uuid.uuid4())

    data = {"user_public_id": user_public_id, "telegram_id": 11112222}
    await async_client.post(
        f"{settings.API_V1_STR}/players/", headers=x_api_key_header, json=data
    )

    data = {"user_public_id": user_public_id, "telegram_id": 33334444}
    response = await async_client.post(
        f"{settings.API_V1_STR}/players/", headers=x_api_key_header, json=data
    )
    assert response.status_code == 409
    content = response.json()
    assert content["detail"] == "User public id already exists."
