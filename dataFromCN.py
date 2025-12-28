import sys
import numpy as np
from customNetworkCreator import get_manual_graph_data

def provide_data_from_cn():
    # Retrieve raw data from user input
    raw_src, raw_dst, raw_weights, raw_seeds_input = get_manual_graph_data()

    if not raw_src:
        print("No edges provided. Exiting.")
        sys.exit()

    # Perform mapping for manual input to handle sparse IDs like 10, 200, 9000
    # Identify all unique nodes involved in edges and seeds
    unique_nodes = sorted(list(set(raw_src) | set(raw_dst) | set(raw_seeds_input)))
    n_nodes = len(unique_nodes)

    # Create mapping dictionaries: Real ID <-> Internal Index (0 to N-1)
    node_map = {uid: idx for idx, uid in enumerate(unique_nodes)}
    reverse_map = {idx: uid for idx, uid in enumerate(unique_nodes)}

    # Convert raw lists to mapped numpy arrays for the adjacency matrix
    src = np.array([node_map[s] for s in raw_src])
    dst = np.array([node_map[d] for d in raw_dst])
    weights = np.array(raw_weights)

    # Initialize fraud seeds and labels dictionary for evaluation
    fraud_seeds = []
    labels = {}

    # Map the seeds provided by user and set ground truth labels
    for s in raw_seeds_input:
        if s in node_map:
            internal_idx = node_map[s]
            fraud_seeds.append(internal_idx)
            # Mark seed nodes as fraud (1) for precision calculation
            labels[internal_idx] = 1
        else:
            print(f"Warning: Seed {s} is not in the graph edges, ignoring.")

    # Explicitly mark non-seed nodes as non-fraud (0)
    for i in range(n_nodes):
        if i not in labels:
            labels[i] = 0

    return src, dst, weights, n_nodes, labels, node_map, reverse_map, fraud_seeds