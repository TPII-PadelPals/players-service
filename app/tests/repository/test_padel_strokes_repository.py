import uuid

from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.padel_stroke import PadelStrokeCreate, DEFINITION_OF_CATEGORIZATION, BASE_ADVANCE, BASE_INTERMEDIATE, \
    BASE_BEGINNER
from app.repository.padel_strokes_repository import PadelStrokesRepository
from app.services.padel_strokes_service import PadelStrokesService


async def test_create_padel_strokes(session: AsyncSession) -> None:
    user_public_id = uuid.uuid4()
    repo = PadelStrokesRepository(session)
    info_create = PadelStrokeCreate(background_ground=DEFINITION_OF_CATEGORIZATION[1], backhand_volley=DEFINITION_OF_CATEGORIZATION[2])
    # test
    result = await repo.create_padel_strokes(info_create, user_public_id)
    # assert
    for field in result.__dict__:
        value = getattr(result, field, None)
        if field[0] == "_":
            continue
        if field == "backhand_volley":
            assert value == BASE_ADVANCE
        elif field == "background_ground":
            assert value == BASE_INTERMEDIATE
        elif field == "user_public_id":
            assert value == user_public_id
        else:
            assert value == BASE_BEGINNER


async def test_get_padel_strokes(session: AsyncSession) -> None:
    user_public_id = uuid.uuid4()
    service = PadelStrokesService()
    repo = PadelStrokesRepository(session)
    info_create = PadelStrokeCreate(background_ground=DEFINITION_OF_CATEGORIZATION[1], backhand_volley=DEFINITION_OF_CATEGORIZATION[2])
    _stroke = await service.create_padel_stroke(session, info_create, user_public_id)
    # test
    result = await repo.get_padel_strokes(user_public_id)
    # assert
    assert result is not None
    for field in result.__dict__:
        value = getattr(result, field, None)
        if field[0] == "_":
            continue
        if field == "backhand_volley":
            assert value == DEFINITION_OF_CATEGORIZATION[2]
        elif field == "background_ground":
            assert value == DEFINITION_OF_CATEGORIZATION[1]
        elif field == "user_public_id":
            assert value == user_public_id
        else:
            assert value == DEFINITION_OF_CATEGORIZATION[0]