from __future__ import annotations

import numpy as np
from tkinter import ttk, messagebox

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def build_visualization_page(frame: ttk.Frame, app) -> None:
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(3, weight=1)

    # --- عنوان ---
    title = ttk.Label(
        frame,
        text="4. Visualization",
        style="Title.TLabel",
        anchor="w",
    )
    title.grid(row=0, column=0, sticky="we", padx=24, pady=(24, 8))

    # --- نوار کنترل N ---
    control_bar = ttk.Frame(frame)
    control_bar.grid(row=1, column=0, sticky="we", padx=24, pady=(0, 8))
    control_bar.columnconfigure(2, weight=1)

    n_label = ttk.Label(
        control_bar,
        text="Top-N nodes for histogram:",
        style="Small.TLabel",
    )
    n_label.grid(row=0, column=0, sticky="w")

    n_entry = ttk.Entry(control_bar, width=6)
    n_entry.insert(0, "100")
    n_entry.grid(row=0, column=1, sticky="w", padx=(4, 8))

    info = ttk.Label(
        frame,
        text=(
            "Histogram of Personalized PageRank scores for the top-N nodes.\n"
            "N should be between 1 and the total number of nodes."
        ),
        style="Small.TLabel",
        anchor="nw",
        justify="left",
        wraplength=760,
    )
    info.grid(row=2, column=0, sticky="nw", padx=24, pady=(0, 4))

    # --- Chart area (جای خالی که بعداً پر می‌کنیم) ---
    fig = Figure(figsize=(5, 3), dpi=100)
    ax = fig.add_subplot(111)

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=3, column=0, sticky="nsew", padx=24, pady=(4, 8))

    scores = app.state.scores

    def refresh_histogram() -> None:
        nonlocal scores, ax

        if scores is None:
            ax.clear()
            ax.text(
                0.5,
                0.5,
                "No scores available.\nRun the analysis first.",
                ha="center",
                va="center",
            )
            ax.set_axis_off()
            canvas.draw()
            return

        n_total = len(scores)

        # خواندن N با ولیدیشن
        try:
            n_value = int(n_entry.get())
        except ValueError:
            messagebox.showinfo("Top-N", "Please enter a valid integer for N.")
            n_entry.delete(0, "end")
            n_entry.insert(0, "100")
            n_value = 100

        if n_value <= 0:
            messagebox.showinfo("Top-N", "N must be at least 1.")
            n_value = 1
        if n_value > n_total:
            messagebox.showinfo(
                "Top-N",
                f"N is too large. Using N = {n_total} (total number of nodes).",
            )
            n_value = n_total

        n_entry.delete(0, "end")
        n_entry.insert(0, str(n_value))

        order = np.argsort(scores)[::-1]
        top_idx = order[:n_value]
        top_scores = scores[top_idx]

        ax.clear()
        ax.hist(top_scores, bins=20, color="#4e79a7")
        ax.set_xlabel("Personalized PageRank score (top-N)")
        ax.set_ylabel("Number of nodes")
        ax.set_title(f"Score distribution for top {n_value} nodes")
        ax.set_axis_on()
        canvas.draw()

    # دکمه Apply N
    apply_btn = ttk.Button(
        control_bar,
        text="Apply N",
        style="Nav.TButton",
        command=refresh_histogram,
    )
    apply_btn.grid(row=0, column=2, sticky="e")

    # --- نوار پایین ---
    button_bar = ttk.Frame(frame)
    button_bar.grid(row=4, column=0, sticky="e", padx=24, pady=24)

    back_btn = ttk.Button(
        button_bar,
        text="Back",
        command=lambda: app.show_page(3),
    )
    back_btn.pack(side="right")

    # بار اول
    refresh_histogram()
