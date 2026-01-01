# gui/theme.py
from __future__ import annotations

import tkinter as tk
from tkinter import ttk


def apply_dark_theme(root: tk.Tk) -> ttk.Style:
    """Configure a simple dark theme and return the style object."""
    style = ttk.Style(root)

    # Base colors (می‌توانیم بعداً فاین‌تیون کنیم)
    bg = "#262626"
    frame_bg = "#303030"
    fg = "#f5f5f5"
    accent = "#3a8cff"
    muted = "#aaaaaa"
    danger = "#ff5555"

    # Set base theme
    style.theme_use("clam")

    # General
    root.configure(bg=bg)
    style.configure(".", background=bg, foreground=fg)

    # Frames
    style.configure("TFrame", background=frame_bg)
    style.configure("Card.TFrame", background=frame_bg, relief="flat")

    # Labels
    style.configure("TLabel", background=frame_bg, foreground=fg)
    style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"), foreground=fg)
    style.configure("Small.TLabel", font=("Segoe UI", 10), foreground=muted)

    # Buttons
    style.configure(
        "TButton",
        padding=(10, 6),
        background="#3b3b3b",
        foreground=fg,
        borderwidth=0,
        focusthickness=0,
    )
    style.map(
        "TButton",
        background=[("active", "#505050"), ("pressed", "#404040")],
    )

    style.configure(
        "Nav.TButton",
        padding=(14, 8),
        background=accent,
        foreground="#ffffff",
    )
    style.map(
        "Nav.TButton",
        background=[("active", "#4b9aff"), ("pressed", "#3375cc")],
    )

    # Danger button (اگه جایی لازم شد)
    style.configure(
        "Danger.TButton",
        padding=(10, 6),
        background=danger,
        foreground="#ffffff",
    )
    style.map(
        "Danger.TButton",
        background=[("active", "#ff7777"), ("pressed", "#cc4444")],
    )

    # Entries
    style.configure(
        "TEntry",
        fieldbackground="#1e1e1e",
        foreground=fg,
        insertcolor=fg,
        borderwidth=0,
    )

    # Treeview (برای جدول نتایج)
    style.configure(
        "Treeview",
        background=frame_bg,
        foreground=fg,
        fieldbackground=frame_bg,
        bordercolor=bg,
        borderwidth=0,
    )
    style.map(
        "Treeview",
        background=[("selected", "#505050")],
        foreground=[("selected", "#ffffff")],
    )
    style.configure(
        "Treeview.Heading",
        background=bg,
        foreground=fg,
    )

    return style

