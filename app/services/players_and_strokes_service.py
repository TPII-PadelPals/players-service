from typing import Any

from sqlalchemy.exc import IntegrityError

from app.models.player import Player, PlayerCreate
from app.models.strokes import Stroke
from app.services.players_service import PlayersService
from app.services.strokes_service import StrokesService
from app.utilities.dependencies import SessionDep
from app.utilities.exceptions import NotUniqueException


class PlayersAndStrokesService:
    async def create_player(
        self, session: SessionDep, player_in: PlayerCreate
    ) -> Player:
        try:
            player = await self._create_player(session, player_in)
            strokes = await self._create_strokes(session, player_in)
            items_to_refresh = [player, strokes]
            await self._finish_transaction(session, items_to_refresh)
            return player
        except IntegrityError:
            await session.rollback()
            raise NotUniqueException("player")
        except Exception as e:
            await session.rollback()
            raise e

    async def _create_player(
        self, session: SessionDep, player_in: PlayerCreate
    ) -> Player:
        service_player = PlayersService()
        player = await service_player.create_player(session, player_in)
        return player

    async def _create_strokes(
        self, session: SessionDep, player_in: PlayerCreate
    ) -> Stroke:
        service_strokes = StrokesService()
        stroke = await service_strokes.create_strokes(
            session, None, player_in.user_public_id
        )
        return stroke

    async def _finish_transaction(
        self, session: SessionDep, other_for_refresh: list[Any]
    ) -> None:
        await session.commit()
        for item in other_for_refresh:
            await session.refresh(item)
