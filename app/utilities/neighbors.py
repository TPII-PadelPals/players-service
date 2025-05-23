from typing import Any

import numpy as np
from sklearn.neighbors import NearestNeighbors  # type: ignore
from sklearn_extra.cluster import KMedoids  # type: ignore


class NearestNeighborsWrapper:
    def __init__(self, metric: str = "cityblock", algorithm: str = "auto") -> None:
        self.metric = metric
        self.algorithm = algorithm

    def query(self, X: Any, query: Any, n_neighbors: int) -> Any:
        nbrs = NearestNeighbors(
            n_neighbors=n_neighbors, metric=self.metric, algorithm=self.algorithm
        )
        nbrs.fit(X)
        return nbrs.kneighbors(query, return_distance=False)


class KMedoidsNeighbors:
    def __init__(
        self,
        n_clusters: int = 10,
        metric: str = "cityblock",
        method: str = "alternate",
        init: str = "random",
        max_iter: int = 300,
    ) -> None:
        self.n_clusters = n_clusters
        self.metric = metric
        self.method = method
        self.init = init
        self.max_iter = max_iter

    def query(self, X: Any, query: Any, n_neighbors: int) -> Any:
        # Fit KMedoids
        model = KMedoids(
            n_clusters=self.n_clusters,
            metric=self.metric,
            method=self.method,
            init=self.init,
            max_iter=self.max_iter,
            random_state=None,
        )
        cluster_labels = model.fit_predict(X)

        # Group data by cluster (keep track of original indices)
        cluster_data = {
            i: np.where(cluster_labels == i)[0] for i in range(self.n_clusters)
        }

        # Precompute medoid locations
        medoids = model.cluster_centers_

        # Compute query distances to medoids
        dists = np.sum(np.abs(medoids - query), axis=1)
        cluster_order = np.argsort(dists)  # Closest clusters first

        # Accumulate point indices from clusters until we have at most n_neighbors
        candidate_indices: list[Any] = []

        for cluster_id in cluster_order:
            candidate_indices.extend(cluster_data[cluster_id])
            if len(candidate_indices) >= n_neighbors:
                break

        # Pick random indices from the candidates
        selected_idx = np.random.choice(
            len(candidate_indices), n_neighbors, replace=False
        )
        result_indices = np.array(candidate_indices)[selected_idx]

        return result_indices
