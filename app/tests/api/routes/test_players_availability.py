import uuid

from httpx import AsyncClient

from app.core.config import settings
from app.models.player_availability import WeekDay


async def test_update_player_availability_days(
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
        "available_days": [
            {"week_day": WeekDay.MONDAY.value, "is_available": True},
            {"week_day": WeekDay.THURSDAY.value, "is_available": True},
        ]
    }

    response = await async_client.patch(
        f"{settings.API_V1_STR}/players/{user_public_id}/availability/",
        headers=x_api_key_header,
        json=patch_data,
        params={"user_public_id": created_player["user_public_id"]},
    )

    assert response.status_code == 200
    content = response.json()

    assert content["user_public_id"] == created_player["user_public_id"]
    assert len(content["available_days"]) == 2

    expected_available_days = {WeekDay.MONDAY.value, WeekDay.THURSDAY.value}
    received_available_days = {
        player_availability["week_day"]
        for player_availability in content["available_days"]
        if player_availability["is_available"]
    }

    assert (
        received_available_days == expected_available_days
    ), f"Expected {expected_available_days}, but got {received_available_days}"


async def test_update_player_availability_not_found_returns_responds_404(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    not_found_user_p_id = str(uuid.uuid4())

    patch_data = {
        "available_days": [
            {"week_day": WeekDay.MONDAY.value, "is_available": True},
            {"week_day": WeekDay.THURSDAY.value, "is_available": True},
        ]
    }

    response = await async_client.patch(
        f"{settings.API_V1_STR}/players/{not_found_user_p_id}/availability/",
        headers=x_api_key_header,
        json=patch_data,
        params={"user_public_id": not_found_user_p_id},
    )

    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Player availability not found."
