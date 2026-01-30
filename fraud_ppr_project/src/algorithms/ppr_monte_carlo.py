# src/algorithms/ppr_monte_carlo.py
import numpy as np
from scipy import sparse

def personalized_pagerank_monte_carlo(A, alpha=0.85, personalize=None, num_walks=1000, max_steps=50):
    """
    Monte Carlo approximation of Personalized PageRank.
    
    Parameters:
    -----------
    A : scipy.sparse.csr_matrix
        Adjacency matrix of the graph
    alpha : float
        Damping factor (probability to continue the random walk)
    num_walks : int
        Number of random walks to simulate
    max_steps : int
        Maximum length of each random walk
    personalize : np.ndarray, optional
        Personalization vector. If None, uniform distribution is used.
    
    Returns:
    --------
    scores : np.ndarray
        PageRank scores for each node
    """
    n = A.shape[0]
    
    if personalize is None:
        personalize = np.ones(n) / n
    else:
        personalize = personalize / personalize.sum()
    
    scores = np.zeros(n)
    
    # Precompute row distributions for faster access
    row_distributions = []
    for i in range(n):
        neighbors = A[i].indices
        if len(neighbors) > 0:
            probs = A[i].data
            probs = probs / probs.sum()
            row_distributions.append((neighbors, probs))
        else:
            row_distributions.append((np.array([]), np.array([])))
    
    # Perform random walks
    for _ in range(num_walks):
        current = np.random.choice(n, p=personalize)
        
        for step in range(max_steps):
            scores[current] += 1
            
            if np.random.random() < alpha:
                neighbors, probs = row_distributions[current]
                if len(neighbors) > 0:
                    current = np.random.choice(neighbors, p=probs)
                else:
                    break  # Dead end
            else:
                break  # Teleport
    
    return scores / (num_walks * max_steps)