from typing import Any

from sklearn.neighbors import NearestNeighbors  # type: ignore


def nearest_neighbors_query(
    X: Any, query: Any, n_neighbors: int, metric: str, algorithm: str
) -> Any:
    nbrs = NearestNeighbors(n_neighbors=n_neighbors, algorithm=algorithm, metric=metric)
    nbrs.fit(X)
    indices = nbrs.kneighbors(query, return_distance=False)
    return indices
