from typing import Tuple, Dict, List
import numpy as np
from src.data.graph_utils import process_raw_graph_data

def parse_manual_data(edges_text: str, seeds_text: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray, int, Dict[int, int], Dict[int, int]]:
    raw_src: List[int] = []
    raw_dst: List[int] = []
    raw_weights: List[float] = []

    # 1. Parse Edges Text
    for line in edges_text.strip().splitlines():
        # raw_src.append(...)

    # 2. Parse Seeds Text
    raw_seeds: List[int] = []
    if seeds_text.strip():

    return process_raw_graph_data(raw_src, raw_dst, raw_weights, raw_seeds)