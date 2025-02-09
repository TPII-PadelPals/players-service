import uuid
from typing import Any

from fastapi import APIRouter, status

from app.models.player import PlayerCreate, PlayerPublic, PlayerUpdate
from app.models.player_availability import (
    PlayerAvailabilityPublic,
)
from app.services.players_availability_service import PlayersAvailabilityService
from app.services.players_service import PlayersService
from app.utilities.dependencies import SessionDep
from app.utilities.messages import (
    PLAYERS_AVAILABILITY_POST_RESPONSES,
    PLAYERS_GET_RESPONSES,
    PLAYERS_POST_RESPONSES,
    PLAYERS_PUT_RESPONSES,
)

router = APIRouter()

service = PlayersService()
player_availability_service = PlayersAvailabilityService()


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
    player = await service.create_player(session, player_in)
    await player_availability_service.create_player_availability(
        session, player_in.user_public_id
    )
    await session.commit()
    await session.refresh(player)
    return player


@router.put(
    "/",
    response_model=PlayerPublic,
    status_code=status.HTTP_200_OK,
    responses={**PLAYERS_PUT_RESPONSES},  # type: ignore[dict-item]
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
async def read_player(session: SessionDep, user_public_id: uuid.UUID) -> PlayerPublic:
    """
    Get Player by Public ID.
    """
    return await service.read_player(session, user_public_id)


@router.post(
    "/{user_public_id}/availability",
    response_model=PlayerAvailabilityPublic,
    status_code=status.HTTP_201_CREATED,
    responses={**PLAYERS_AVAILABILITY_POST_RESPONSES},  # type: ignore[dict-item]
)
async def create_player_availability(
    *,
    session: SessionDep,
    user_public_id: uuid.UUID,
) -> Any:
    """
    Create new player availability.
    """
    return await player_availability_service.create_player_availability(
        session, user_public_id
    )
