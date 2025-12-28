# ppr.py
import numpy as np
from scipy import sparse


def make_personalization_vector(n_nodes, fraud_seeds):
    p = np.zeros(n_nodes, dtype=np.float64)
    if len(fraud_seeds) == 0:
        p[:] = 1.0 / n_nodes
    else:
        p[fraud_seeds] = 1.0
        p /= p.sum()
    return p


def personalized_pagerank(A, alpha=0.85, max_iter=100, tol=1e-6,
                          personalize=None):
    """
    A: csr_matrix, shape (n, n), edges i->j as A[i, j] > 0
    """
    n, _ = A.shape

    # Out-degree
    out_deg = np.asarray(A.sum(axis=1)).reshape(-1)

    # Handle dangling nodes: give their mass according to p
    dangling = (out_deg == 0)

    # Row-normalize A to get transition matrix M
    # Only non-zero out_deg rows are scaled
    k = np.where(out_deg > 0)[0]
    inv_out = sparse.csr_matrix((1.0 / out_deg[k], (k, k)), shape=(n, n))
    M = inv_out @ A  # still csr and row-stochastic for non-dangling rows

    if personalize is None:
        personalize = np.ones(n, dtype=np.float64) / n
    else:
        personalize = personalize.astype(np.float64)
        personalize /= personalize.sum()
    p = personalize

    r = p.copy()  # start from personalization
    for _ in range(max_iter):
        r_old = r.copy()
        # Teleport and walk step
        walk = r_old @ M
        # Add dangling contribution: redistribute dangling mass with p
        dangling_mass = r_old[dangling].sum()
        r = (1 - alpha) * walk + (1 - alpha) * dangling_mass * p + alpha * p

        # L1 convergence check
        if np.abs(r - r_old).sum() < tol:
            break

    # Normalize for safety
    r /= r.sum()
    return r
