from __future__ import annotations

import webbrowser
from tkinter import ttk


def build_about_page(frame: ttk.Frame, app) -> None:
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(3, weight=1)

    title = ttk.Label(
        frame,
        text="Fraud Detection via Personalized PageRank",
        style="Title.TLabel",
        anchor="w",
    )
    title.grid(row=0, column=0, sticky="we", padx=24, pady=(24, 4))

    subtitle = ttk.Label(
        frame,
        text="Interactive demo of graph-based fraud scoring on transaction data.",
        style="Small.TLabel",
        anchor="w",
        justify="left",
    )
    subtitle.grid(row=1, column=0, sticky="we", padx=24, pady=(0, 16))

    text = (
        "This project showcases how graph algorithms can help analysts "
        "spot suspicious accounts in large transaction networks.\n\n"
        "The app guides you through:\n"
        "- loading a labeled transaction dataset,\n"
        "- configuring Personalized PageRank parameters,\n"
        "- running the analysis, and\n"
        "- exploring the top-ranked suspicious nodes with Precision@K.\n"
    )

    info = ttk.Label(
        frame,
        text=text,
        style="Small.TLabel",
        anchor="nw",
        justify="left",
        wraplength=760,
    )
    info.grid(row=2, column=0, sticky="nwe", padx=24, pady=(0, 8))

    # بخش Credits
    credits_text = (
        "Developed by:\n"
        "  - Ali Shameli\n"
        "  - Shahriar Moghimi\n\n"
        "Course:\n"
        "  - Data Structures (DS) Project, Fall 2025\n\n"
        "Supervisor:\n"
        "   - Dr. Ali Katan Foroush\n"
    )

    credits = ttk.Label(
        frame,
        text=credits_text,
        style="BoldSmall.TLabel",
        anchor="nw",
        justify="left",
        wraplength=760,
    )
    credits.grid(row=3, column=0, sticky="nwe", padx=24, pady=(0, 16))

    # لینک گیت‌هاب
    repo_url = "https://github.com/Ali-Shameli/Personalized-PageRank.git"  # این را عوض کن

    link_btn = ttk.Button(
        frame,
        text="Open project on GitHub",
        style="Secondary.TButton",
        command=lambda: webbrowser.open_new_tab(repo_url),
    )
    link_btn.grid(row=4, column=0, sticky="w", padx=24, pady=(0, 16))

    # نوار دکمه
    button_bar = ttk.Frame(frame)
    button_bar.grid(row=5, column=0, sticky="e", padx=24, pady=24)

    back_btn = ttk.Button(
        button_bar,
        text="Back",
        command=lambda: app.show_page(0),
    )
    back_btn.pack(side="right")
