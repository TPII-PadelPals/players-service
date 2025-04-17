from typing import Any

from sqlalchemy.exc import IntegrityError

from app.models.player import Player, PlayerCreate
from app.services.players_availability_service import PlayersAvailabilityService
from app.services.players_service import PlayersService
from app.services.strokes_service import StrokesService
from app.utilities.dependencies import SessionDep
from app.utilities.exceptions import NotUniqueException


class PlayerCreationService:
    def __init__(
        self,
        players_service: PlayersService,
        strokes_service: StrokesService,
        player_availability_service: PlayersAvailabilityService,
    ):
        self.players_service = players_service
        self.strokes_service = strokes_service
        self.player_availability_service = player_availability_service

    async def create_player(
        self, session: SessionDep, player_in: PlayerCreate
    ) -> Player:
        try:
            player = await self.players_service.create_player(session, player_in)
            strokes = await self.strokes_service.create_strokes(
                session, stroke_in=None, user_public_id=player_in.user_public_id
            )
            player_availability = (
                await self.player_availability_service.create_player_availability(
                    session, player.user_public_id
                )
            )

            player_availabilities = player_availability.available_days
            items_to_refresh = [player, strokes] + player_availabilities

            await self._finish_transaction(session, items_to_refresh)
            return player
        except IntegrityError:
            await session.rollback()
            raise NotUniqueException("player")
        except Exception as e:
            await session.rollback()
            raise e

    async def _finish_transaction(
        self, session: SessionDep, other_for_refresh: list[Any]
    ) -> None:
        await session.commit()
        for item in other_for_refresh:
            await session.refresh(item)
