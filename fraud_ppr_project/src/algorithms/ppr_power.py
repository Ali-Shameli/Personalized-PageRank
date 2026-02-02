# src/algorithms/ppr_power.py

from typing import Iterable, Optional, Tuple
import numpy as np
from scipy import sparse

def make_personalization_vector(n_nodes: int, fraud_seeds: Iterable[int]) -> np.ndarray:
    """Build a normalized personalization vector p."""
    p = np.zeros(n_nodes, dtype=np.float64)
    seeds = list(fraud_seeds)
    if len(seeds) == 0:
        p[:] = 1.0 / n_nodes
    else:
        p[seeds] = 1.0
        p /= p.sum()
    return p

def personalized_pagerank(
    A: sparse.spmatrix,
    alpha: float = 0.15,
    max_iter: int = 100,
    tol: float = 1e-6,
    personalize: Optional[np.ndarray] = None,
    start_vec: Optional[np.ndarray] = None  # <--- اضافه شد
) -> Tuple[np.ndarray, int, float]:
    """
    Compute Personalized PageRank scores using power iteration.
    Supports warm start via start_vec.
    """
    if alpha <= 0.0 or alpha >= 1.0:
        raise ValueError("alpha must be in (0, 1)")

    if not sparse.isspmatrix_csr(A):
        A = A.tocsr()

    n, m = A.shape
    if n != m:
        raise ValueError("Adjacency matrix A must be square")

    # Out-degree
    out_deg = np.asarray(A.sum(axis=1)).reshape(-1)
    dangling = (out_deg == 0)

    # Transition matrix M
    k = np.where(out_deg > 0)[0]
    inv_out = sparse.csr_matrix((1.0 / out_deg[k], (k, k)), shape=(n, n))
    M = inv_out @ A

    # Personalization vector p
    if personalize is None:
        p = np.ones(n, dtype=np.float64) / n
    else:
        p = np.asarray(personalize, dtype=np.float64)
        if p.shape[0] != n:
            raise ValueError(f"personalize vector length {p.shape[0]} != n_nodes {n}")
        if p.sum() == 0.0:
            p = np.ones(n, dtype=np.float64) / n
        else:
            p /= p.sum()

    # Initialization (Warm Start Logic)
    if start_vec is not None:
        if start_vec.shape[0] != n:
             raise ValueError(f"start_vec length {start_vec.shape[0]} != n_nodes {n}")
        r = start_vec.astype(np.float64).copy()
        if r.sum() > 0:
            r /= r.sum()
    else:
        r = p.copy()  # Cold start from personalization

    final_err = float("inf")
    n_iter = 0

    for it in range(1, max_iter + 1):
        r_old = r.copy()
        walk = r_old @ M
        dangling_mass = r_old[dangling].sum()
        
        # Power Iteration Formula
        # r = (1-α)*walk + ( (1-α)*dangling_mass + α ) * p
        
        r = (1.0 - alpha) * walk + ((1.0 - alpha) * dangling_mass + alpha) * p

        final_err = np.abs(r - r_old).sum()
        n_iter = it
        if final_err < tol:
            break

    if r.sum() > 0:
        r /= r.sum()

    return r, n_iter, final_err