from app.models.player import Player, PlayerCreate
from app.repository.players_repository import PlayersRepository
from app.utilities.dependencies import SessionDep


class PlayersService:
    async def create_player(
        self, session: SessionDep, player_in: PlayerCreate
    ) -> Player:
        repo = PlayersRepository(session)
        player = await repo.create_player(player_in)
        return player
