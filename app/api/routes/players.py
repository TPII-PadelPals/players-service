import uuid
from typing import Any

from fastapi import APIRouter, status

from app.models.player import PlayerCreate, PlayerPublic, PlayerUpdate
from app.services.players_and_strokes_service import PlayersAndStrokesService
from app.services.players_service import PlayersService
from app.utilities.dependencies import SessionDep
from app.utilities.messages import (
    PLAYERS_GET_RESPONSES,
    PLAYERS_PATCH_RESPONSES,
    PLAYERS_POST_RESPONSES,
)

router = APIRouter()

service = PlayersService()


@router.post(
    "/",
    response_model=PlayerPublic,
    status_code=status.HTTP_201_CREATED,
    responses={**PLAYERS_POST_RESPONSES},  # type: ignore[dict-item]
)
async def create_player(*, session: SessionDep, player_in: PlayerCreate) -> Any:
    """
    Create new player.
    """
    service_aux = PlayersAndStrokesService()
    return await service_aux.create_player(session, player_in)


@router.patch(
    "/",
    response_model=PlayerPublic,
    status_code=status.HTTP_200_OK,
    responses={**PLAYERS_PATCH_RESPONSES},  # type: ignore[dict-item]
)
async def update_player(
    *,
    session: SessionDep,
    user_public_id: uuid.UUID,
    player_in: PlayerUpdate,
) -> Any:
    """
    Update a player.
    """
    return await service.update_player(session, user_public_id, player_in)


@router.get(
    "/{user_public_id}",
    response_model=PlayerPublic,
    status_code=status.HTTP_200_OK,
    responses={**PLAYERS_GET_RESPONSES},  # type: ignore[dict-item]
)
async def read_player(session: SessionDep, user_public_id: uuid.UUID) -> Any:
    """
    Get Player by Public ID.
    """
    return await service.read_player(session, user_public_id)
