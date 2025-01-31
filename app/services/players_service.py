import copy
import uuid

from app.models.player import Player, PlayerCreate, PlayerUpdate
from app.repository.players_repository import PlayersRepository
from app.services.padel_strokes_service import PadelStrokesService
from app.utilities.dependencies import SessionDep
from app.utilities.exceptions import NotUniqueException


class PlayersService:
    auxiliary_service_strokes = PadelStrokesService()

    async def create_player(
        self, session: SessionDep, player_in: PlayerCreate
    ) -> Player:
        repo = PlayersRepository(session)
        try:
            _stroke = await self.auxiliary_service_strokes.create_padel_stroke_empty(session, player_in.user_public_id)
        except NotUniqueException:
            raise NotUniqueException("player")
        except Exception as e:
            raise e
        player = await repo.create_player(player_in)
        return player

    async def update_player(
        self, session: SessionDep, user_public_id: uuid.UUID, player_in: PlayerUpdate
    ) -> Player:
        repo = PlayersRepository(session)
        return await repo.update_player(user_public_id, player_in)
