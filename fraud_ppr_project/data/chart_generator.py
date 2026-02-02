import matplotlib.pyplot as plt
import os


def plot_benchmark_results():
    edges = [1000, 5000, 10000, 15000, 20000, 25000]

    time_a015 = [2.25, 2.41, 2.82, 3.22, 3.68, 4.16]
    time_a05 = [1.45, 1.72, 2.05, 2.36, 2.72, 3.08]
    time_a085 = [1.07, 1.32, 1.46, 1.72, 1.98, 2.22]

    plt.figure(figsize=(10, 6), dpi=100)

    plt.plot(edges, time_a015, marker='o', linestyle='-', linewidth=2, label=r'$\alpha=0.15$')
    plt.plot(edges, time_a05, marker='s', linestyle='--', linewidth=2, label=r'$\alpha=0.5$')
    plt.plot(edges, time_a085, marker='^', linestyle='-.', linewidth=2, label=r'$\alpha=0.85$')

    plt.title(r"Impact of Damping Factor ($\alpha$) on Scalability", fontsize=14, fontweight='bold')
    plt.xlabel("Number of Edges", fontsize=12)
    plt.ylabel("Execution Time (microseconds)", fontsize=12)

    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend(title="Damping Factor", fontsize=10)
    plt.tight_layout()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(current_dir, "scalability_chart_final.png")

    plt.savefig(save_path)
    print(f"Chart saved: {save_path}")
    plt.show()


if __name__ == "__main__":
    plot_benchmark_results()