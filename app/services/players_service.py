from uuid import UUID

from app.models.player import Player, PlayerCreate, PlayerUpdate
from app.repository.players_repository import PlayersRepository
from app.utilities.dependencies import SessionDep


class PlayersService:
    async def create_player(
        self, session: SessionDep, player_in: PlayerCreate
    ) -> Player:
        repo = PlayersRepository(session)
        player = await repo.create_player(player_in)
        return player

    async def update_player(
        self, session: SessionDep, user_public_id: UUID, player_in: PlayerUpdate
    ) -> Player:
        repo = PlayersRepository(session)
        return await repo.update_player(user_public_id, player_in)

    async def read_player(
        self, session: SessionDep, user_public_id: UUID
    ) -> Player:
        repo = PlayersRepository(session)
        return await repo.read_player(user_public_id)
