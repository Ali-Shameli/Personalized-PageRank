# data_loader.py
import numpy as np
from scipy import sparse


def load_transactions(path):
    """
    Loads transactions with weights (amounts).
    Expected CSV columns: src_id, dst_id, amount, label(optional)
    """
    src, dst, weights = [], [], []
    labels = {}

    with open(path, 'r') as f:
        next(f)  # skip header
        for line in f:
            parts = line.strip().split(',')
            s = int(parts[0])
            d = int(parts[1])

            w = float(parts[2])

            src.append(s)
            dst.append(d)
            weights.append(w)

            if len(parts) > 3:
                labels[d] = int(parts[3])

    n_nodes = max(max(src), max(dst)) + 1

    return np.array(src), np.array(dst), np.array(weights), n_nodes, labels


def build_adj_matrix(src, dst, weights, n_nodes):
    """
    Builds a weighted adjacency matrix.
    src, dst: node indices
    weights: edge weights (transaction amounts)
    """
    # using weights instead np.ones
    # if there is more than one connection between two nodes, they are combined
    A = sparse.csr_matrix((weights, (src, dst)), shape=(n_nodes, n_nodes))
    return A