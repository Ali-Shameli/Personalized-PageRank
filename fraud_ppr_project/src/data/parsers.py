from typing import Tuple, Dict, List
import numpy as np
from src.data.graph_utils import process_raw_graph_data

def parse_manual_data(edges_text: str, seeds_text: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray, int, Dict[int, int], Dict[int, int]]:
    raw_src: List[int] = []
    raw_dst: List[int] = []
    raw_weights: List[float] = []

    lines = edges_text.strip().splitlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue

        parts = line.replace(",", " ").split()

        if len(parts) < 3:
            raise ValueError(f"Invalid line format: {line}")

        try:
            s = int(parts[0])
            d = int(parts[1])
            w = float(parts[2])

            if w <= 0:
                w = 1.0

            raw_src.append(s)
            raw_dst.append(d)
            raw_weights.append(w)
        except ValueError:
            raise ValueError(f"Values must be numeric: {line}")

    if not raw_src:
        raise ValueError("No valid edges found.")

    raw_seeds: List[int] = []
    if seeds_text.strip():
        try:
            for x in seeds_text.replace(",", " ").split():
                raw_seeds.append(int(x))
        except ValueError:
            raise ValueError("Seeds must be integer Node IDs.")

    return process_raw_graph_data(raw_src, raw_dst, raw_weights, raw_seeds)