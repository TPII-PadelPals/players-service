import uuid

from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.player import PlayerCreate
from app.services.players_availability_service import PlayersAvailabilityService
from app.services.players_creation_service import PlayerCreationService
from app.services.players_service import PlayersService
from app.services.strokes_service import StrokesService
from app.tests.utils.utils import create_player


async def test_create_strokes_defaults_to_beginner_base_level(
    session: AsyncSession,
) -> None:
    user_public_id = uuid.uuid4()
    service = StrokesService()
    player = await create_player(session, user_public_id)
    # test
    info_strokes = None
    stroke = await service.create_strokes(session, info_strokes, user_public_id)
    await session.commit()
    await session.refresh(player)
    await session.refresh(stroke)
    # assert
    for field in stroke.__dict__:
        value = getattr(stroke, field, None)
        if field[0] == "_" or field == "id":
            continue
        elif field == "user_public_id":
            assert value == user_public_id
        else:
            assert value == 1.0


async def test_create_and_get_strokes(session: AsyncSession) -> None:
    user_public_id = uuid.uuid4()
    service = StrokesService()
    info_strokes = None
    player = await create_player(session, user_public_id)
    stroke_created = await service.create_strokes(session, info_strokes, user_public_id)
    await session.commit()
    await session.refresh(player)
    await session.refresh(stroke_created)
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
            assert value == 1.0


async def test_generate_strokes_whit_player(session: AsyncSession) -> None:
    user_public_id = uuid.uuid4()

    strokes_service = StrokesService()
    players_creation_service = PlayerCreationService(
        players_service=PlayersService(),
        strokes_service=StrokesService(),
        player_availability_service=PlayersAvailabilityService(),
    )
    player_create = PlayerCreate(user_public_id=str(user_public_id))
    # test
    _player = await players_creation_service.create_player(session, player_create)
    strokes = await strokes_service.get_strokes(session, user_public_id)
    # assert
    for field in strokes.__dict__:
        value = getattr(strokes, field, None)
        if field[0] == "_":
            continue
        elif field == "user_public_id":
            assert value == user_public_id
        else:
            assert value == 1.0
