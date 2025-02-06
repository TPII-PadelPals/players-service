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
        await self._create_strokes(session, player_in)
        player = await self._create_player(session, player_in)
        return player

    async def _create_player(self, session: SessionDep, player_in: PlayerCreate) -> Player:
        service_player = PlayersService()
        try:
            player = await service_player.create_player(session, player_in)
            session.commit()
            return player
        except IntegrityError:
            self._raise_not_unique(session)
        except Exception as e:
            session.rollback()
            raise e

    async def _create_strokes(self, session: SessionDep, player_in: PlayerCreate):
        service_strokes = StrokesService()
        try:
            _stroke = await service_strokes.create_padel_stroke(session, None, player_in.user_public_id)
        except NotUniqueException:
            self._raise_not_unique(session)
        except IntegrityError:
            self._raise_not_unique(session)
        except Exception as e:
            raise e

    @staticmethod
    def _raise_not_unique(session: SessionDep):
        session.rollback()
        raise NotUniqueException("player")