# gui/app.py
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Dict

import numpy as np

from src.data.data_loader import load_transactions, build_adj_matrix
from src.algorithms.ppr_power import make_personalization_vector, personalized_pagerank
from src.evaluation.metrics import precision_at_k
from .pages.manual_page import build_manual_page

from .pages.welcome_page import build_welcome_page
from .pages.load_page import build_load_page
from .pages.run_page import build_run_page
from .pages.results_page import build_results_page
from .pages.how_page import build_how_page      # جدید
from .pages.about_page import build_about_page  # جدید
from .theme import apply_dark_theme
from .pages.visualization_page import build_visualization_page



class AppState:
    def __init__(self) -> None:
        self.data_path: str | None = None
        self.data_source: str | None = None

        self.scores = None          # np.array
        self.labels = None          # dict
        self.precision_at_50 = None # float
        self.reverse_map = None


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
        elif index == 4:                      # جدید
            build_how_page(frame, app=self)
        elif index == 5:                      # جدید
            build_about_page(frame, app=self)
        elif index == 6:
            build_visualization_page(frame, app=self)
        elif index == 7:
            build_manual_page(frame, app=self)

    def show_page(self, index: int) -> None:
    # برای Results و Visualization همیشه ریفرش کن
        if index in (3, 6) and index in self.frames:
            self.frames[index].destroy()
            del self.frames[index]

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
        """
        Execute the Personalized PageRank algorithm.
        This method orchestrates data loading, matrix building, and algorithm execution.
        """
        if not self.state.data_path:
            raise ValueError("No dataset selected")

        # Step 1: Load data
        # Note: We now unpack 6 return values, including 'weights' and 'rev_map'
        src, dst, weights, n_nodes, labels, rev_map = load_transactions(self.state.data_path)

        # Store the reverse map in the app state so the Results Page can use it later
        self.state.reverse_map = rev_map

        print(f"Graph loaded successfully: {n_nodes} nodes (Weighted & Mapped Mode)")

        # Step 2: Build the weighted adjacency matrix
        # We pass the 'weights' array to the builder function
        A = build_adj_matrix(src, dst, weights, n_nodes)

        # Step 3: Prepare personalization vector (Fraud Seeds)
        # Identify nodes labeled as fraud (label=1)
        fraud_seeds = [node for node, lab in labels.items() if lab == 1]
        p = make_personalization_vector(n_nodes, fraud_seeds)

        # Step 4: Run the algorithm
        result = personalized_pagerank(
            A,
            alpha=alpha,
            max_iter=max_iter,
            tol=tol,
            personalize=p,
        )

        # Handle result unpacking (in case future implementations return tuples)
        if isinstance(result, tuple):
            scores = result[0]
        else:
            scores = result

        # Step 5: Evaluate Precision@50
        prec50 = precision_at_k(scores, labels, k=50)

        # Step 6: Update state with results
        self.state.scores = scores
        self.state.labels = labels
        self.state.precision_at_50 = prec50



def run_app() -> None:
    app = WizardApp()
    app.mainloop()
