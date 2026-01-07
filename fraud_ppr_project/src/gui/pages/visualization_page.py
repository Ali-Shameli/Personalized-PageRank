from __future__ import annotations

from tkinter import ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



def build_visualization_page(frame: ttk.Frame, app) -> None:
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(2, weight=1)

    title = ttk.Label(
        frame,
        text="4. Visualization",
        style="Title.TLabel",
        anchor="w",
    )
    title.grid(row=0, column=0, sticky="we", padx=24, pady=(24, 8))

    info = ttk.Label(
        frame,
        text=(
            "Histogram of Personalized PageRank scores.\n"
            "This helps you see how suspicion scores are distributed "
            "across all nodes."
        ),
        style="Small.TLabel",
        anchor="nw",
        justify="left",
        wraplength=760,
    )
    info.grid(row=1, column=0, sticky="nw", padx=24, pady=(0, 8))

    # --- Chart area ---
    scores = app.state.scores
    fig = Figure(figsize=(5, 3), dpi=100)

    ax = fig.add_subplot(111)
    if scores is None:
        ax.text(
            0.5,
            0.5,
            "No scores available.\nRun the analysis first.",
            ha="center",
            va="center",
        )
        ax.set_axis_off()
    else:
        ax.hist(scores, bins=50, color="#4e79a7")
        ax.set_xlabel("Personalized PageRank score")
        ax.set_ylabel("Number of nodes")
        ax.set_title("Score distribution")

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=2, column=0, sticky="nsew", padx=24, pady=(8, 8))

    # --- Bottom bar ---
    button_bar = ttk.Frame(frame)
    button_bar.grid(row=3, column=0, sticky="e", padx=24, pady=24)

    back_btn = ttk.Button(
        button_bar,
        text="Back",
        command=lambda: app.show_page(3),
    )
    back_btn.pack(side="right")
