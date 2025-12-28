from evaluate import precision_at_k


def dynamic_evaluation(labels, n_nodes, scores):
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
