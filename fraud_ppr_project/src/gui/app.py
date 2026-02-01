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
from .pages.add_edge_page import build_add_edge_page



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
        elif index == 8:
            build_add_edge_page(frame, app=self)

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

    def run_ppr(self, alpha: float, weighted: bool = True, algorithm: str = "power",
            # Optional parameters for Power iteration
            max_iter: int = 100, tol: float = 1e-6,
            # Optional parameters for Monte Carlo  
            num_walks: int = 1000, max_steps: int = 50) -> None:
        """
        Executes the Personalized PageRank algorithm.
        Handles data loading (from manual entry or file), matrix construction,
        and result calculation.
        """

        # --- Step 1: Determine Data Source and Load Data ---
        if self.state.data_source == "manual":
            # Retrieve pre-parsed data directly from the application state (RAM)
            # This data was processed in the Manual Page
            src, dst, weights, n_nodes, labels, rev_map = self.state.manual_data
            print(f"Using Manually Entered Data. Total Nodes: {n_nodes}")

        else:
            # Default behavior: Load from the selected CSV file
            if not self.state.data_path:
                raise ValueError("No dataset selected. Please go back and select a file.")

            # Load and map the data using the data loader module
            src, dst, weights, n_nodes, labels, rev_map = load_transactions(self.state.data_path)
            print(f"Graph loaded from file: {self.state.data_path}. Total Nodes: {n_nodes}")

        # --- Step 2: Handle weighted/unweighted mode ---
        if not weighted:
            print("Running in UNWEIGHTED mode: all edge weights set to 1.0")
            weights = np.ones_like(weights, dtype=float)  # همه وزن‌ها = ۱
        else:
            print("Running in WEIGHTED mode: using original edge weights")

        # --- Step 3: Store Metadata ---
        # Save the reverse mapping dictionary to the state.
        # This is crucial for the Results Page to display real Node IDs instead of internal indices.
        self.state.reverse_map = rev_map

        # --- Step 4: Build Adjacency Matrix ---
        # Build the sparse weighted adjacency matrix
        A = build_adj_matrix(src, dst, weights, n_nodes)

        # --- Step 5: Prepare Personalization Vector ---
        # Identify seed nodes (confirmed fraudsters) from the labels dictionary
        fraud_seeds = [node for node, lab in labels.items() if lab == 1]

        # Create the personalization vector (distribution) based on seeds
        p = make_personalization_vector(n_nodes, fraud_seeds)

        # --- Step 6: Run the Algorithm ---
        print(f"Starting PPR execution (algorithm={algorithm}, alpha={alpha})...")
        
        if algorithm == "power":
            # Use Power iteration algorithm
            from src.algorithms.ppr_power import personalized_pagerank as ppr_power
            result = ppr_power(
                A,
                alpha=alpha,
                max_iter=max_iter,
                tol=tol,
                personalize=p,
            )
        elif algorithm == "monte_carlo":
            # Use Monte Carlo algorithm
            from src.algorithms.ppr_monte_carlo import personalized_pagerank_monte_carlo
            # Note: Monte Carlo parameters may be different
            result = personalized_pagerank_monte_carlo(
                A,
                alpha=alpha,
                personalize=p,
                # These parameters should come from GUI
                num_walks= num_walks,  
                max_steps= max_steps
            )
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        
        # Unpack the result (some implementations return a tuple of scores and iterations)
        if isinstance(result, tuple):
            scores = result[0]
        else:
            scores = result

        # --- Step 7: Calculate Metrics ---
        # Calculate Precision@50 to evaluate performance (if ground truth labels exist)
        prec50 = precision_at_k(scores, labels, k=50)

        # --- Step 8: Update Application State ---
        # Store results in the state to be accessed by the Results Page
        self.state.scores = scores
        self.state.labels = labels
        self.state.precision_at_50 = prec50
        self.state.weighted = weighted  # Store the mode for reference
        self.state.algorithm = algorithm

        # === NEW: Store data for incremental updates ===
        self.state.adj_matrix = A  # CSR sparse matrix
        self.state.personalization = p  # personalization vector
        self.state.alpha = alpha  # damping factor
        self.state.compact_to_real = rev_map  # reverse mapping
        self.state.real_to_compact = {v: k for k, v in rev_map.items()}  # forward mapping

    # در کلاس App (فایل app.py)

    def run_incremental_ppr(self, new_edges):
        """
        new_edges: list of (src, dst, weight)
        """
        import tkinter.messagebox as messagebox  # ✅ این خط رو اضافه کن
        if self.state.scores is None or self.state.adj_matrix is None:
            messagebox.showerror("Error", "No existing graph to update.")
            return

        from src.algorithms.ppr_incremental import update_ppr_incremental

        try:
            # فراخوانی الگوریتم جدید
            new_adj, new_scores = update_ppr_incremental(
                adj_matrix=self.state.adj_matrix,
                old_scores=self.state.scores,
                personalization_dict=self.state.personalization, # فرض: این را در state داری
                alpha=0.85,  # یا مقداری که در state ذخیره کردی
                new_edges=new_edges
            )

            # آپدیت State
            self.state.adj_matrix = new_adj
            self.state.scores = new_scores
            
            # (اختیاری) اگر نودهای جدید اضافه شدند، لیبل‌هایشان را 0 (unknown) بگذار
            if len(new_scores) > len(self.state.labels):
                # دیکشنری لیبل‌ها را آپدیت کن ولی چون دیکشنری است خودش هندل می‌شود
                # فقط اگر لیستی داری باید حواست باشد.
                pass
            
            self.refresh_results_page()
            messagebox.showinfo("Success", f"Updated scores with {len(new_edges)} new edge(s).")
            
        except Exception as e:
            messagebox.showerror("Error", f"Incremental update failed:{e}")
        
    def refresh_results_page(self):
        """رفرش صفحه نتایج"""
        # پاک کردن صفحه نتایج اگر وجود دارد
        if 3 in self.frames:
            self.frames[3].destroy()
            del self.frames[3]
        
        # ساخت مجدد صفحه
        self._create_page(3)
        
        # نمایش صفحه
        self.show_page(3)
        
        print("Results page refreshed successfully")
        
    print("Analysis completed successfully.")


def run_app() -> None:
    app = WizardApp()
    app.mainloop()
