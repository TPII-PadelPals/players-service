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
        stroke = await self._create_strokes(session, player_in)
        # All data that needs to be refreshed must be in the list
        other_for_refresh = [stroke]
        # This is the final function (commit and refresh are done)
        player = await self._create_only_player_and_finish(session, player_in, other_for_refresh)
        return player

    async def _create_only_player_and_finish(self, session: SessionDep, player_in: PlayerCreate, other_for_refresh: list) -> Player:
        service_player = PlayersService()
        try:
            player = await service_player.create_player(session, player_in)
            print("ASDASDASD OK player")
            await session.commit()
            print("ASDASDASD OK commit")
            await session.refresh(player)
            for item in other_for_refresh:
                await session.refresh(item)
            print("ASDASDASD OK refresh")
            return player
        except IntegrityError:
            self._raise_not_unique(session)
        except Exception as e:
            print("ASDASDASD ERROR: ", str(e))
            await session.rollback()
            raise e

    async def _create_strokes(self, session: SessionDep, player_in: PlayerCreate):
        service_strokes = StrokesService()
        try:
            stroke = await service_strokes.create_padel_stroke(session, None, player_in.user_public_id)
            # The commit is not made because it is not the final function
            print("ASDASDASD OK stroke")
            return stroke
        except NotUniqueException:
            self._raise_not_unique(session)
        except IntegrityError:
            self._raise_not_unique(session)
        except Exception as e:
            print("ASDASDASD ERROR IN CREATING STROKES")
            raise e

    @staticmethod
    def _raise_not_unique(session: SessionDep):
        print("ASDASDASD NOT UNIQUE")
        session.rollback()
        raise NotUniqueException("player")