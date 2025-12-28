# data_loader.py
import numpy as np
from scipy import sparse


def load_transactions(path):
    """
    Loads transactions and maps potentially sparse IDs to contiguous indices (0..N-1).
    Returns:
        mapped_src, mapped_dst, mapped_weights, n_nodes, mapped_labels,
        node_map (RealID -> InternalID), reverse_map (InternalID -> RealID)
    """
    raw_src, raw_dst, weights = [], [], []
    raw_labels = {}  # Store labels using real node IDs as keys

    with open(path, 'r') as f:
        next(f)  # Skip the CSV header line
        for line in f:
            parts = line.strip().split(',')
            if not parts:
                continue

            s = int(parts[0])
            d = int(parts[1])
            w = float(parts[2])

            raw_src.append(s)
            raw_dst.append(d)
            weights.append(w)

            # Check if the file contains a label column (the fourth column)
            if len(parts) > 3:
                raw_labels[d] = int(parts[3])

    # Identify all unique nodes and sort them to ensure consistent mapping
    unique_nodes = sorted(list(set(raw_src) | set(raw_dst)))
    n_nodes = len(unique_nodes)

    # Create mapping dictionaries
    # node_map: Transforms real ID (e.g., 7000) to an internal index (e.g., 2)
    node_map = {node_id: idx for idx, node_id in enumerate(unique_nodes)}

    # reverse_map: Transforms internal index back to real ID for final results display
    reverse_map = {idx: node_id for idx, node_id in enumerate(unique_nodes)}

    # Convert raw ID lists to mapped index arrays (values will be between 0 and N-1)
    mapped_src = np.array([node_map[s] for s in raw_src])
    mapped_dst = np.array([node_map[d] for d in raw_dst])
    mapped_weights = np.array(weights)

    # Convert labels to use internal indices for evaluation calculations
    mapped_labels = {}
    for real_id, label in raw_labels.items():
        if real_id in node_map:
            mapped_labels[node_map[real_id]] = label

    return mapped_src, mapped_dst, mapped_weights, n_nodes, mapped_labels, node_map, reverse_map


def build_adj_matrix(src, dst, weights, n_nodes):
    """
    Builds a weighted adjacency matrix using compressed sparse row format.
    Input src and dst must already be mapped to contiguous indices.
    """
    A = sparse.csr_matrix((weights, (src, dst)), shape=(n_nodes, n_nodes))
    return A