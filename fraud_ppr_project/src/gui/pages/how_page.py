# src/gui/pages/how_page.py
from __future__ import annotations

from tkinter import ttk


def build_how_page(frame: ttk.Frame, app) -> None:
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(2, weight=1)

    # عنوان اصلی
    title = ttk.Label(
        frame,
        text="How it works",
        style="Title.TLabel",
        anchor="w",
    )
    title.grid(row=0, column=0, sticky="we", padx=24, pady=(24, 4))

    # زیرتیتر
    subtitle = ttk.Label(
        frame,
        text="Graph-based fraud detection in four steps.",
        style="Small.TLabel",
        anchor="w",
        justify="left",
    )
    subtitle.grid(row=1, column=0, sticky="we", padx=24, pady=(0, 16))

    # کادر مراحل
    pipeline = ttk.LabelFrame(frame, text="Analysis pipeline")
    pipeline.grid(row=2, column=0, sticky="nwe", padx=24, pady=(0, 16))
    pipeline.columnconfigure(0, weight=1)

    step_text = (
        "1) Build the transaction graph.\n"
        "   Each node is an account / address and each edge is a transaction.\n\n"
        "2) Mark known fraud nodes.\n"
        "   These labels come from historical investigations or external data.\n\n"
        "3) Run Personalized PageRank from fraud seeds.\n"
        "   The algorithm spreads \"suspicion\" over the graph and gives each "
        "node a score based on its proximity to fraud.\n\n"
        "4) Rank nodes and evaluate Precision@K.\n"
        "   We sort nodes by score, focus on the top-K most suspicious ones "
        "and measure how many of them are truly fraudulent."
    )

    steps_label = ttk.Label(
        pipeline,
        text=step_text,
        style="Small.TLabel",
        anchor="nw",
        justify="left",
        wraplength=760,
    )
    steps_label.grid(row=0, column=0, sticky="nw", padx=12, pady=12)

    # بخش Precision@K
    pk_frame = ttk.LabelFrame(frame, text="What does Precision@K mean?")
    pk_frame.grid(row=3, column=0, sticky="nwe", padx=24, pady=(0, 16))
    pk_frame.columnconfigure(0, weight=1)

    pk_text = (
        "Precision@K answers a simple question:\n"
        "If an analyst only investigates the top-K suspicious nodes, "
        "what fraction of them are actually fraud?\n\n"
        "High Precision@K means the model concentrates true fraud cases "
        "near the top of the ranking, which is crucial when investigation "
        "capacity is limited."
    )

    pk_label = ttk.Label(
        pk_frame,
        text=pk_text,
        style="Small.TLabel",
        anchor="nw",
        justify="left",
        wraplength=760,
    )
    pk_label.grid(row=0, column=0, sticky="nw", padx=12, pady=12)

    # نوار دکمه
    button_bar = ttk.Frame(frame)
    button_bar.grid(row=4, column=0, sticky="e", padx=24, pady=24)

    back_btn = ttk.Button(
        button_bar,
        text="Back",
        command=lambda: app.show_page(0),
    )
    back_btn.pack(side="right")
