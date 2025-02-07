from sqlalchemy.exc import IntegrityError
from app.models.player import Player, PlayerCreate
from app.services.players_service import PlayersService
from app.services.strokes_service import StrokesService
from app.utilities.dependencies import SessionDep
from app.utilities.exceptions import NotUniqueException


class PlayersAndStrokesService:
    async def create_player(
        self, session: SessionDep, player_in: PlayerCreate
    ) -> Player:
        player = await self._create_only_player(session, player_in)
        stroke = await self._create_strokes(session, player_in)
        # All data that needs to be refreshed must be in the list
        other_for_refresh = [player, stroke]
        # This is the final function (refresh are done)
        await self._finish_transaction(session, other_for_refresh)
        return player


    async def _create_only_player(self, session: SessionDep, player_in: PlayerCreate) -> Player:
        service_player = PlayersService()
        try:
            player = await service_player.create_player(session, player_in)
            # The commit is not made because it is not the final function
            return player
        except IntegrityError:
            await self._raise_not_unique(session)
        except Exception as e:
            await session.rollback()
            raise e


    async def _create_strokes(self, session: SessionDep, player_in: PlayerCreate):
        service_strokes = StrokesService()
        try:
            stroke = await service_strokes.create_padel_stroke(session, None, player_in.user_public_id)
            # The commit is not made because it is not the final function
            return stroke
        except NotUniqueException:
            await self._raise_not_unique(session)
        except IntegrityError:
            await self._raise_not_unique(session)
        except Exception as e:
            raise e


    async def _finish_transaction(self, session: SessionDep, other_for_refresh: list):
        try:
            await session.commit()
            for item in other_for_refresh:
                await session.refresh(item)
        except IntegrityError:
            await self._raise_not_unique(session)
        except Exception as e:
            await session.rollback()
            raise e


    @staticmethod
    async def _raise_not_unique(session: SessionDep):
        await session.rollback()
        raise NotUniqueException("player")
