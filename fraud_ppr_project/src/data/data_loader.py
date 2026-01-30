# src/data/data_loader.py

from typing import Dict, Tuple, List
import numpy as np
from scipy import sparse

def load_transactions(path: str) -> Tuple[np.ndarray, np.ndarray, int, Dict[int, int], Dict[int, int]]:
    """
    Load transactions and map sparse IDs to contiguous indices (0..N-1).
    Returns:
        src (mapped), dst (mapped), n_nodes, labels (mapped), reverse_map
    """
    raw_src: List[int] = []
    raw_dst: List[int] = []
    raw_labels: Dict[int, int] = {}

    with open(path, "r", encoding="utf-8") as f:
        # Skip header if present
        header = next(f, None)
        if header is None:
            raise ValueError(f"Empty file: {path}")

        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split(",")
            # Assume format: src, dst, amount, label(optional)
            if len(parts) < 2:
                continue

            try:
                s = int(parts[0])
                d = int(parts[1])
                raw_src.append(s)
                raw_dst.append(d)

                if len(parts) > 3 and parts[3] != "":
                    raw_labels[d] = int(parts[3])
            except ValueError:
                continue

    if not raw_src:
        raise ValueError(f"No valid edges found in file: {path}")

    # Mapping
    # 1. Find all unique nodes
    unique_nodes = sorted(list(set(raw_src) | set(raw_dst)))
    n_nodes = len(unique_nodes)

    # 2. Create translation dictionary (Real ID -> Internal Index)
    node_map = {node_id: idx for idx, node_id in enumerate(unique_nodes)}

    # 3. Create reverse translation dictionary (Internal Index -> Real ID) for user display
    reverse_map = {idx: node_id for idx, node_id in enumerate(unique_nodes)}

    # 4. Convert raw lists to mapped arrays
    mapped_src = np.array([node_map[s] for s in raw_src], dtype=np.int64)
    mapped_dst = np.array([node_map[d] for d in raw_dst], dtype=np.int64)

    # 5. Map labels to internal IDs
    mapped_labels = {}
    for real_id, label in raw_labels.items():
        if real_id in node_map:
            mapped_labels[node_map[real_id]] = int(label)

    return mapped_src, mapped_dst, n_nodes, mapped_labels, reverse_map

def build_adj_matrix(
        src: np.ndarray,
        dst: np.ndarray,
        n_nodes: int,
) -> sparse.csr_matrix:
    """Build adjacency matrix from MAPPED indices."""
    if src.shape != dst.shape:
        raise ValueError("src and dst must have the same shape")

    data = np.ones(len(src), dtype=np.float64)
    # Since IDs are mapped (0 to N-1), the matrix is built compactly and correctly
    A = sparse.csr_matrix((data, (src, dst)), shape=(n_nodes, n_nodes))
    return A
