from typing import Dict, Tuple, List
import numpy as np
from scipy import sparse


def load_transactions(path: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray, int, Dict[int, int], Dict[int, int]]:
    """
    Load transactions from a CSV file, handling edge weights and ID mapping.

    This function performs the following steps:
    1. Reads the CSV file (skips header).
    2. Extracts source, destination, and amount (weight).
    3. Maps sparse/large node IDs to contiguous internal indices (0 to N-1).
    4. Returns mapped arrays ready for the adjacency matrix.

    Returns:
        src (mapped): Source node indices.
        dst (mapped): Destination node indices.
        weights: Transaction amounts as edge weights.
        n_nodes: Total count of unique nodes.
        labels (mapped): Dictionary of fraud labels using mapped IDs.
        reverse_map: Dictionary to translate internal IDs back to real CSV IDs.
    """
    raw_src: List[int] = []
    raw_dst: List[int] = []
    raw_weights: List[float] = []
    raw_labels: Dict[int, int] = {}

    with open(path, "r", encoding="utf-8") as f:
        # Skip the header line if it exists
        header = next(f, None)
        if header is None:
            raise ValueError(f"Empty file: {path}")

        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split(",")
            # Expected format: src, dst, amount, [label]
            # We need at least 3 columns now (src, dst, amount)
            if len(parts) < 3:
                continue

            try:
                s = int(parts[0])
                d = int(parts[1])
                w = float(parts[2])  # Read the transaction amount as weight

                # Optional: Ensure weights are positive to avoid math errors in PageRank
                if w <= 0:
                    w = 1.0

                raw_src.append(s)
                raw_dst.append(d)
                raw_weights.append(w)

                # Check if a label column exists (4th column)
                if len(parts) > 3 and parts[3] != "":
                    raw_labels[d] = int(parts[3])
            except ValueError:
                # Skip lines with parsing errors
                continue

    if not raw_src:
        raise ValueError(f"No valid edges found in file: {path}")

    # --- Mapping Logic (Handling Sparse IDs) ---

    # 1. Identify all unique nodes in the graph
    unique_nodes = sorted(list(set(raw_src) | set(raw_dst)))
    n_nodes = len(unique_nodes)

    # 2. Create a map from Real ID (CSV) -> Internal Index (0..N-1)
    node_map = {node_id: idx for idx, node_id in enumerate(unique_nodes)}

    # 3. Create a reverse map from Internal Index -> Real ID (for display purposes)
    reverse_map = {idx: node_id for idx, node_id in enumerate(unique_nodes)}

    # 4. Convert raw lists to numpy arrays using the node_map
    mapped_src = np.array([node_map[s] for s in raw_src], dtype=np.int64)
    mapped_dst = np.array([node_map[d] for d in raw_dst], dtype=np.int64)

    # 5. Convert weights to a numpy float array
    mapped_weights = np.array(raw_weights, dtype=np.float64)

    # 6. Map the fraud labels to internal indices
    mapped_labels = {}
    for real_id, label in raw_labels.items():
        if real_id in node_map:
            mapped_labels[node_map[real_id]] = int(label)

    return mapped_src, mapped_dst, mapped_weights, n_nodes, mapped_labels, reverse_map


def build_adj_matrix(
        src: np.ndarray,
        dst: np.ndarray,
        weights: np.ndarray,
        n_nodes: int,
) -> sparse.csr_matrix:
    """
    Build a weighted adjacency matrix using Compressed Sparse Row (CSR) format.

    Parameters:
    src, dst: Mapped node indices.
    weights: Array of transaction amounts.
    n_nodes: Total number of nodes.
    """
    if src.shape != dst.shape or src.shape != weights.shape:
        raise ValueError("src, dst, and weights arrays must have the same shape")

    # Create the matrix using the actual weights instead of ones
    A = sparse.csr_matrix((weights, (src, dst)), shape=(n_nodes, n_nodes))
    return A
