from __future__ import annotations

import os
import tkinter as tk
from tkinter import ttk, filedialog


def build_load_page(frame: ttk.Frame, app) -> None:
    """Page 1: choose sample data or browse custom CSV."""
    for c in range(3):
        frame.columnconfigure(c, weight=1)
    for r in range(6):
        frame.rowconfigure(r, weight=0)
    frame.rowconfigure(6, weight=1)

    # ---- عنوان ----
    title = ttk.Label(
        frame,
        text="1. Load transactions data",
        style="Title.TLabel",
        anchor="w",
    )
    title.grid(row=0, column=0, columnspan=3, sticky="we", padx=24, pady=(24, 8))

    desc_text = (
        "Choose one of the sample datasets provided with the project, "
        "or load your own CSV file."
    )
    desc = ttk.Label(
        frame,
        text=desc_text,
        style="Small.TLabel",
        justify="left",
        anchor="w",
    )
    desc.grid(row=1, column=0, columnspan=3, sticky="we", padx=24, pady=(0, 16))

    # ---- نمونه‌داده‌ها ----
    sample_frame = ttk.LabelFrame(frame, text="Use sample data")
    sample_frame.grid(row=2, column=0, columnspan=3, sticky="we", padx=24, pady=(0, 12))
    for c in range(3):
        sample_frame.columnconfigure(c, weight=1)

    sample_var = tk.StringVar(value="")

    # مسیرها را متناسب با پروژه‌ات تنظیم کن
    samples = {
        "Small synthetic (test_small.csv)": os.path.join("data", "test_small.csv"),
        "Labeled Bitcoin (transactions_bitcoin_labeled.csv)": os.path.join(
            "data", "transactions_bitcoin_labeled.csv"
        ),
    }

    row = 0
    for label, path in samples.items():
        rb = ttk.Radiobutton(
            sample_frame,
            text=label,
            value=path,
            variable=sample_var,
        )
        rb.grid(row=row, column=0, columnspan=3, sticky="w", padx=12, pady=4)
        row += 1

    # ---- فایل دلخواه ----
    custom_frame = ttk.LabelFrame(frame, text="Or load from CSV file")
    custom_frame.grid(row=3, column=0, columnspan=3, sticky="we", padx=24, pady=(0, 12))
    for c in range(3):
        custom_frame.columnconfigure(c, weight=1)

    path_var = tk.StringVar(value="")

    entry = ttk.Entry(custom_frame, textvariable=path_var)
    entry.grid(row=0, column=0, columnspan=2, sticky="we", padx=(12, 8), pady=(8, 8))

    def browse_file() -> None:
        filepath = filedialog.askopenfilename(
            title="Select transactions CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if filepath:
            path_var.set(filepath)
            sample_var.set("")  # اگر کاربر فایل خودش را انتخاب کرد، sample خنثی شود

    browse_btn = ttk.Button(custom_frame, text="Browse…", command=browse_file)
    browse_btn.grid(row=0, column=2, sticky="we", padx=(0, 12), pady=(8, 8))

    # ---- دکمه‌های پایین ----
    button_bar = ttk.Frame(frame)
    button_bar.grid(row=5, column=0, columnspan=3, sticky="e", padx=24, pady=24)

    def on_next() -> None:
        # اولویت: sample اگر انتخاب شده، بعد custom
        chosen_path = sample_var.get().strip()
        source = None

        if chosen_path:
            source = "sample"
        else:
            custom_path = path_var.get().strip()
            if custom_path:
                chosen_path = custom_path
                source = "custom"

        if not chosen_path:
            # فعلاً فقط یک پیام ساده (بعداً می‌توانی messagebox استفاده کنی)
            print("No data selected")
            return

        # print("DEBUG chosen_path:", chosen_path, "source:", source)

        app.state.data_path = chosen_path
        app.state.data_source = source

        # reset old analysis results
        app.state.scores = None
        app.state.labels = None
        app.state.precision_at_50 = None

        app.show_page(2)

        app.state.precision_at_50 = None

    back_btn = ttk.Button(
        button_bar,
        text="Back",
        command=lambda: app.show_page(0),
    )
    back_btn.pack(side="left", padx=(0, 8))

    next_btn = ttk.Button(
        button_bar,
        text="Next",
        style="Nav.TButton",
        command=on_next,
    )
    next_btn.pack(side="left")
