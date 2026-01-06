# src/gui/pages/welcome_page.py
from __future__ import annotations

from tkinter import ttk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.app import WizardApp  # فقط برای type hints، در runtime استفاده نمی‌شود


def build_welcome_page(frame: ttk.Frame, app) -> None:
    """Build the centered welcome page UI inside the given frame."""
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=2)
    frame.columnconfigure(2, weight=1)

    for r in range(6):
        frame.rowconfigure(r, weight=0)
    frame.rowconfigure(5, weight=1)

    title = ttk.Label(
        frame,
        text="Fraud Detection via Personalized PageRank",
        style="Title.TLabel",
        anchor="center",
    )
    title.grid(row=0, column=1, sticky="we", padx=16, pady=(32, 8))

    desc_text = (
        "Analyze transaction graphs and highlight potentially fraudulent nodes\n"
        "using Personalized PageRank and the 'guilt by association' principle.\n\n"
        "Start the 3-step wizard to load data and run the analysis."
    )
    desc = ttk.Label(
        frame,
        text=desc_text,
        justify="center",
        style="Small.TLabel",
        anchor="center",
    )
    desc.grid(row=1, column=1, sticky="we", padx=16, pady=(0, 24))

    start_btn = ttk.Button(
        frame,
        text="Start analysis",
        style="Nav.TButton",
        command=lambda: app.show_page(1),  # رفتن به صفحه Load
    )
    start_btn.grid(row=2, column=1, sticky="we", padx=120, pady=(4, 4))
    
    how_btn = ttk.Button(
        frame,
        text="How it works",
        style="Nav.TButton",
        command=lambda: app.show_page(4),
    )
    how_btn.grid(row=3, column=1, sticky="we", padx=120, pady=(4, 4))

    about_btn = ttk.Button(
        frame,
        text="About",
        style="Nav.TButton",
        command=lambda: app.show_page(5),
    )
    about_btn.grid(row=4, column=1, sticky="we", padx=120, pady=(4, 4))
