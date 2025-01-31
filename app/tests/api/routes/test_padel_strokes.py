import uuid

from httpx import AsyncClient

from app.core.config import settings
from app.models.padel_stroke import DEFINITION_OF_CATEGORIZATION


async def test_create_player_create_stroke_associated(
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
        f"{settings.API_V1_STR}/padel-strokes/", headers=x_api_key_header, params={"user_public_id": user_public_id_str},
    )
    # assert
    assert response_stroke.status_code == 200
    content = response_stroke.json()
    print("ASDASDASD: ", content, type(content))
    assert content["user_public_id"] == user_public_id_str
    for field, value in content.items():
        if field == "user_public_id":
            assert value == user_public_id_str
        else:
            assert value == DEFINITION_OF_CATEGORIZATION[0]

