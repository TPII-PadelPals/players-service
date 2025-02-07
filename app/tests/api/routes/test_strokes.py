import uuid

from httpx import AsyncClient

from app.core.config import settings


async def test_create_player_create_strokes_associated(
        async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    user_public_id = uuid.uuid4()
    user_public_id_str = str(user_public_id)
    telegram_id = 10103030

    data_player = {"user_public_id": user_public_id_str, "telegram_id": telegram_id}

    response_player = await async_client.post(
        f"{settings.API_V1_STR}/players/", headers=x_api_key_header, json=data_player
    )
    # If the test fails it has no meaning
    assert response_player.status_code == 201

    # test
    response_stroke = await async_client.get(
        f"{settings.API_V1_STR}/strokes/", headers=x_api_key_header, params={"user_public_id": user_public_id_str},
    )
    # assert
    assert response_stroke.status_code == 200
    content = response_stroke.json()
    assert content["user_public_id"] == user_public_id_str
    for field, value in content.items():
        if field == "user_public_id":
            assert value == user_public_id_str
        else:
            assert value == 1.0

async def test_update_strokes(
        async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    user_public_id = uuid.uuid4()
    user_public_id_str = str(user_public_id)
    telegram_id = 10103030

    data_player = {"user_public_id": user_public_id_str, "telegram_id": telegram_id}

    response_player = await async_client.post(
        f"{settings.API_V1_STR}/players/", headers=x_api_key_header, json=data_player
    )
    # If the test fails it has no meaning
    assert response_player.status_code == 201

    change_intermediate = ("background_ground", "forehand_back_wall", "backhand_back_wall")
    change_advance = ("forehand_volley", "backhand_volley")
    data = {
        "background_ground": 2.0,
        "forehand_back_wall": 2.0,
        "backhand_back_wall": 2.0,
        "forehand_volley": 3.0,
        "backhand_volley": 3.0,
    }
    # test
    response = await async_client.put(
        f"{settings.API_V1_STR}/strokes/", headers=x_api_key_header, params={"user_public_id": user_public_id_str}, json=data
    )
    # assert
    assert response.status_code == 200
    content = response.json()
    assert content["user_public_id"] == user_public_id_str
    for field, value in content.items():
        if field == "user_public_id":
            assert value == user_public_id_str
        elif field in change_intermediate:
            assert value == 2.0
        elif field in change_advance:
            assert value == 3.0
        else:
            assert value == 1.0
