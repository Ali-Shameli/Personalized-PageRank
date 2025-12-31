# src/gui/main_gui.py

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np


from src.data.data_loader import load_transactions, build_adj_matrix
from src.algorithms.ppr_power import make_personalization_vector, personalized_pagerank
from src.evaluation.metrics import precision_at_k


# یک state ساده سراسری برای نگهداری گراف فعلی
class AppState:
    def __init__(self) -> None:
        self.dataset_name: str | None = None
        self.src = None
        self.dst = None
        self.n_nodes: int | None = None
        self.labels: dict[int, int] | None = None
        self.A = None
        self.fraud_seeds: list[int] = []

        # نتایج آخرین اجرای PPR
        self.ppr_scores = None
        self.ppr_n_iter: int | None = None
        self.ppr_final_err: float | None = None
        self.ppr_precision_at_k: float | None = None
        self.ppr_k: int = 10


STATE = AppState()


def run_app() -> None:
    root = tk.Tk()
    root.title("Fraud Detection via Personalized PageRank")
    root.geometry("900x600")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    data_frame = ttk.Frame(notebook)
    run_frame = ttk.Frame(notebook)
    results_frame = ttk.Frame(notebook)

    notebook.add(data_frame, text="Data")
    notebook.add(run_frame, text="Run PPR")
    notebook.add(results_frame, text="Results")

    _build_data_tab(data_frame)

    # تب‌های Run / Results را فعلاً ساده نگه می‌داریم
    _build_run_tab(run_frame)
    _build_results_tab(results_frame)

    root.mainloop()


# ----------------- DATA TAB ----------------- #

def _build_data_tab(frame: ttk.Frame) -> None:
    """Tab for selecting and loading datasets."""
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)

    # عنوان
    title = ttk.Label(frame, text="Select and load a dataset", font=("Segoe UI", 12, "bold"))
    title.grid(row=0, column=0, columnspan=2, sticky="w", padx=16, pady=(16, 8))

    # انتخاب دیتاست
    ttk.Label(frame, text="Dataset:").grid(row=1, column=0, sticky="w", padx=16, pady=4)

    dataset_var = tk.StringVar(value="test")

    rb_test = ttk.Radiobutton(
        frame,
        text="Small test graph (data/test_small.csv)",
        variable=dataset_var,
        value="test",
    )
    rb_btc = ttk.Radiobutton(
        frame,
        text="Bitcoin Alpha (data/btcAlpha_small.csv)",
        variable=dataset_var,
        value="btc",
    )
    rb_test.grid(row=2, column=0, columnspan=2, sticky="w", padx=32, pady=2)
    rb_btc.grid(row=3, column=0, columnspan=2, sticky="w", padx=32, pady=2)

    # دکمه لود
    load_btn = ttk.Button(
        frame,
        text="Load dataset",
        command=lambda: _on_load_dataset(dataset_var, frame),
    )
    load_btn.grid(row=4, column=0, sticky="w", padx=16, pady=(12, 8))

    # بخش خلاصه گراف
    sep = ttk.Separator(frame, orient="horizontal")
    sep.grid(row=5, column=0, columnspan=2, sticky="ew", padx=16, pady=8)

    summary_label = ttk.Label(frame, text="Graph summary will appear here.")
    summary_label.grid(row=6, column=0, columnspan=2, sticky="w", padx=16, pady=(4, 4))

    # ذخیره‌ی label در frame تا بعداً آپدیت کنیم
    frame.summary_label = summary_label  # type: ignore[attr-defined]


def _on_load_dataset(dataset_var: tk.StringVar, frame: ttk.Frame) -> None:
    """Load selected dataset into global STATE and update summary."""
    choice = dataset_var.get()
    if choice == "test":
        path = "data/test_small.csv"
        name = "Small Test Graph"
    else:
        path = "data/btcAlpha_small.csv"
        name = "Bitcoin Alpha (small)"

    try:
        src, dst, n_nodes, labels = load_transactions(path)
        A = build_adj_matrix(src, dst, n_nodes)
        fraud_seeds = [node for node, lab in labels.items() if lab == 1]

        STATE.dataset_name = name
        STATE.src = src
        STATE.dst = dst
        STATE.n_nodes = n_nodes
        STATE.labels = labels
        STATE.A = A
        STATE.fraud_seeds = fraud_seeds

        n_edges = len(src)
        n_labels = len(labels)

        text = (
            f"Dataset: {name}\n"
            f"Nodes: {n_nodes}\n"
            f"Edges: {n_edges}\n"
            f"Labeled nodes: {n_labels}\n"
            f"Fraud seeds (label=1): {len(fraud_seeds)}"
        )

        summary_label: ttk.Label = frame.summary_label  # type: ignore[attr-defined]
        summary_label.config(text=text)

        messagebox.showinfo("Dataset loaded", f"{name} loaded successfully.")

    except Exception as e:
        messagebox.showerror("Error loading dataset", f"{type(e).__name__}: {e}")


