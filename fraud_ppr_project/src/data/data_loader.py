# src/data/data_loader.py

from typing import Dict, Tuple

import numpy as np
from scipy import sparse


def load_transactions(path: str) -> Tuple[np.ndarray, np.ndarray, int, Dict[int, int]]:
    """
    Load transaction edges (and optional fraud labels) from a CSV file.

    Expected CSV format (with header):
        src_id,dst_id,amount,label(optional)

    Parameters
    ----------
    path : str
        Path to the CSV file.

    Returns
    -------
    src : np.ndarray, shape (m,)
        Source node indices for each edge.
    dst : np.ndarray, shape (m,)
        Destination node indices for each edge.
    n_nodes : int
        Number of nodes in the graph (max node id + 1).
    labels : dict[int, int]
        Optional fraud labels keyed by node id (typically dst).
        Empty if no label column is present.
    """
    src: list[int] = []
    dst: list[int] = []
    labels: Dict[int, int] = {}

    with open(path, "r", encoding="utf-8") as f:
        # Skip header
        header = next(f, None)
        if header is None:
            raise ValueError(f"Empty file: {path}")

        for line in f:
            line = line.strip()
            if not line:
                continue  # skip empty lines

            parts = line.split(",")
            if len(parts) < 2:
                continue  # malformed line, ignore

            s = int(parts[0])
            d = int(parts[1])
            src.append(s)
            dst.append(d)

            # Optional fraud label (assumed on dst node)
            if len(parts) > 3 and parts[3] != "":
                labels[d] = int(parts[3])

    if not src or not dst:
        raise ValueError(f"No edges found in file: {path}")

    n_nodes = max(max(src), max(dst)) + 1

    return np.array(src, dtype=np.int64), np.array(dst, dtype=np.int64), n_nodes, labels


def build_adj_matrix(
    src: np.ndarray,
    dst: np.ndarray,
    n_nodes: int,
) -> sparse.csr_matrix:
    """
    Build an unweighted adjacency matrix in CSR format.

    Parameters
    ----------
    src : np.ndarray, shape (m,)
        Source node indices.
    dst : np.ndarray, shape (m,)
        Destination node indices.
    n_nodes : int
        Number of nodes in the graph.

    Returns
    -------
    A : csr_matrix, shape (n_nodes, n_nodes)
        Adjacency matrix with A[i, j] > 0 if edge i -> j exists.
        Multiple edges are simply summed (weight = count).
    """
    if src.shape != dst.shape:
        raise ValueError("src and dst must have the same shape")

    data = np.ones(len(src), dtype=np.float64)
    A = sparse.csr_matrix((data, (src, dst)), shape=(n_nodes, n_nodes))
    return A
