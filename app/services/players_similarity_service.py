from uuid import UUID

import numpy as np
from sklearn.neighbors import BallTree  # type: ignore

from app.models.player import PlayerList
from app.services.strokes_service import StrokesService
from app.utilities.dependencies import SessionDep


class PlayersSimilarityService:
    DISTANCE_METRIC = "euclidean"

    async def get_players_by_similtude(
        self,
        session: SessionDep,
        user_public_id: UUID | None,
        players: PlayerList,
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

        ball_tree = BallTree(strokes_array[1:], metric=self.DISTANCE_METRIC)
        _, idxs_neighbors = ball_tree.query(strokes_array[:1], k=max_players)

        players.data = [players.data[idx] for idx in idxs_neighbors.flatten()]
        return players
