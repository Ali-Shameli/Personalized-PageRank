from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox

from src.data.parsers import parse_manual_data


def build_manual_page(frame: ttk.Frame, app) -> None:

    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(2, weight=1)  # The text area (row 2) will expand

    title = ttk.Label(frame, text="Manual Graph Entry", style="Title.TLabel")
    title.grid(row=0, column=0, sticky="w", padx=24, pady=(24, 8))

    desc = ttk.Label(
        frame,
        text="Define your graph structure below.\nFormat: SourceID, DestinationID, Amount (Weight)",
        style="Small.TLabel"
    )
    desc.grid(row=1, column=0, sticky="w", padx=24, pady=(0, 16))

    input_frame = ttk.LabelFrame(frame, text="Edges List")
    input_frame.grid(row=2, column=0, sticky="nsew", padx=24, pady=(0, 12))

    input_frame.columnconfigure(0, weight=1)
    input_frame.rowconfigure(0, weight=1)

    text_area = tk.Text(
        input_frame,
        height=10,
        width=50,
        bg="#2b2b2b",
        fg="#f0f0f0",
        insertbackground="white",  # Cursor color
        font=("Consolas", 10)
    )
    text_area.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)

    scrollbar = ttk.Scrollbar(input_frame, orient="vertical", command=text_area.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    text_area.configure(yscrollcommand=scrollbar.set)

    example_text = "1, 2, 50.0\n2, 3, 10.5\n3, 1, 2.0\n4, 2, 100.0\n5, 5, 10.0"
    text_area.insert("1.0", example_text)