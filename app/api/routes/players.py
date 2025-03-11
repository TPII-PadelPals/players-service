import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Query, status

from app.api.routes import players_availability
from app.models.player import (
    PlayerCreate,
    PlayerFilters,
    PlayerListPublic,
    PlayerPublic,
    PlayerUpdate,
)
from app.services.players_availability_service import PlayersAvailabilityService
from app.services.players_creation_service import PlayerCreationService
from app.services.players_service import PlayersService
from app.services.strokes_service import StrokesService
from app.utilities.dependencies import SessionDep
from app.utilities.messages import (
    PLAYERS_GET_RESPONSES,
    PLAYERS_PATCH_RESPONSES,
    PLAYERS_POST_RESPONSES,
)

router = APIRouter()
router.include_router(
    players_availability.router, prefix="/{user_public_id}/availability"
)

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
    service_aux = PlayerCreationService(
        players_service=PlayersService(),
        strokes_service=StrokesService(),
        player_availability_service=PlayersAvailabilityService(),
    )
    player = await service_aux.create_player(session, player_in)
    return player


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


@router.get("/", response_model=PlayerListPublic, status_code=status.HTTP_200_OK)
async def filter_players(
    session: SessionDep, player_filters: Annotated[PlayerFilters, Query()]
) -> Any:
    """
    Get Player/s by filter options.
    """
    player_list = await service.filter_players(session, player_filters)
    return player_list.to_public()