# ----------------- PLACEHOLDERS FOR OTHER TABS ----------------- #

def _build_run_tab(frame: ttk.Frame) -> None:
    """Tab for configuring and running PPR."""
    frame.columnconfigure(0, weight=0)
    frame.columnconfigure(1, weight=1)

    title = ttk.Label(frame, text="Run Personalized PageRank", font=("Segoe UI", 12, "bold"))
    title.grid(row=0, column=0, columnspan=2, sticky="w", padx=16, pady=(16, 8))

    # پارامترها
    ttk.Label(frame, text="Alpha (damping):").grid(row=1, column=0, sticky="w", padx=16, pady=4)
    alpha_var = tk.StringVar(value="0.85")
    alpha_entry = ttk.Entry(frame, textvariable=alpha_var, width=10)
    alpha_entry.grid(row=1, column=1, sticky="w", padx=4, pady=4)

    ttk.Label(frame, text="Tolerance (tol):").grid(row=2, column=0, sticky="w", padx=16, pady=4)
    tol_var = tk.StringVar(value="1e-6")
    tol_entry = ttk.Entry(frame, textvariable=tol_var, width=10)
    tol_entry.grid(row=2, column=1, sticky="w", padx=4, pady=4)

    ttk.Label(frame, text="Max iterations:").grid(row=3, column=0, sticky="w", padx=16, pady=4)
    max_iter_var = tk.StringVar(value="100")
    max_iter_entry = ttk.Entry(frame, textvariable=max_iter_var, width=10)
    max_iter_entry.grid(row=3, column=1, sticky="w", padx=4, pady=4)

    ttk.Label(frame, text="K for Precision@K:").grid(row=4, column=0, sticky="w", padx=16, pady=4)
    k_var = tk.StringVar(value="10")
    k_entry = ttk.Entry(frame, textvariable=k_var, width=10)
    k_entry.grid(row=4, column=1, sticky="w", padx=4, pady=4)

    # دکمه Run
    run_btn = ttk.Button(
        frame,
        text="Run Personalized PageRank",
        command=lambda: _on_run_ppr(alpha_var, tol_var, max_iter_var, k_var, frame),
    )
    run_btn.grid(row=5, column=0, columnspan=2, sticky="w", padx=16, pady=(12, 8))

    # ناحیه وضعیت
    status_label = ttk.Label(frame, text="Status: waiting for input...")
    status_label.grid(row=6, column=0, columnspan=2, sticky="w", padx=16, pady=(8, 4))

    frame.status_label = status_label  # type: ignore[attr-defined]

def _on_run_ppr(
    alpha_var: tk.StringVar,
    tol_var: tk.StringVar,
    max_iter_var: tk.StringVar,
    k_var: tk.StringVar,
    frame: ttk.Frame,
) -> None:
    """Run PPR on the currently loaded dataset."""
    if STATE.A is None or STATE.n_nodes is None or STATE.labels is None:
        messagebox.showwarning("No dataset", "Please load a dataset from the Data tab first.")
        return

    try:
        alpha = float(alpha_var.get())
        tol = float(tol_var.get())
        max_iter = int(max_iter_var.get())
        k = int(k_var.get())
        if not (0.0 < alpha < 1.0):
            raise ValueError("alpha must be between 0 and 1")
        if max_iter <= 0 or k <= 0:
            raise ValueError("max_iter and K must be positive")
    except Exception as e:
        messagebox.showerror("Invalid parameters", f"{type(e).__name__}: {e}")
        return

    status_label: ttk.Label = frame.status_label  # type: ignore[attr-defined]
    status_label.config(text="Status: running PPR...")

    frame.update_idletasks()

    try:
        n_nodes = STATE.n_nodes
        assert n_nodes is not None

        # personalization
        p = make_personalization_vector(n_nodes, STATE.fraud_seeds)

        # run PPR
        scores, n_iter, final_err = personalized_pagerank(
            STATE.A,
            alpha=alpha,
            max_iter=max_iter,
            tol=tol,
            personalize=p,
        )

        # precision@k
        prec = precision_at_k(scores, STATE.labels, k)

        # ذخیره در STATE
        STATE.ppr_scores = scores
        STATE.ppr_n_iter = n_iter
        STATE.ppr_final_err = final_err
        STATE.ppr_precision_at_k = prec
        STATE.ppr_k = k

        status_label.config(
            text=(
                f"Status: done. iterations={n_iter}, "
                f"error={final_err:.2e}, Precision@{k}={prec:.4f}"
            )
        )

        messagebox.showinfo(
            "PPR finished",
            f"PPR finished in {n_iter} iterations.\n"
            f"Final L1 error: {final_err:.2e}\n"
            f"Precision@{k}: {prec:.4f}",
        )

    except Exception as e:
        status_label.config(text="Status: error.")
        messagebox.showerror("Error running PPR", f"{type(e).__name__}: {e}")

