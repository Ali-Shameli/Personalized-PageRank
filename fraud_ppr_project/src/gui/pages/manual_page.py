from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np



def build_manual_page(frame: ttk.Frame, app) -> None:
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(2, weight=1)

    title = ttk.Label(frame, text="Manual Graph Entry", style="Title.TLabel")
    title.grid(row=0, column=0, sticky="w", padx=24, pady=(24, 8))

    desc = ttk.Label(
        frame,
        text="Enter edges (Src, Dst, Weight) and Fraud Seeds manually.",
        style="Small.TLabel"
    )
    desc.grid(row=1, column=0, sticky="w", padx=24, pady=(0, 16))

    input_frame = ttk.LabelFrame(frame, text="Edges List (Format: NodeA, NodeB, Weight)")
    input_frame.grid(row=2, column=0, sticky="nsew", padx=24, pady=(0, 12))
    input_frame.columnconfigure(0, weight=1)
    input_frame.rowconfigure(0, weight=1)

    text_area = tk.Text(input_frame, height=10, width=50, bg="#1e1e1e", fg="#f5f5f5", insertbackground="white")
    text_area.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
    text_area.insert("1.0", "1, 2, 5.0\n2, 3, 10.5\n3, 1, 2.0\n4, 2, 100.0")

    seed_frame = ttk.LabelFrame(frame, text="Fraud Seeds (Node IDs, separated by comma)")
    seed_frame.grid(row=3, column=0, sticky="we", padx=24, pady=(0, 12))

    seeds_entry = ttk.Entry(seed_frame)
    seeds_entry.grid(row=0, column=0, sticky="we", padx=12, pady=12)
    seeds_entry.insert(0, "4")