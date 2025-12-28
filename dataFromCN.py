import sys

import numpy as np

from customNetworkCreator import get_manual_graph_data


def provide_data_from_cn(src, dst, weights, n_nodes, labels, node_map, reverse_map, fraud_seeds):
    raw_src, raw_dst, raw_weights, raw_seeds_input = get_manual_graph_data()

    if not raw_src:
        print("No edges provided. Exiting.")
        sys.exit()

    # Perform mapping for manual input to handle sparse IDs like 10, 200, 9000
    # Identify all unique nodes involved
    unique_nodes = sorted(list(set(raw_src) | set(raw_dst) | set(raw_seeds_input)))
    n_nodes = len(unique_nodes)

    # Create maps
    node_map = {uid: idx for idx, uid in enumerate(unique_nodes)}
    reverse_map = {idx: uid for idx, uid in enumerate(unique_nodes)}

    # Convert raw lists to mapped numpy arrays
    src = np.array([node_map[s] for s in raw_src])
    dst = np.array([node_map[d] for d in raw_dst])
    weights = np.array(raw_weights)

    # Map the seeds provided by user
    fraud_seeds = []
    for s in raw_seeds_input:
        if s in node_map:
            fraud_seeds.append(node_map[s])
        else:
            print(f"Warning: Seed {s} is not in the graph edges, ignoring.")

    return src, dst, weights, n_nodes, labels, node_map, reverse_map, fraud_seeds