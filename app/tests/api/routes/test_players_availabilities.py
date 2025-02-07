import uuid

from httpx import AsyncClient

from app.core.config import settings
from app.utilities.exceptions import NotUniqueException


async def test_create_player_available_days(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    user_public_id = str(uuid.uuid4())
    expected_player_availabilities = [
        {"user_public_id": user_public_id, "week_day": 1, "is_available": False},
        {"user_public_id": user_public_id, "week_day": 2, "is_available": False},
        {"user_public_id": user_public_id, "week_day": 3, "is_available": False},
        {"user_public_id": user_public_id, "week_day": 4, "is_available": False},
        {"user_public_id": user_public_id, "week_day": 5, "is_available": False},
        {"user_public_id": user_public_id, "week_day": 6, "is_available": False},
        {"user_public_id": user_public_id, "week_day": 7, "is_available": False},
    ]

    response = await async_client.post(
        f"{settings.API_V1_STR}/players/{user_public_id}/availability",
        headers=x_api_key_header,
    )
    assert response.status_code == 201
    content = response.json()

    assert len(content["available_days"]) == len(expected_player_availabilities)

    actual_availabilities = [
        {
            "user_public_id": day["user_public_id"],
            "week_day": day["week_day"],
            "is_available": day["is_available"],
        }
        for day in content["available_days"]
    ]

    assert (
        actual_availabilities == expected_player_availabilities
    ), f"Expected: {expected_player_availabilities}, but got: {actual_availabilities}"


async def test_create_player_available_days_user_public_id_already_exists_responds_409(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    user_public_id = str(uuid.uuid4())

    await async_client.post(
        f"{settings.API_V1_STR}/players/{user_public_id}/availability",
        headers=x_api_key_header,
    )

    response = await async_client.post(
        f"{settings.API_V1_STR}/players/{user_public_id}/availability",
        headers=x_api_key_header,
    )

    assert response.status_code == 409

    response_detail = response.json().get("detail")
    expected_detail = NotUniqueException("player availability").detail

    assert (
        response_detail == expected_detail
    ), f"Expected '{expected_detail}' but got '{response_detail}'"
