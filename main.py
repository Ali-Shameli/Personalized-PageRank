# main.py
import numpy as np
from data_loader import build_adj_matrix
from dynamicEvaluation import dynamic_evaluation
from ppr import make_personalization_vector, personalized_pagerank
from inputValidation import get_valid_input
from dataFromFile import provide_data_from_file
from dataFromCN import provide_data_from_cn


if __name__ == "__main__":
    print("=========================================")
    print("   Fraud Detection via Personalized PR   ")
    print("=========================================")
    print("1. Load from CSV file")
    print("2. Enter Graph Manually")

    choice = get_valid_input(
        "Select option [1/2]: ",
        int,
        lambda x: x in [1, 2]
    )

    # Initialize variables
    src, dst, weights = None, None, None
    n_nodes = 0
    fraud_seeds = []  # These will be internal mapped IDs
    labels = {}  # These will be internal mapped IDs

    # Mappings to handle sparse IDs
    node_map = {}  # Real ID -> Internal Index
    reverse_map = {}  # Internal Index -> Real ID

    if choice == 1:
        provide_data_from_file(src, dst, weights, n_nodes, labels, node_map, reverse_map, fraud_seeds)


    else:
        provide_data_from_cn(src, dst, weights, n_nodes, labels, node_map, reverse_map, fraud_seeds)


    # --- PPR Algorithm Execution ---

    # Build matrix using internal mapped indices (0 to n_nodes-1)
    A = build_adj_matrix(src, dst, weights, n_nodes)

    # Create personalization vector
    p = make_personalization_vector(n_nodes, fraud_seeds)

    # Compute PageRank
    print("\n[INFO] Computing Personalized PageRank...")
    scores = personalized_pagerank(A, alpha=0.85, max_iter=100, tol=1e-6, personalize=p)

    # Results Presentation
    # Sort by score descending
    sorted_nodes = np.argsort(scores)[::-1]

    print("\n[RESULTS] Most suspicious nodes:")
    print("-" * 50)

    display_limit = 20

    for rank, internal_idx in enumerate(sorted_nodes):
        # Stop after limit if loaded from file (to avoid flooding console)
        if rank >= display_limit:
            print("... (showing top 20 results)")
            break

        # Retrieve the original ID for display
        real_node_id = reverse_map.get(internal_idx, internal_idx)

        score = scores[internal_idx]

        # Check if it was a seed
        is_seed = " (Known Seed)" if internal_idx in fraud_seeds else ""

        print(f"Rank {rank + 1:2d}: Node {real_node_id:4d} | Score: {score:.6f}{is_seed}")


    # Dynamic Evaluation Section
    dynamic_evaluation(labels, n_nodes, scores)