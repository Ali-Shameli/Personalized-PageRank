import sys

from data_loader import load_transactions
from inputValidation import get_valid_input


def provide_data_from_file(src, dst, weights, n_nodes, labels, node_map, reverse_map, fraud_seeds):
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

        return src, dst, weights, n_nodes, labels, node_map, reverse_map, fraud_seeds

    except FileNotFoundError:
        print("Error: File not found.")
        sys.exit()
    except Exception as e:
        print(f"Error loading file: {e}")
        sys.exit()
