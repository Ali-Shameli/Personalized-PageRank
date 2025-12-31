# src/gui/main_gui.py

import tkinter as tk
from tkinter import ttk, messagebox

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
    label = ttk.Label(
        frame,
        text="Run tab: در مرحله بعد تنظیمات الگوریتم و دکمه Run را اینجا اضافه می‌کنیم.",
    )
    label.pack(padx=20, pady=20, anchor="w")


def _build_results_tab(frame: ttk.Frame) -> None:
    label = ttk.Label(
        frame,
        text="Results tab: در مرحله بعد جدول Top-K و Precision@K اینجا نمایش داده می‌شود.",
    )
    label.pack(padx=20, pady=20, anchor="w")
