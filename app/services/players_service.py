from uuid import UUID

from app.models.player import (
    Player,
    PlayerCreate,
    PlayerFilters,
    PlayerList,
    PlayerUpdate,
)
from app.repository.players_repository import PlayersRepository
from app.services.google_service import GoogleService
from app.services.players_similarity_service import PlayersSimilarityService
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
        if player_in.address:
            service = GoogleService()
            longitude, latitude = await service.get_coordinates(player_in.address)
            player_in.longitude = longitude
            player_in.latitude = latitude
        repo = PlayersRepository(session)
        return await repo.update_player(user_public_id, player_in)

    async def read_player(self, session: SessionDep, user_public_id: UUID) -> Player:
        repo = PlayersRepository(session)
        return await repo.get_player_by_user_public_id(user_public_id)

    async def get_players_by_filters(
        self, session: SessionDep, player_filters: PlayerFilters
    ) -> PlayerList:
        n_players = player_filters.n_players
        if n_players is not None and n_players <= 0:
            return PlayerList(data=[])

        repo = PlayersRepository(session)
        players = await repo.get_players_by_filters(player_filters)

        sim_service = PlayersSimilarityService()
        players = await sim_service.get_players_by_similtude(
            session, player_filters.user_public_id, players, n_players
        )

        players.data = players.data[:n_players]
        return players
