# src/gui/pages/run_page.py
from __future__ import annotations

import tkinter as tk
from tkinter import ttk


def build_run_page(frame: ttk.Frame, app) -> None:
    """Page 2: configure and run Personalized PageRank."""
    for c in range(3):
        frame.columnconfigure(c, weight=1)
    for r in range(6):
        frame.rowconfigure(r, weight=0)
    frame.rowconfigure(6, weight=1)

    title = ttk.Label(
        frame,
        text="2. Configure and run analysis",
        style="Title.TLabel",
        anchor="w",
    )
    title.grid(row=0, column=0, columnspan=3, sticky="we", padx=24, pady=(24, 8))

    data_info = app.state.data_path or "No dataset selected"
    data_label = ttk.Label(
        frame,
        text=f"Selected dataset: {data_info}",
        style="Small.TLabel",
        anchor="w",
        justify="left",
    )
    data_label.grid(row=1, column=0, columnspan=3, sticky="we", padx=24, pady=(0, 16))

    # ---- پارامترها ----
    params_frame = ttk.LabelFrame(frame, text="Personalized PageRank parameters")
    params_frame.grid(row=2, column=0, columnspan=3, sticky="we", padx=24, pady=(0, 12))
    for c in range(4):
        params_frame.columnconfigure(c, weight=1)

    alpha_var = tk.DoubleVar(value=0.85)
    maxiter_var = tk.IntVar(value=100)
    tol_var = tk.DoubleVar(value=1e-6)

    alpha_label = ttk.Label(params_frame, text="Damping factor (alpha):")
    alpha_label.grid(row=0, column=0, sticky="w", padx=12, pady=(8, 4))
    alpha_entry = ttk.Entry(params_frame, textvariable=alpha_var)
    alpha_entry.grid(row=0, column=1, sticky="we", padx=(0, 12), pady=(8, 4))

    maxiter_label = ttk.Label(params_frame, text="Max iterations:")
    maxiter_label.grid(row=1, column=0, sticky="w", padx=12, pady=4)
    maxiter_entry = ttk.Entry(params_frame, textvariable=maxiter_var)
    maxiter_entry.grid(row=1, column=1, sticky="we", padx=(0, 12), pady=4)

    tol_label = ttk.Label(params_frame, text="Tolerance (L1):")
    tol_label.grid(row=2, column=0, sticky="w", padx=12, pady=(4, 8))
    tol_entry = ttk.Entry(params_frame, textvariable=tol_var)
    tol_entry.grid(row=2, column=1, sticky="we", padx=(0, 12), pady=(4, 8))

    # ---- ناحیه وضعیت / لاگ ----
    status_label = ttk.Label(
        frame,
        text="Press Run to start the analysis.",
        style="Small.TLabel",
        anchor="w",
        justify="left",
    )
    status_label.grid(row=3, column=0, columnspan=3, sticky="we", padx=24, pady=(8, 0))


    def on_run() -> None:
        if not app.state.data_path:
            status_label.configure(text="No dataset selected on previous step.")
            return

        try:
            alpha = float(alpha_var.get())
            max_iter = int(maxiter_var.get())
            tol = float(tol_var.get())
        except ValueError:
            status_label.configure(text="Invalid parameter values.")
            return

        status_label.configure(text="Running Personalized PageRank…")

        try:
            app.run_ppr(alpha=alpha, max_iter=max_iter, tol=tol)
            status_label.configure(text="Analysis finished. Showing results…")
            app.show_page(3)
        except Exception as e:
            # traceback.print_exc()
            status_label.configure(text=f"Error during analysis: {e}")

    # ---- دکمه‌های پایین ----
    button_bar = ttk.Frame(frame)
    button_bar.grid(row=5, column=0, columnspan=3, sticky="e", padx=24, pady=24)

    back_btn = ttk.Button(
        button_bar,
        text="Back",
        command=lambda: app.show_page(1),
    )
    back_btn.pack(side="left", padx=(0, 8))

    run_btn = ttk.Button(
        button_bar,
        text="Run analysis",
        style="Nav.TButton",
        command=on_run,
    )
    run_btn.pack(side="left")
