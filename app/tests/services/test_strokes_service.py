import uuid

from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.strokes import DEFINITION_OF_CATEGORIZATION, BASE_SKILL_NEW
from app.models.player import PlayerCreate
from app.services.strokes_service import StrokesService
from app.services.players_service import PlayersService


async def test_create_strokes_defaults_to_beginner_base_level(session: AsyncSession) -> None:
    user_public_id = uuid.uuid4()
    service = StrokesService()
    # test
    info_strokes = None
    stroke = await service.create_padel_stroke(session, info_strokes, user_public_id)
    # assert
    for field in stroke.__dict__:
        value = getattr(stroke, field, None)
        if field[0] == "_":
            continue
        elif field == "user_public_id":
            assert value == user_public_id
        else:
            assert value == BASE_SKILL_NEW


async def test_create_and_get_strokes(session: AsyncSession) -> None:
    user_public_id = uuid.uuid4()
    service = StrokesService()
    info_strokes = None
    _ = await service.create_padel_stroke(session, info_strokes, user_public_id)
    # test
    stroke = await service.get_strokes(session, user_public_id)
    # assert
    for field in stroke.__dict__:
        value = getattr(stroke, field, None)
        if field[0] == "_":
            continue
        elif field == "user_public_id":
            assert value == user_public_id
        else:
            assert value == DEFINITION_OF_CATEGORIZATION[0]


async def test_generate_strokes_whit_player(session: AsyncSession) -> None:
    user_public_id = uuid.uuid4()
    telegram_id = 10103030

    strokes_service = StrokesService()
    player_service = PlayersService()
    player_create = PlayerCreate(user_public_id=str(user_public_id), telegram_id=telegram_id)
    # test
    _player = await player_service.create_player(session, player_create)
    strokes = await strokes_service.get_strokes(session, user_public_id)
    # assert
    for field in strokes.__dict__:
        value = getattr(strokes, field, None)
        if field[0] == "_":
            continue
        elif field == "user_public_id":
            assert value == user_public_id
        else:
            assert value == DEFINITION_OF_CATEGORIZATION[0]
