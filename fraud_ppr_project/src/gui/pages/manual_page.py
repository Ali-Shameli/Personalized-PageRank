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