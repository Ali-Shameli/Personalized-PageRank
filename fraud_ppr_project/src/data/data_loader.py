from typing import Dict, Tuple, List
import numpy as np
from scipy import sparse
from src.data.graph_utils import process_raw_graph_data


def load_transactions(path: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray, int, Dict[int, int], Dict[int, int]]:
    """
    Load transactions from a CSV file.

    This function reads the raw CSV data, extracts edges and labels,
    and then delegates the mapping and normalization logic to 'process_raw_graph_data'.

    Parameters
    ----------
    path : str
        Path to the CSV file.

    Returns
    -------
    src : np.ndarray
        Mapped source node indices.
    dst : np.ndarray
        Mapped destination node indices.
    weights : np.ndarray
        Transaction amounts as edge weights.
    n_nodes : int
        Total number of unique nodes found.
    labels : dict
        Dictionary of fraud labels (mapped ID -> label).
    reverse_map : dict
        Dictionary to translate internal IDs back to original CSV IDs.
    """
    raw_src: List[int] = []
    raw_dst: List[int] = []
    raw_weights: List[float] = []
    raw_seeds: List[int] = []  # To store IDs labeled as fraud (label=1)

    with open(path, "r", encoding="utf-8") as f:
        # Skip the header line if present
        header = next(f, None)
        if header is None:
            raise ValueError(f"Empty file: {path}")

        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split(",")
            # Expected CSV format: src_id, dst_id, amount, [label]
            # We need at least 3 columns (src, dst, amount)
            if len(parts) < 3:
                continue

            try:
                s = int(parts[0])
                d = int(parts[1])
                w = float(parts[2])

                # Ensure positive weight (optional safety check)
                if w <= 0:
                    w = 1.0

                raw_src.append(s)
                raw_dst.append(d)
                raw_weights.append(w)

                # Check for the optional 4th column (Fraud Label)
                # Typically, the label is associated with the destination node (d)
                if len(parts) > 3 and parts[3] != "":
                    label = int(parts[3])
                    if label == 1:
                        raw_seeds.append(d)

            except ValueError:
                # Skip lines that contain non-numeric data or parsing errors
                continue

    if not raw_src:
        raise ValueError(f"No valid edges found in file: {path}")

    # Use the shared utility to process raw lists into mapped arrays
    return process_raw_graph_data(raw_src, raw_dst, raw_weights, raw_seeds)


def build_adj_matrix(
    src: np.ndarray,
    dst: np.ndarray,
    weights: np.ndarray,
    n_nodes: int,
) -> sparse.csr_matrix:
    """
    Build a weighted adjacency matrix in CSR format using mapped indices.

    Parameters
    ----------
    src : np.ndarray
        Source node indices (0 to N-1).
    dst : np.ndarray
        Destination node indices (0 to N-1).
    weights : np.ndarray
        Edge weights corresponding to (src, dst) pairs.
    n_nodes : int
        Total number of nodes (dimension of the matrix).

    Returns
    -------
    sparse.csr_matrix
        The weighted adjacency matrix of shape (n_nodes, n_nodes).
    """
    if src.shape != dst.shape or src.shape != weights.shape:
        raise ValueError("src, dst, and weights arrays must have the same shape")

    # Construct the sparse matrix
    # Duplicate edges are summed by default in CSR construction
    A = sparse.csr_matrix((weights, (src, dst)), shape=(n_nodes, n_nodes))
    return A