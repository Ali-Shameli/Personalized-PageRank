# src/gui/main_gui.py

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# بعداً این‌ها را واقعا استفاده می‌کنیم
from src.data.data_loader import load_transactions, build_adj_matrix
from src.algorithms.ppr_power import make_personalization_vector, personalized_pagerank
from src.evaluation.metrics import precision_at_k


def run_app() -> None:
    """Start the main Tkinter application window."""
    root = tk.Tk()
    root.title("Fraud Detection via Personalized PageRank")
    root.geometry("900x600")

    # تب‌ها
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # تب 1: Data
    data_frame = ttk.Frame(notebook)
    notebook.add(data_frame, text="Data")

    # تب 2: Run
    run_frame = ttk.Frame(notebook)
    notebook.add(run_frame, text="Run PPR")

    # تب 3: Results
    results_frame = ttk.Frame(notebook)
    notebook.add(results_frame, text="Results")

    _build_data_tab(data_frame)
    _build_run_tab(run_frame)
    _build_results_tab(results_frame)

    root.mainloop()


# ----------------- تب‌ها (فعلاً ساده) ----------------- #

def _build_data_tab(frame: ttk.Frame) -> None:
    label = ttk.Label(
        frame,
        text="در این تب بعداً انتخاب دیتاست و خلاصه گراف را می‌گذاریم.",
    )
    label.pack(padx=20, pady=20, anchor="w")


def _build_run_tab(frame: ttk.Frame) -> None:
    label = ttk.Label(
        frame,
        text="اینجا تنظیمات الگوریتم (alpha, tol, ... ) و دکمه Run خواهد بود.",
    )
    label.pack(padx=20, pady=20, anchor="w")


def _build_results_tab(frame: ttk.Frame) -> None:
    label = ttk.Label(
        frame,
        text="در این تب جدول Top-K و Precision@K و خلاصه نتایج نمایش داده می‌شود.",
    )
    label.pack(padx=20, pady=20, anchor="w")
