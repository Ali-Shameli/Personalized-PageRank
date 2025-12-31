# gui/pages/welcome_page.py
from __future__ import annotations

from tkinter import ttk


def build_welcome_page(frame: ttk.Frame, go_next) -> None:
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
        "Click start to continue."
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
        command=go_next,  # فعلاً فقط تابع ساده برای رفتن به صفحه بعد
    )
    start_btn.grid(row=2, column=1, sticky="we", padx=120, pady=(4, 4))
