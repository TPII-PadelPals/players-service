import uuid
from typing import Any

from fastapi import APIRouter, status

from app.models.strokes import StrokePublic, StrokeUpdate
from app.services.strokes_service import StrokesService
from app.utilities.dependencies import SessionDep
from app.utilities.messages import STROKES_GET_RESPONSES, STROKES_PUT_RESPONSES

router = APIRouter()

service = StrokesService()


@router.put(
    "/",
    response_model=StrokePublic,
    status_code=status.HTTP_200_OK,
    responses={**STROKES_PUT_RESPONSES},  # type: ignore[dict-item]
)
async def update_stroke(
        *,
        session: SessionDep,
        user_public_id: uuid.UUID,
        stroke_in: StrokeUpdate,
) -> Any:
    """
    Update a strokes.
    """
    return await service.update_stroke(session, user_public_id, stroke_in)


@router.get(
    "/",
    response_model=StrokePublic,
    status_code=status.HTTP_200_OK,
    responses={**STROKES_GET_RESPONSES},  # type: ignore[dict-item]
)
async def get_strokes(*, session: SessionDep, user_public_id: uuid.UUID) -> Any:
    """
    Get a strokes.
    """
    return await service.get_strokes(session, user_public_id)