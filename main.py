# main.py
import numpy as np
import sys
from data_loader import load_transactions, build_adj_matrix
from ppr import make_personalization_vector, personalized_pagerank
from evaluate import precision_at_k


def get_valid_input(prompt, parse_func, condition=lambda x: True, error_msg="Invalid input. Please try again."):
    """
    Helper function to ensure user input is valid and matches expected criteria.
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
    Collects graph edges (src, dst, weight) and seeds from user manually.
    """
    print("\n--- Manual Graph Data Entry ---")
    print("Format for each edge: source destination weight")
    print("Example: 0 1 50.5")
    print("Type 'end' to finish adding edges.\n")

    src_list = []
    dst_list = []
    weights_list = []

    # 1. Edge Collection Loop
    while True:
        line = input("Edge (src dst weight) or 'end': ").strip()
        if line.lower() == 'end':
            if len(src_list) == 0:
                print("Error: No edges entered! Please add at least one edge.")
                continue
            break

        parts = line.split()
        if len(parts) != 3:
            print("Error: Please enter 3 values (src, dst, weight).")
            continue

        try:
            s, d = int(parts[0]), int(parts[1])
            w = float(parts[2])

            if s < 0 or d < 0 or w <= 0:
                print("Error: Node IDs must be non-negative and weight must be positive.")
                continue

            src_list.append(s)
            dst_list.append(d)
            weights_list.append(w)
            print(f"Edge {s} -> {d} with weight {w} recorded.")

        except ValueError:
            print("Error: Node IDs must be integers and weight must be a number.")

    # Determine total number of unique nodes based on entries
    n_nodes = max(max(src_list), max(dst_list)) + 1
    print(f"\nTotal nodes detected: {n_nodes} (indexed 0 to {n_nodes - 1})")

    # 2. Fraud Seed Collection
    print("\nEnter initial fraud seed nodes (these will be treated as known frauds).")
    print("Separate IDs with space. Example: 1 5")

    def parse_seeds(inp):
        return [int(x) for x in inp.split()]

    def validate_seeds(seeds):
        return all(0 <= node < n_nodes for node in seeds) and len(seeds) > 0

    fraud_seeds = get_valid_input(
        prompt="Fraud seeds: ",
        parse_func=parse_seeds,
        condition=validate_seeds,
        error_msg=f"Error: Seed IDs must be between 0 and {n_nodes - 1}."
    )

    return np.array(src_list), np.array(dst_list), np.array(weights_list), n_nodes, fraud_seeds


def main():
    print("=== Fraud Detection System (PPR-based) ===")
    print("1. Load data from 'transactions.csv'")
    print("2. Enter graph data manually")

    choice = get_valid_input(
        prompt="Select an option (1 or 2): ",
        parse_func=int,
        condition=lambda x: x in [1, 2],
        error_msg="Please enter 1 or 2."
    )

    labels = {}  # Dictionary to store ground truth (node: label)

    if choice == 1:
        print("\n[INFO] Loading data from CSV...")
        try:
            # Assuming data_loader is updated to return weights and labels
            src, dst, weights, n_nodes, labels = load_transactions("transactions.csv")

            # Identify seed set (where label is 1)
            fraud_seeds = [node for node, lab in labels.items() if lab == 1]
            print(f"[INFO] Loaded {n_nodes} nodes and {len(fraud_seeds)} initial seeds.")

        except FileNotFoundError:
            print("Error: 'transactions.csv' not found!")
            sys.exit(1)
        except Exception as e:
            print(f"Error during file loading: {e}")
            sys.exit(1)

    else:
        # Manual Mode
        src, dst, weights, n_nodes, fraud_seeds = get_manual_graph_data()

        # In Manual mode, we assume the provided seeds are the only known frauds
        # This allows us to calculate Precision for the manual graph as well
        labels = {node: 0 for node in range(n_nodes)}
        for seed in fraud_seeds:
            labels[seed] = 1

        print("\n[INFO] Manual graph constructed successfully.")

    # --- PPR Algorithm Execution ---

    # 1. Build the weighted Adjacency Matrix
    A = build_adj_matrix(src, dst, weights, n_nodes)

    # 2. Create the personalization vector (Teleportation distribution)
    p = make_personalization_vector(n_nodes, fraud_seeds)

    # 3. Compute Personalized PageRank scores
    print("\n[INFO] Computing Personalized PageRank...")
    scores = personalized_pagerank(A, alpha=0.85, max_iter=100, tol=1e-6, personalize=p)

    # 4. Results Presentation
    sorted_nodes = np.argsort(scores)[::-1]

    print("\n[RESULTS] Most suspicious nodes:")
    print("-" * 50)
    for rank, node in enumerate(sorted_nodes):
        is_seed = " (Known Seed)" if node in fraud_seeds else ""
        print(f"Rank {rank + 1:2d}: Node {node:4d} | Score: {scores[node]:.6f}{is_seed}")

        # Limit the output for large graphs from CSV
        if choice == 1 and rank >= 19:
            print("... (showing top 20 results)")
            break

    print("-" * 50)

    # 5. Evaluation
    # Shows how many of the top-k results are actually in our fraud list
    print("\n[EVALUATION] Model Performance Metrics (Precision@k):")
    # For small manual graphs, k should not exceed total node count
    test_ks = [5, 10, 20]
    for k in test_ks:
        if k <= n_nodes or choice == 1:
            prec = precision_at_k(scores, labels, k)
            print(f"Precision@{k}: {prec:.3f}")


if __name__ == "__main__":
    main()