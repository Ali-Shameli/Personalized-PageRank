import numpy as np
from scipy import sparse
from src.algorithms.ppr_power import personalized_pagerank

def update_ppr_incremental(adj_matrix, old_scores, personalization_vec, alpha, new_edges, tol=1e-6):
    """
    Update PPR efficiently using Warm Start.
    personalization_vec: np.array (P vector, not dict)
    """
    # 1. Update Adjacency
    A = adj_matrix.tolil()
    n = A.shape[0]

    max_node_idx = n - 1
    for s, d, w in new_edges:
        max_node_idx = max(max_node_idx, s, d)
    new_n = max_node_idx + 1

    # Resize if needed
    if new_n > n:
        A.resize((new_n, new_n))
        old_scores = np.pad(old_scores, (0, new_n - n), 'constant')
        # Pad personalization vector too! (important)
        personalization_vec = np.pad(personalization_vec, (0, new_n - n), 'constant')
        # Normalize p again just in case (though padding 0s keeps sum same)
        if personalization_vec.sum() > 0:
             personalization_vec /= personalization_vec.sum()
        
        n = new_n

    # Update edges
    for s, d, w in new_edges:
        A[s, d] = w

    new_adj = A.tocsr()

    # 2. Warm Start Power Iteration
    # Unpack tuple result!
    new_scores, _, _ = personalized_pagerank(
        new_adj,
        personalize=personalization_vec, # Now it's the padded array
        alpha=alpha,
        tol=tol,
        max_iter=50,
        start_vec=old_scores
    )

    return new_adj, new_scores