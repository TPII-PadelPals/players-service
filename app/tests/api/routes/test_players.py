import uuid
from typing import Any

from httpx import AsyncClient

from app.core.config import settings
from app.services.google_service import GoogleService
from app.services.players_availability_service import PlayersAvailabilityService
from app.tests.utils.players import mock_raise_not_unique_exception
from app.utilities.exceptions import NotUniqueException


async def test_create_player(
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

    response_detail = response.json().get("detail")
    expected_detail = NotUniqueException("player").detail

    assert (
        response_detail == expected_detail
    ), f"Expected '{expected_detail}' but got '{response_detail}'"


async def test_create_player_when_player_availability_service_raise_exception_responds_409(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    monkeypatch.setattr(
        PlayersAvailabilityService,
        "create_player_availability",
        mock_raise_not_unique_exception("player availability"),
    )

    user_public_id = str(uuid.uuid4())

    data = {"user_public_id": user_public_id, "telegram_id": 11112222}
    response = await async_client.post(
        f"{settings.API_V1_STR}/players/", headers=x_api_key_header, json=data
    )

    assert response.status_code == 409

    response_detail = response.json().get("detail")
    expected_detail = NotUniqueException("player availability").detail

    assert (
        response_detail == expected_detail
    ), f"Expected '{expected_detail}' but got '{response_detail}'"

    response = await async_client.get(
        f"{settings.API_V1_STR}/players/{user_public_id}",
        headers=x_api_key_header,
        params={"user_public_id": str(user_public_id)},
    )
    assert response.status_code == 404

    content = response.json()
    assert content["detail"] == "Player not found."


async def test_update_player_no_address(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    user_public_id = str(uuid.uuid4())
    telegram_id = 10103030

    post_data = {"user_public_id": user_public_id, "telegram_id": telegram_id}
    response_post = await async_client.post(
        f"{settings.API_V1_STR}/players/", headers=x_api_key_header, json=post_data
    )
    created_player = response_post.json()

    patch_data = {
        "time_availability": 5,
        "zone_km": 10,
        "latitude": 0.10,
        "longitude": 0.20,
    }
    response = await async_client.patch(
        f"{settings.API_V1_STR}/players/",
        headers=x_api_key_header,
        json=patch_data,
        params={"user_public_id": created_player["user_public_id"]},
    )

    assert response.status_code == 200
    content = response.json()

    assert content["user_public_id"] == created_player["user_public_id"]
    assert content["telegram_id"] == created_player["telegram_id"]
    assert content["time_availability"] == patch_data["time_availability"]
    assert content["zone_km"] == patch_data["zone_km"]
    assert content["zone_location"] is None
    assert content["latitude"] == patch_data["latitude"]
    assert content["longitude"] == patch_data["longitude"]


async def test_update_player_with_address(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    GET_COORDS_RESULT = (0.4, 0.3)

    async def mock_get_coordinates(_self: Any, _: str) -> tuple[float, float]:
        return GET_COORDS_RESULT

    monkeypatch.setattr(GoogleService, "get_coordinates", mock_get_coordinates)

    user_public_id = str(uuid.uuid4())
    telegram_id = 10103030

    post_data = {"user_public_id": user_public_id, "telegram_id": telegram_id}
    response_post = await async_client.post(
        f"{settings.API_V1_STR}/players/", headers=x_api_key_header, json=post_data
    )
    created_player = response_post.json()

    patch_data = {
        "time_availability": 5,
        "zone_km": 10,
        "zone_location": "Paseo Colón 850",
    }
    response = await async_client.patch(
        f"{settings.API_V1_STR}/players/",
        headers=x_api_key_header,
        json=patch_data,
        params={"user_public_id": created_player["user_public_id"]},
    )

    assert response.status_code == 200
    content = response.json()

    assert content["user_public_id"] == created_player["user_public_id"]
    assert content["telegram_id"] == created_player["telegram_id"]
    assert content["time_availability"] == patch_data["time_availability"]
    assert content["zone_km"] == patch_data["zone_km"]
    assert content["zone_location"] == patch_data["zone_location"]
    assert content["latitude"] == GET_COORDS_RESULT[1]
    assert content["longitude"] == GET_COORDS_RESULT[0]


async def test_update_player_not_found_returns_responds_404(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    patch_data = {"time_availability": 5}
    response = await async_client.patch(
        f"{settings.API_V1_STR}/players/",
        headers=x_api_key_header,
        json=patch_data,
        params={"user_public_id": str(uuid.uuid4())},
    )

    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Player not found."


async def test_update_player_with_time_availability_more_than_seven_responds_422(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    user_public_id = str(uuid.uuid4())
    telegram_id = 10103030

    post_data = {"user_public_id": user_public_id, "telegram_id": telegram_id}
    response_post = await async_client.post(
        f"{settings.API_V1_STR}/players/", headers=x_api_key_header, json=post_data
    )
    _created_player = response_post.json()

    patch_data = {"time_availability": 8}
    response = await async_client.patch(
        f"{settings.API_V1_STR}/players/",
        headers=x_api_key_header,
        json=patch_data,
        params={"user_public_id": user_public_id},
    )

    assert response.status_code == 422
    content = response.json()
    assert content["detail"][0]["loc"] == ["body", "time_availability"]
    assert content["detail"][0]["msg"] == "Input should be less than or equal to 7"


async def test_update_player_with_time_availability_less_than_1_responds_422(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    user_public_id = str(uuid.uuid4())
    telegram_id = 10103030

    post_data = {"user_public_id": user_public_id, "telegram_id": telegram_id}
    response_post = await async_client.post(
        f"{settings.API_V1_STR}/players/", headers=x_api_key_header, json=post_data
    )
    _created_player = response_post.json()

    patch_data = {"time_availability": 0}
    response = await async_client.patch(
        f"{settings.API_V1_STR}/players/",
        headers=x_api_key_header,
        json=patch_data,
        params={"user_public_id": user_public_id},
    )

    assert response.status_code == 422
    content = response.json()
    assert content["detail"][0]["loc"] == ["body", "time_availability"]
    assert content["detail"][0]["msg"] == "Input should be greater than or equal to 1"
