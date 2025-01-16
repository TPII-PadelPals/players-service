from typing import Any

from fastapi import APIRouter, status

from app.models.player import PlayerCreate, PlayerPublic
from app.services.players_service import PlayersService
from app.utilities.dependencies import SessionDep
from app.utilities.messages import POST_PLAYERS_RESPONSES

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
