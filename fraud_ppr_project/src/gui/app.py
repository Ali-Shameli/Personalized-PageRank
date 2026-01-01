from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Dict

import numpy as np

from src.data.data_loader import load_transactions, build_adj_matrix
from src.algorithms.ppr_power import make_personalization_vector, personalized_pagerank
from src.evaluation.metrics import precision_at_k

from .pages.welcome_page import build_welcome_page
from .pages.load_page import build_load_page
from .pages.run_page import build_run_page
from .pages.results_page import build_results_page
from .theme import apply_dark_theme


class AppState:
    def __init__(self) -> None:
        self.data_path: str | None = None
        self.data_source: str | None = None

        self.scores = None          # np.array
        self.labels = None          # dict
        self.precision_at_50 = None # float


class WizardApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.state = AppState()

        self.title("Fraud Detection via Personalized PageRank")
        self.geometry("900x600")
        self.minsize(800, 500)

        self.style = apply_dark_theme(self)

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self._container = container
        self.frames: Dict[int, ttk.Frame] = {}

        self._create_page(0)
        self.show_page(0)

    # ---------- صفحات ----------

    def _create_page(self, index: int) -> None:
        if index in self.frames:
            return

        frame = ttk.Frame(self._container)
        frame.grid(row=0, column=0, sticky="nsew")
        self.frames[index] = frame

        if index == 0:
            build_welcome_page(frame, app=self)
        elif index == 1:
            build_load_page(frame, app=self)
        elif index == 2:
            build_run_page(frame, app=self)
        elif index == 3:
            build_results_page(frame, app=self)

    def show_page(self, index: int) -> None:
        self._create_page(index)
        frame = self.frames[index]
        frame.tkraise()

    def show_how_it_works(self) -> None:
        tk.messagebox.showinfo(
            "How it works",
            "This will explain the Personalized PageRank-based fraud detection.",
        )

    def show_about(self) -> None:
        tk.messagebox.showinfo(
            "About",
            "Fraud Detection via Personalized PageRank.\nCourse project.",
        )

    def run_ppr(self, alpha: float, max_iter: int, tol: float) -> None:
        if not self.state.data_path:
            raise ValueError("No dataset selected")

        src, dst, n_nodes, labels = load_transactions(self.state.data_path)
        # print("DEBUG shapes:", type(src), src.shape, type(dst), dst.shape, n_nodes, len(labels))

        A = build_adj_matrix(src, dst, n_nodes)
        # print("DEBUG A shape:", A.shape, "nnz:", A.nnz)

        fraud_seeds = [node for node, lab in labels.items() if lab == 1]
        # print("DEBUG fraud_seeds length:", len(fraud_seeds))

        p = make_personalization_vector(n_nodes, fraud_seeds)

        # print("DEBUG: before personalized_pagerank")
        result = personalized_pagerank(
            A,
            alpha=alpha,
            max_iter=max_iter,
            tol=tol,
            personalize=p,
        )
        # اگر فقط یک آرایه برگرداند، همان را بگیر؛ اگر tuple بود، جزء اولش را بگیر
        if isinstance(result, tuple):
            scores = result[0]
        else:
            scores = result
        # print("DEBUG: after personalized_pagerank, before precision_at_k")
        # print("DEBUG type(scores):", type(scores))
        # print("DEBUG scores shape / first element:", getattr(scores, "shape", None), scores[0] if hasattr(scores, "__getitem__") else None)

        prec50 = precision_at_k(scores, labels, k=50)
        # print("DEBUG: after precision_at_k")

        self.state.scores = scores
        self.state.labels = labels
        self.state.precision_at_50 = prec50

        
        # print("DEBUG saved scores len:", len(scores), "labels len:", len(labels), "prec50:", prec50)


def run_app() -> None:
    app = WizardApp()
    app.mainloop()
