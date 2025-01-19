import uuid
from typing import Any

from fastapi import APIRouter, status

from app.models.player import PlayerCreate, PlayerPublic, PlayerUpdate
from app.services.players_service import PlayersService
from app.utilities.dependencies import SessionDep
from app.utilities.messages import PLAYERS_PUT_RESPONSES, POST_PLAYERS_RESPONSES

router = APIRouter()

service = PlayersService()


@router.post(
    "/",
    response_model=PlayerPublic,
    status_code=status.HTTP_201_CREATED,
    responses={**POST_PLAYERS_RESPONSES},  # type: ignore[dict-item]
)
async def create_player(*, session: SessionDep, player_in: PlayerCreate) -> Any:
    """
    Create new player.
    """
    return await service.create_player(session, player_in)


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
    updated_player = await service.update_player(session, user_public_id, player_in)
    return updated_player
