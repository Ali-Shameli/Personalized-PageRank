# main.py
import numpy as np
from data_loader import load_transactions, build_adj_matrix
from ppr import make_personalization_vector, personalized_pagerank
from evaluate import precision_at_k

# 1. Load data
src, dst, n_nodes, labels = load_transactions("transactions.csv")

# 2. Build graph
A = build_adj_matrix(src, dst, n_nodes)

# 3. Define fraud seed set (e.g., nodes labeled 1)
fraud_seeds = [node for node, lab in labels.items() if lab == 1]

# 4. Personalization vector
p = make_personalization_vector(n_nodes, fraud_seeds)

# 5. Run PPR
scores = personalized_pagerank(A, alpha=0.85, max_iter=100, tol=1e-6,
                               personalize=p)

# Sort nodes by PPR score in descending order
sorted_nodes = np.argsort(scores)[::-1]

print("\nTop suspicious nodes (by PPR score):")
for rank, node in enumerate(sorted_nodes):
    print(f"Rank {rank+1}: node {node}, score={scores[node]:.4f}")

print("Fraud seeds:", fraud_seeds)
print("Personalization vector p:", p)
print("Scores:", scores)

# 6. Evaluate
for k in [10, 50, 100]:
    prec = precision_at_k(scores, labels, k)
    print(f"Precision@{k}: {prec:.3f}")
