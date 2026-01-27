# src/evaluation/metrics.py

from typing import Dict

import numpy as np


def precision_at_k(
    scores: np.ndarray,
    labels_dict: Dict[int, int],
    k: int,
) -> float:
    """
    Compute Precision@K for ranking given node-level fraud labels.

    Parameters
    ----------
    scores : np.ndarray, shape (n,)
        PPR scores (index = node id).
    labels_dict : dict[int, int]
        Mapping node_id -> label (1 = fraud, 0 = non-fraud).
        Nodes not present in this dict are treated as unlabeled (0).
    k : int
        The cut-off rank K.

    Returns
    -------
    precision : float
        Precision@K value in [0, 1]. If K == 0, returns 0.0.
    """
    n = len(scores)
    if k <= 0 or n == 0:
        return 0.0

    labeled = np.zeros(n, dtype=int)
    for node, lab in labels_dict.items():
        if 0 <= node < n:
            labeled[node] = int(lab)

    # Effective K cannot exceed number of nodes
    k_eff = min(k, n)

    # Indices of top-k nodes by score (descending)
    top_k = np.argsort(scores)[::-1][:k_eff]

    relevant = labeled[top_k].sum()
    precision = relevant / float(k_eff) if k_eff > 0 else 0.0
    return precision
