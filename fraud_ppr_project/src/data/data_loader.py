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



