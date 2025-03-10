import uuid
from typing import Any

from fastapi import APIRouter, status

from app.models.player_availability import (
    PlayerAvailabilityListPublic,
    PlayerAvailabilityListUpdate,
)
from app.services.players_availability_service import PlayersAvailabilityService
from app.utilities.dependencies import SessionDep
from app.utilities.messages import PLAYERS_AVAILABILITY_PATCH_RESPONSES

router = APIRouter()


@router.patch(
    "/",
    response_model=PlayerAvailabilityListPublic,
    status_code=status.HTTP_200_OK,
    responses={**PLAYERS_AVAILABILITY_PATCH_RESPONSES},  # type: ignore[dict-item]
)
async def update_player_availability(
    *,
    session: SessionDep,
    user_public_id: uuid.UUID,
    player_availability_in: PlayerAvailabilityListUpdate,
) -> Any:
    """
    Update player availability.
    """
    player_availability_updated = (
        await PlayersAvailabilityService().update_player_availability(
            session, user_public_id, player_availability_in
        )
    )
    return player_availability_updated.to_public()
