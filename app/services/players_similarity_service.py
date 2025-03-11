import numpy as np
from sklearn.neighbors import BallTree

from app.models.player import PlayerFilters, PlayerList
from app.services.strokes_service import StrokesService
from app.utilities.dependencies import SessionDep


class PlayersSimilarityService:
    async def filter_similar_players(
        self, session: SessionDep, players: PlayerList, player_filters: PlayerFilters
    ) -> PlayerList:
        main_user_public_id = player_filters.user_public_id
        if main_user_public_id is None:
            return players

        other_players = [
            player
            for player in players.data
            if player.user_public_id != main_user_public_id
        ]
        len_others = len(other_players)
        if len_others == 0:
            return players

        strokes_service = StrokesService()
        main_strokes = (
            (await strokes_service.get_strokes(session, main_user_public_id))
            .to_numpy()
            .reshape(1, -1)
        )
        other_strokes = []
        for other_player in other_players:
            other_stroke = (
                await strokes_service.get_strokes(session, other_player.user_public_id)
            ).to_numpy()
            other_strokes.append(other_stroke)
        other_strokes = np.array(other_strokes)  # type: ignore

        n_players = player_filters.n_players
        if n_players is None:
            n_players = len_others
        else:
            n_players = min(len_others, n_players)

        ball_tree = BallTree(other_strokes, metric="euclidean")
        _, indices_neighbors = ball_tree.query(main_strokes, k=n_players)

        players.data = [other_players[idx] for idx in indices_neighbors.flatten()]

        return players
