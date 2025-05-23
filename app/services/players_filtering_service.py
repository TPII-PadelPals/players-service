from uuid import UUID

import numpy as np

from app.models.player import PlayerFilters, PlayerList
from app.services.players_service import PlayersService
from app.services.strokes_service import StrokesService
from app.utilities.dependencies import SessionDep
from app.utilities.neighbors import nearest_neighbors_query


class PlayersFilteringService:
    DISTANCE_METRIC = "cityblock"

    async def get_players_by_filters(
        self,
        session: SessionDep,
        player_filters: PlayerFilters,
    ) -> PlayerList:
        # Start TODO
        # Investigate how to extract this params
        # from PlayerFilters and set them as extra
        # params of the API request
        user_public_id = player_filters.user_public_id
        player_filters.user_public_id = None
        n_players = player_filters.n_players
        player_filters.n_players = None
        # End TODO
        if n_players is not None and n_players <= 0:
            return PlayerList(data=[])

        players_service = PlayersService()
        players = await players_service.get_players_by_filters(session, player_filters)
        players = await self._get_players_by_similitude(
            session, players, user_public_id, n_players
        )

        players.data = players.data[:n_players]
        return players

    async def _get_players_by_similitude(
        self,
        session: SessionDep,
        players: PlayerList,
        user_public_id: UUID | None,
        n_players: int | None,
    ) -> PlayerList:
        """
        From `players`, filter the n_players (at most) who are the
        most similar to the one given by the user_public_id.
        """
        if user_public_id is None:
            return players

        players.data = [
            player for player in players.data if player.user_public_id != user_public_id
        ]
        if len(players.data) == 0:
            return players

        user_public_ids = [user_public_id] + [
            player.user_public_id for player in players.data
        ]
        strokes = [
            await StrokesService().get_strokes(session, user_public_id)
            for user_public_id in user_public_ids
        ]
        strokes_array = np.array([stroke.to_numpy_array() for stroke in strokes])

        max_players = len(players.data)
        if n_players is not None:
            max_players = min(max_players, n_players)

        idxs_neighbors = nearest_neighbors_query(
            X=strokes_array[1:],
            query=strokes_array[:1],
            n_neighbors=max_players,
            metric=self.DISTANCE_METRIC,
            algorithm="auto",
        )

        players.data = [players.data[idx] for idx in idxs_neighbors.flatten()]
        return players
