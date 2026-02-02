from typing import List, Dict, Tuple
import numpy as np

def process_raw_graph_data(
    raw_src: List[int],
    raw_dst: List[int],
    raw_weights: List[float],
    raw_seeds: List[int] = None
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, int, Dict[int, int], Dict[int, int]]:
    """
    Common Logic: Takes raw lists and performs ID Mapping & Normalization.
    Used by both File Loader and Manual Parser.
    """
    if raw_seeds is None:
        raw_seeds = []

    # 1. Identify Unique Nodes
    unique_nodes = sorted(list(set(raw_src) | set(raw_dst) | set(raw_seeds)))
    n_nodes = len(unique_nodes)

    # 2. Create Maps
    node_map = {uid: i for i, uid in enumerate(unique_nodes)}
    reverse_map = {i: uid for i, uid in enumerate(unique_nodes)}

    # 3. Convert to Mapped Numpy Arrays
    mapped_src = np.array([node_map[s] for s in raw_src], dtype=np.int64)
    mapped_dst = np.array([node_map[d] for d in raw_dst], dtype=np.int64)
    mapped_weights = np.array(raw_weights, dtype=np.float64)

    # 4. Create Labels (Seeds -> Internal ID)
    mapped_labels = {}
    for s_id in raw_seeds:
        if s_id in node_map:
            mapped_labels[node_map[s_id]] = 1  # 1 means Fraud

    return mapped_src, mapped_dst, mapped_weights, n_nodes, mapped_labels, reverse_map