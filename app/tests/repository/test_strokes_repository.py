import uuid

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.strokes import StrokeCreate, DEFINITION_OF_CATEGORIZATION, BASE_ADVANCE, BASE_INTERMEDIATE, BASE_BEGINNER
from app.repository.strokes_repository import StrokesRepository
from app.services.strokes_service import StrokesService
from app.utilities.exceptions import NotFoundException


async def test_create_strokes(session: AsyncSession) -> None:
    user_public_id = uuid.uuid4()
    repo = StrokesRepository(session)
    info_create = StrokeCreate(background_ground=DEFINITION_OF_CATEGORIZATION[1], backhand_volley=DEFINITION_OF_CATEGORIZATION[2])
    # test
    result = await repo.create_stroke(info_create, user_public_id)
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


async def test_get_strokes(session: AsyncSession) -> None:
    user_public_id = uuid.uuid4()
    service = StrokesService()
    repo = StrokesRepository(session)
    info_create = StrokeCreate(background_ground=DEFINITION_OF_CATEGORIZATION[1], backhand_volley=DEFINITION_OF_CATEGORIZATION[2])
    _stroke = await service.create_padel_stroke(session, info_create, user_public_id)
    # test
    result = await repo.get_strokes(user_public_id)
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


async def test_get_strokes_raises_exception_if_associated_player_not_exists(session: AsyncSession) -> None:
    user_public_id = uuid.uuid4()
    repo = StrokesRepository(session)
    # test
    # try:
    #     _result = await repo.get_strokes(user_public_id)
    #     raise AssertionError
    # # assert
    # except NotFoundException as error:
    #     assert error.detail == "Padel strokes not found."
    # except Exception:
    #     raise AssertionError
    with pytest.raises(NotFoundException ) as e:
        await repo.get_strokes(user_public_id)
    assert e.value.detail == "Padel strokes not found."



async def test_update_padel_strokes(session: AsyncSession) -> None:
    user_public_id = uuid.uuid4()
    service = StrokesService()
    repo = StrokesRepository(session)
    info_create = StrokeCreate(background_ground=DEFINITION_OF_CATEGORIZATION[1], backhand_volley=DEFINITION_OF_CATEGORIZATION[2])
    _stroke = await service.create_padel_stroke(session, info_create, user_public_id)
    update_info = StrokeCreate(background_ground=DEFINITION_OF_CATEGORIZATION[2], forehand_ground=DEFINITION_OF_CATEGORIZATION[1])
    # test
    result = await repo.update_strokes(update_info, user_public_id)
    # assert
    assert result is not None
    for field in result.__dict__:
        value = getattr(result, field, None)
        if field[0] == "_":
            continue
        if field == "backhand_volley" or field == "background_ground":
            assert value == DEFINITION_OF_CATEGORIZATION[2]
        elif field == "forehand_ground":
            assert value == DEFINITION_OF_CATEGORIZATION[1]
        elif field == "user_public_id":
            assert value == user_public_id
        else:
            assert value == DEFINITION_OF_CATEGORIZATION[0]