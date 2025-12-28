# main.py
import numpy as np
import sys
from data_loader import load_transactions, build_adj_matrix
from ppr import make_personalization_vector, personalized_pagerank
from evaluate import precision_at_k


def get_valid_input(prompt, parse_func, condition=lambda x: True, error_msg="Invalid input."):
    """
    Helper function to ensure user input is valid.
    """
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input:
                continue
            parsed_value = parse_func(user_input)
            if condition(parsed_value):
                return parsed_value
            else:
                print(error_msg)
        except ValueError:
            print(error_msg)
        except Exception as e:
            print(f"Unexpected error: {e}")


def get_manual_graph_data():
    """
    Collects raw graph edges and seeds from user manually.
    Returns raw lists (before mapping).
    """
    print("\n--- Manual Graph Data Entry ---")
    print("Format: source destination weight")
    print("Example: 10 20 5.5")
    print("Type 'end' to finish adding edges.\n")

    src_list = []
    dst_list = []
    weights_list = []

    # Edge Collection Loop
    while True:
        line = input("Edge (src dst weight) or 'end': ").strip()
        if line.lower() == 'end':
            break

        parts = line.split()
        if len(parts) != 3:
            print("Invalid format. Need 3 values.")
            continue

        try:
            s = int(parts[0])
            d = int(parts[1])
            w = float(parts[2])
            src_list.append(s)
            dst_list.append(d)
            weights_list.append(w)
        except ValueError:
            print("Invalid numbers. Integers for IDs, float for weight.")

    # Seed Collection
    print("\nEnter Fraud Seeds (IDs separated by space):")
    seeds_input = input("> ").strip()
    raw_seeds = []
    if seeds_input:
        try:
            raw_seeds = [int(x) for x in seeds_input.split()]
        except ValueError:
            print("Invalid seeds. Proceeding with empty seed list.")

    return src_list, dst_list, weights_list, raw_seeds


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
        print("which network?")
        print("1 : test(6 nodes)")
        print("2 : btcAlpha")

        secchoice = get_valid_input(
            "Select option [1/2]: ",
            int,
            lambda x: x in [1, 2]
        )
        if secchoice == 1:
            file_path = "transactions.csv"
        else:
            file_path = "transactions_bitcoin_labeled.csv"


        try:
            print(f"\n[INFO] Loading {file_path}...")
            # Unpacking the new return values including maps
            src, dst, weights, n_nodes, labels, node_map, reverse_map = load_transactions(file_path)

            print(f"[INFO] Graph loaded.")
            print(f"       Unique Nodes: {n_nodes}")
            print(f"       Edges: {len(weights)}")

            # Extract seeds from labels (where label == 1)
            # Note: keys in labels are already mapped to internal indices
            fraud_seeds = [node for node, label in labels.items() if label == 1]
            print(f"       Fraud Seeds found in file: {len(fraud_seeds)}")

        except FileNotFoundError:
            print("Error: File not found.")
            sys.exit()
        except Exception as e:
            print(f"Error loading file: {e}")
            sys.exit()

    else:
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
    if labels:
        print("\n[EVALUATION] Precision at different k values:")
        print("-" * 50)

        # Define all possible k values
        k_values = [5, 10, 20, 30, 40, 50, 60]

        # Filter k values based on n_nodes
        # Example: if n_nodes=11, it shows k=5 and k=10
        valid_ks = [k for k in k_values if k < n_nodes]

        if not valid_ks and n_nodes > 0:
            # If graph is very small (e.g. n=3), just show the largest possible
            valid_ks = [n_nodes]

        for k in valid_ks:
            prec = precision_at_k(scores, labels, k)
            print(f"Precision@{k:2d}: {prec:.4f}")

        print("-" * 50)