from __future__ import annotations

import numpy as np
from tkinter import ttk


def build_results_page(frame: ttk.Frame, app) -> None:
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=0)
    frame.rowconfigure(1, weight=1)

    title = ttk.Label(
        frame,
        text="3. Results",
        style="Title.TLabel",
        anchor="w",
    )
    title.grid(row=0, column=0, sticky="we", padx=24, pady=(24, 8))

    info = ttk.Label(
        frame,
        text="Top suspicious nodes by PPR score (top 20).",
        style="Small.TLabel",
        anchor="w",
        justify="left",
    )
    info.grid(row=1, column=0, sticky="we", padx=24, pady=(0, 8))

    tree = ttk.Treeview(
        frame,
        columns=("rank", "node", "score", "label"),
        show="headings",
        height=15,
    )
    tree.heading("rank", text="Rank")
    tree.heading("node", text="Node ID")
    tree.heading("score", text="Score")
    tree.heading("label", text="Label")

    tree.column("rank", width=60, anchor="center")
    tree.column("node", width=80, anchor="center")
    tree.column("score", width=120, anchor="e")
    tree.column("label", width=80, anchor="center")

    tree.grid(row=2, column=0, sticky="nsew", padx=24, pady=(0, 24))
    frame.rowconfigure(2, weight=1)

    # پرکردن جدول بر اساس state
    scores = app.state.scores
    labels = app.state.labels

    if scores is None:
        return

    n = len(scores)
    order = np.argsort(scores)[::-1]  # نزولی
    top_k = order[: min(20, n)]

    for idx, node in enumerate(top_k, start=1):
        score = scores[node]
        lab = labels.get(int(node), 0)
        tree.insert(
            "", "end",
            values=(idx, int(node), f"{score:.6f}", lab),
        )

    # precision@50 اگر موجود است
    if app.state.precision_at_50 is not None:
        info.configure(
            text=(
                "Top suspicious nodes by PPR score (top 20).\n"
                f"Precision@50: {app.state.precision_at_50:.3f}"
            )
        )
