# data_loader.py
import numpy as np
from scipy import sparse

def load_transactions(path):
    # Expected CSV columns: src_id,dst_id,amount,label(optional)
    src, dst = [], []
    labels = {}
    with open(path) as f:
        next(f)  # skip header
        for line in f:
            parts = line.strip().split(',')
            s = int(parts[0]); d = int(parts[1])
            src.append(s); dst.append(d)
            if len(parts) > 3:  # optional fraud label for dst
                labels[d] = int(parts[3])
    n_nodes = max(max(src), max(dst)) + 1
    return np.array(src), np.array(dst), n_nodes, labels

def build_adj_matrix(src, dst, n_nodes):
    # Unweighted adjacency; multiple edges just add 1 each
    data = np.ones(len(src), dtype=np.float64)
    A = sparse.csr_matrix((data, (src, dst)), shape=(n_nodes, n_nodes))
    return A
