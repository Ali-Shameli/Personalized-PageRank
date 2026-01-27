# src/algorithms/ppr_power.py

from typing import Iterable, Optional, Tuple

import numpy as np
from scipy import sparse


def make_personalization_vector(
    n_nodes: int,
    fraud_seeds: Iterable[int],
) -> np.ndarray:
    """
    Build a normalized personalization vector p.

    Parameters
    ----------
    n_nodes : int
        Total number of nodes in the graph.
    fraud_seeds : iterable of int
        Node indices marked as fraudulent (seed set).

    Returns
    -------
    p : np.ndarray, shape (n_nodes,)
        Normalized personalization vector.
    """
    p = np.zeros(n_nodes, dtype=np.float64)

    seeds = list(fraud_seeds)
    if len(seeds) == 0:
        # Fallback: uniform over all nodes
        p[:] = 1.0 / n_nodes
    else:
        p[seeds] = 1.0
        p /= p.sum()

    return p


def personalized_pagerank(
    A: sparse.spmatrix,
    alpha: float = 0.85,
    max_iter: int = 100,
    tol: float = 1e-6,
    personalize: Optional[np.ndarray] = None,
) -> Tuple[np.ndarray, int, float]:
    """
    Compute Personalized PageRank scores using power iteration.

    Parameters
    ----------
    A : sparse matrix (n x n)
        Adjacency matrix with edges i -> j encoded as A[i, j] > 0.
        Will be converted to CSR if needed.
    alpha : float, default=0.85
        Teleportation probability (damping factor) in (0, 1).
    max_iter : int, default=100
        Maximum number of iterations.
    tol : float, default=1e-6
        L1 tolerance for convergence.
    personalize : array-like of shape (n,), optional
        Personalization vector p. Will be cast to float64 and normalized.
        If None, a uniform vector is used.

    Returns
    -------
    r : np.ndarray, shape (n,)
        Personalized PageRank scores (sum to 1).
    n_iter : int
        Number of iterations actually performed.
    final_err : float
        L1 difference between last two iterations.
    """
    if alpha <= 0.0 or alpha >= 1.0:
        raise ValueError("alpha must be in (0, 1)")

    # Ensure CSR format
    if not sparse.isspmatrix_csr(A):
        A = A.tocsr()

    n, m = A.shape
    if n != m:
        raise ValueError("Adjacency matrix A must be square")

    # Out-degree
    out_deg = np.asarray(A.sum(axis=1)).reshape(-1)

    # Dangling nodes: rows with zero out-degree
    dangling = (out_deg == 0)

    # Row-normalize A to get transition matrix M
    # Only non-zero out_deg rows are scaled
    k = np.where(out_deg > 0)[0]
    inv_out = sparse.csr_matrix((1.0 / out_deg[k], (k, k)), shape=(n, n))
    M = inv_out @ A  # csr, row-stochastic for non-dangling rows

    # Personalization vector p
    if personalize is None:
        p = np.ones(n, dtype=np.float64) / n
    else:
        p = np.asarray(personalize, dtype=np.float64)
        if p.shape[0] != n:
            raise ValueError("personalize vector has wrong length")
        if p.sum() == 0.0:
            raise ValueError("personalize vector must not be all zeros")
        p /= p.sum()

    # Initialize rank vector from personalization
    r = p.copy()

    final_err = float("inf")
    n_iter = 0

    for it in range(1, max_iter + 1):
        r_old = r.copy()

        # Random-walk step
        walk = r_old @ M

        # Dangling mass redistributed according to p
        dangling_mass = r_old[dangling].sum()

        # Teleport + walk + dangling
        r = (1.0 - alpha) * walk + (1.0 - alpha) * dangling_mass * p + alpha * p

        # Convergence check (L1 norm)
        final_err = np.abs(r - r_old).sum()
        n_iter = it
        if final_err < tol:
            break

    # Normalize for safety
    s = r.sum()
    if s > 0:
        r /= s

    return r, n_iter, final_err
