import uuid
from typing import Any

from fastapi import APIRouter, status

from app.models.padel_stroke import PadelStrokePublic, PadelStrokeCreate, PadelStrokeUpdate
from app.services.padel_strokes_service import PadelStrokesService
from app.utilities.dependencies import SessionDep
from app.utilities.messages import PLAYERS_POST_RESPONSES, PLAYERS_PUT_RESPONSES

router = APIRouter()

service = PadelStrokesService()


# @router.post(
#     "/",
#     response_model=PadelStrokePublic,
#     status_code=status.HTTP_201_CREATED,
#     responses={**PLAYERS_POST_RESPONSES},  # type: ignore[dict-item]
# )
# async def create_padel_stroke(*, session: SessionDep, padel_stroke_in: PadelStrokeCreate, user_public_id: uuid.UUID) -> Any:
#     """
#     Create new player.
#     """
#     return await service.create_padel_stroke(session, padel_stroke_in)


@router.put(
    "/",
    response_model=PadelStrokePublic,
    status_code=status.HTTP_200_OK,
    responses={**PLAYERS_PUT_RESPONSES},  # type: ignore[dict-item]
)
async def update_padel_stroke(
        *,
        session: SessionDep,
        user_public_id: uuid.UUID,
        padel_stroke_in: PadelStrokeUpdate,
) -> Any:
    """
    Update a player.
    """
    return await service.update_padel_stroke(session, user_public_id, padel_stroke_in)





@router.get(
    "/",
    response_model=PadelStrokePublic,
    status_code=status.HTTP_200_OK,
    responses={**PLAYERS_PUT_RESPONSES},  # type: ignore[dict-item]
)
async def get_padel_strokes(*, session: SessionDep, user_public_id: uuid.UUID):
    """

    """
    return await service.get_padel_strokes(session, user_public_id)