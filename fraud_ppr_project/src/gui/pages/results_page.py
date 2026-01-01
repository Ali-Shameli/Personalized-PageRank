from __future__ import annotations

from tkinter import ttk


def build_results_page(frame: ttk.Frame, app) -> None:
    """Page 3: placeholder for results."""
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)

    label = ttk.Label(
        frame,
        text="3. Results\n\nResults will be shown here after running PPR.",
        anchor="center",
        justify="center",
        style="Title.TLabel",
    )
    label.grid(row=0, column=0, sticky="nsew", padx=24, pady=24)
