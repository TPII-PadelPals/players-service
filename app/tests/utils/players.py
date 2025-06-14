from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.player import Player, PlayerCreate, PlayerUpdate
from app.models.player_availability import (
    PlayerAvailabilityBase,
    PlayerAvailabilityListUpdate,
)
from app.models.strokes import StrokeBase, StrokeUpdate
from app.services.players_availability_service import PlayersAvailabilityService
from app.services.players_creation_service import PlayerCreationService
from app.services.players_service import PlayersService
from app.services.strokes_service import StrokesService
from app.utilities.dependencies import SessionDep
from app.utilities.exceptions import NotUniqueException


async def mock_create_player_availability_raise_not_unique_exception(
    _self: Any, _session: AsyncSession, _user_public_id: str
) -> None:
    mock_raise_not_unique_exception("player availability")


def mock_raise_not_unique_exception(class_name: str) -> None:
    raise NotUniqueException(class_name)


class PlayerCreationExtendedService(PlayerCreationService):
    def __init__(self) -> None:
        super().__init__(
            PlayersService(), StrokesService(), PlayersAvailabilityService()
        )

    async def create_player_extended(
        self, session: SessionDep, player_data: dict[str, Any]
    ) -> Player:
        user_public_id = player_data["user_public_id"]
        player = await self.create_player(session, PlayerCreate(**player_data))
        player = await self.players_service.update_player(
            session, user_public_id, PlayerUpdate(**player_data)
        )
        if "available_days" in player_data:
            available_days = PlayerAvailabilityListUpdate(
                available_days=[
                    PlayerAvailabilityBase(week_day=day, is_available=True)
                    for day in player_data["available_days"]
                ]
            )
            await self.player_availability_service.update_player_availability(
                session, user_public_id, available_days
            )
        if "strokes" in player_data:
            strokes_skills = dict(
                zip(
                    StrokeBase().model_dump().keys(),
                    player_data["strokes"],
                    strict=False,
                )
            )
            await self.strokes_service.update_strokes(
                session, user_public_id, StrokeUpdate(**strokes_skills)
            )
        return player
