import uuid

from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.padel_stroke import DEFINITION_OF_CATEGORIZATION, BASE_SKILL_NEW
from app.models.player import PlayerCreate
from app.services.padel_strokes_service import PadelStrokesService
from app.services.players_service import PlayersService


async def test_create_padel_stroke_empty(session: AsyncSession) -> None:
    user_public_id = uuid.uuid4()
    service = PadelStrokesService()
    # test
    empty_stroke = await service.create_padel_stroke_empty(session, user_public_id)
    # assert
    for field in empty_stroke.__dict__:
        value = getattr(empty_stroke, field, None)
        if field[0] == "_":
            continue
        elif field == "user_public_id":
            assert value == user_public_id
        else:
            assert value == BASE_SKILL_NEW


async def test_create_and_get_padel_stroke_empty(session: AsyncSession) -> None:
    user_public_id = uuid.uuid4()
    service = PadelStrokesService()
    _ = await service.create_padel_stroke_empty(session, user_public_id)
    # test
    empty_stroke = await service.get_padel_strokes(session, user_public_id)
    # assert
    for field in empty_stroke.__dict__:
        value = getattr(empty_stroke, field, None)
        if field[0] == "_":
            continue
        elif field == "user_public_id":
            assert value == user_public_id
        else:
            assert value == DEFINITION_OF_CATEGORIZATION[0]


async def test_generate_strokes_whit_player(session: AsyncSession) -> None:
    user_public_id = uuid.uuid4()
    telegram_id = 10103030

    stroke_service = PadelStrokesService()
    player_service = PlayersService()
    player_create = PlayerCreate(user_public_id=str(user_public_id), telegram_id=telegram_id)
    # test
    _player = await player_service.create_player(session, player_create)
    empty_stroke = await stroke_service.get_padel_strokes(session, user_public_id)
    # assert
    for field in empty_stroke.__dict__:
        value = getattr(empty_stroke, field, None)
        if field[0] == "_":
            continue
        elif field == "user_public_id":
            assert value == user_public_id
        else:
            assert value == DEFINITION_OF_CATEGORIZATION[0]