def _build_results_tab(frame: ttk.Frame) -> None:
    """Tab for displaying PPR results (top-K table + summary)."""
    frame.rowconfigure(1, weight=1)
    frame.columnconfigure(0, weight=1)

    title = ttk.Label(frame, text="PPR Results", font=("Segoe UI", 12, "bold"))
    title.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 4))

    # خلاصه
    summary_var = tk.StringVar(value="No results yet. Run PPR first.")
    summary_label = ttk.Label(frame, textvariable=summary_var, justify="left")
    summary_label.grid(row=1, column=0, sticky="nw", padx=16, pady=(0, 8))

    # جدول top-K
    columns = ("rank", "node", "score", "is_seed", "label")
    tree = ttk.Treeview(
        frame,
        columns=columns,
        show="headings",
        height=15,
    )
    tree.heading("rank", text="Rank")
    tree.heading("node", text="Node ID")
    tree.heading("score", text="Score")
    tree.heading("is_seed", text="Seed?")
    tree.heading("label", text="True label")

    tree.column("rank", width=60, anchor="center")
    tree.column("node", width=80, anchor="center")
    tree.column("score", width=120, anchor="e")
    tree.column("is_seed", width=70, anchor="center")
    tree.column("label", width=80, anchor="center")

    tree.grid(row=2, column=0, sticky="nsew", padx=16, pady=(0, 8))

    # اسکرول عمودی
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=2, column=1, sticky="ns", pady=(0, 8))

    # دکمه برای refresh (وقتی Run PPR تمام شد)
    refresh_btn = ttk.Button(
        frame,
        text="Refresh from last PPR run",
        command=lambda: _refresh_results(summary_var, tree),
    )
    refresh_btn.grid(row=3, column=0, sticky="w", padx=16, pady=(4, 12))

    # ذخیره برای استفاده بعدی
    frame.summary_var = summary_var   # type: ignore[attr-defined]
    frame.tree = tree                 # type: ignore[attr-defined]

def _refresh_results(summary_var: tk.StringVar, tree: ttk.Treeview) -> None:
    """Update summary label and top-K table from STATE."""
    if STATE.ppr_scores is None or STATE.n_nodes is None or STATE.labels is None:
        messagebox.showwarning(
            "No results",
            "No PPR results found. Please run PPR in the 'Run PPR' tab first.",
        )
        return

    scores = STATE.ppr_scores
    labels = STATE.labels
    fraud_seeds = set(STATE.fraud_seeds)
    k = STATE.ppr_k or 10

    n = len(scores)
    k_eff = min(k, n)
    sorted_nodes = np.argsort(scores)[::-1][:k_eff]

    # خلاصه
    n_iter = STATE.ppr_n_iter
    final_err = STATE.ppr_final_err
    prec = STATE.ppr_precision_at_k

    summary_lines = [
        f"Dataset: {STATE.dataset_name or 'N/A'}",
        f"Top-K shown: {k_eff}",
        f"Iterations: {n_iter}",
        f"Final L1 error: {final_err:.2e}" if final_err is not None else "Final L1 error: N/A",
        f"Precision@{k}: {prec:.4f}" if prec is not None else f"Precision@{k}: N/A",
    ]
    summary_var.set("\n".join(summary_lines))

    # پاک‌کردن جدول قبلی
    for item in tree.get_children():
        tree.delete(item)

    # پر کردن جدول
    for rank, node in enumerate(sorted_nodes, start=1):
        score = scores[node]
        is_seed = "Yes" if node in fraud_seeds else "No"
        true_label = labels.get(int(node), 0)
        tree.insert(
            "",
            "end",
            values=(
                rank,
                int(node),
                f"{score:.6f}",
                is_seed,
                true_label,
            ),
        )

