# evaluate.py
import numpy as np

def precision_at_k(scores, labels_dict, k):
    """
    scores: np.array of PPR scores (index = node id)
    labels_dict: {node_id: 0/1} where 1 = fraud
    """
    n = len(scores)
    labeled = np.zeros(n, dtype=int)
    for node, lab in labels_dict.items():
        if node < n:
            labeled[node] = lab
    #The actual number of nodes we can take.
    k_eff = min (k, n)
    
    top_k = np.argsort(scores)[::-1][:k_eff]
    relevant = labeled[top_k].sum()
    return relevant / float(k_eff) if k_eff > 0 else 0.0
