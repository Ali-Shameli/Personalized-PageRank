from __future__ import annotations

import tkinter as tk
from tkinter import ttk


def build_run_page(frame: ttk.Frame, app) -> None:
    """Page 2: configure and run Personalized PageRank."""
    for c in range(3):
        frame.columnconfigure(c, weight=1)
    for r in range(8):  # افزایش به 8 ردیف
        frame.rowconfigure(r, weight=0)
    frame.rowconfigure(8, weight=1)

    title = ttk.Label(
        frame,
        text="2. Configure and run analysis",
        style="Title.TLabel",
        anchor="w",
    )
    title.grid(row=0, column=0, columnspan=3, sticky="we", padx=24, pady=(24, 8))

    if app.state.data_source == "manual":
        data_info = "manual"
    else:
        data_info = app.state.data_path or "No dataset selected"
    data_label = ttk.Label(
        frame,
        text=f"Selected dataset: {data_info}",
        style="Small.TLabel",
        anchor="w",
        justify="left",
    )
    data_label.grid(row=1, column=0, columnspan=3, sticky="we", padx=24, pady=(0, 12))

    # ---- نوع گراف ----
    graph_type_frame = ttk.LabelFrame(frame, text="Graph type")
    graph_type_frame.grid(row=2, column=0, columnspan=3, sticky="we", padx=24, pady=(0, 12))
    
    graph_type_var = tk.StringVar(value="unweighted")
    
    unweighted_rb = ttk.Radiobutton(
        graph_type_frame,
        text="Unweighted graph",
        variable=graph_type_var,
        value="unweighted"
    )
    unweighted_rb.pack(side="left", padx=12, pady=8)
    
    weighted_rb = ttk.Radiobutton(
        graph_type_frame,
        text="Weighted graph",
        variable=graph_type_var,
        value="weighted"
    )
    weighted_rb.pack(side="left", padx=12, pady=8)
    
    note_label = ttk.Label(
        graph_type_frame,
        text="(Edge weights will be used for transition probabilities)",
        style="Small.TLabel"
    )
    note_label.pack(side="left", padx=8, pady=8)

    # ---- الگوریتم ----
    algorithm_frame = ttk.LabelFrame(frame, text="Algorithm")
    algorithm_frame.grid(row=3, column=0, columnspan=3, sticky="we", padx=24, pady=(0, 12))
    
    algorithm_var = tk.StringVar(value="power")
    
    power_rb = ttk.Radiobutton(
        algorithm_frame,
        text="Power iteration (accurate)",
        variable=algorithm_var,
        value="power"
    )
    power_rb.pack(side="left", padx=12, pady=8)
    
    monte_rb = ttk.Radiobutton(
        algorithm_frame,
        text="Monte Carlo (fast approximate)",
        variable=algorithm_var,
        value="monte_carlo"
    )
    monte_rb.pack(side="left", padx=12, pady=8)

    # ---- کانتینر دینامیک برای پارامترها ----
    params_container = ttk.Frame(frame)
    params_container.grid(row=4, column=0, columnspan=3, sticky="we", padx=24, pady=(0, 12))

    # زیرفریم برای پارامترهای Power iteration
    power_params_frame = ttk.LabelFrame(params_container, text="Parameters for Power iteration")
    for c in range(4):
        power_params_frame.columnconfigure(c, weight=1)

    # زیرفریم برای پارامترهای Monte Carlo
    monte_params_frame = ttk.LabelFrame(params_container, text="Parameters for Monte Carlo")
    for c in range(4):
        monte_params_frame.columnconfigure(c, weight=1)

    # ---- متغیرهای پارامترها ----
    alpha_var = tk.DoubleVar(value=0.85)
    max_iter_var = tk.IntVar(value=100)
    tol_var = tk.DoubleVar(value=1e-6)
    num_walks_var = tk.IntVar(value=1000)
    walk_length_var = tk.IntVar(value=50)

    def setup_power_params():
        """ایجاد ویجت‌های پارامترهای Power iteration"""
        # پاک کردن قبلی (اگر وجود داشت)
        for widget in power_params_frame.winfo_children():
            widget.destroy()
        
        ttk.Label(power_params_frame, text="Damping factor (alpha):").grid(
            row=0, column=0, sticky="w", padx=12, pady=(8,4))
        ttk.Entry(power_params_frame, textvariable=alpha_var).grid(
            row=0, column=1, sticky="we", padx=(0,12), pady=(8,4))
        
        ttk.Label(power_params_frame, text="Max iterations:").grid(
            row=1, column=0, sticky="w", padx=12, pady=4)
        ttk.Entry(power_params_frame, textvariable=max_iter_var).grid(
            row=1, column=1, sticky="we", padx=(0,12), pady=4)
        
        ttk.Label(power_params_frame, text="Tolerance (L1):").grid(
            row=2, column=0, sticky="w", padx=12, pady=(4,8))
        ttk.Entry(power_params_frame, textvariable=tol_var).grid(
            row=2, column=1, sticky="we", padx=(0,12), pady=(4,8))

    def setup_monte_params():
        """ایجاد ویجت‌های پارامترهای Monte Carlo"""
        # پاک کردن قبلی (اگر وجود داشت)
        for widget in monte_params_frame.winfo_children():
            widget.destroy()
        
        ttk.Label(monte_params_frame, text="Damping factor (alpha):").grid(
            row=0, column=0, sticky="w", padx=12, pady=(8,4))
        ttk.Entry(monte_params_frame, textvariable=alpha_var).grid(
            row=0, column=1, sticky="we", padx=(0,12), pady=(8,4))
        
        ttk.Label(monte_params_frame, text="Number of random walks:").grid(
            row=1, column=0, sticky="w", padx=12, pady=4)
        ttk.Entry(monte_params_frame, textvariable=num_walks_var).grid(
            row=1, column=1, sticky="we", padx=(0,12), pady=4)
        
        ttk.Label(monte_params_frame, text="Max walk length:").grid(
            row=2, column=0, sticky="w", padx=12, pady=(4,8))
        ttk.Entry(monte_params_frame, textvariable=walk_length_var).grid(
            row=2, column=1, sticky="we", padx=(0,12), pady=(4,8))

    def show_power_params():
        """نمایش پارامترهای Power iteration"""
        monte_params_frame.pack_forget()
        power_params_frame.pack(fill="x", expand=True)
        setup_power_params()

    def show_monte_params():
        """نمایش پارامترهای Monte Carlo"""
        power_params_frame.pack_forget()
        monte_params_frame.pack(fill="x", expand=True)
        setup_monte_params()

    # ---- تنظیم اولیه ----
    setup_power_params()
    setup_monte_params()
    show_power_params()  # نمایش پیش‌فرض

    # ---- اتصال رویداد تغییر الگوریتم ----
    algorithm_var.trace_add("write", lambda *args: on_algorithm_change())

    def on_algorithm_change():
        """هنگام تغییر الگوریتم"""
        if algorithm_var.get() == "power":
            show_power_params()
        else:
            show_monte_params()

    # ---- ناحیه وضعیت / لاگ ----
    status_label = ttk.Label(
        frame,
        text="Press Run to start the analysis.",
        style="Small.TLabel",
        anchor="w",
        justify="left",
    )
    status_label.grid(row=5, column=0, columnspan=3, sticky="we", padx=24, pady=(8, 0))

    # ---- تابع اجرا ----
    def on_run() -> None:
        if not app.state.data_path and app.state.data_source !="manual":
            status_label.configure(text="No dataset selected on previous step.")
            return

        try:
            algorithm = algorithm_var.get()
            weighted = (graph_type_var.get() == "weighted")
            
            if algorithm == "power":
                params = {
                    "alpha": float(alpha_var.get()),
                    "max_iter": int(max_iter_var.get()),
                    "tol": float(tol_var.get()),
                    "weighted": weighted,
                    "algorithm": "power"
                }
            else:  # monte_carlo
                params = {
                    "alpha": float(alpha_var.get()),
                    "num_walks": int(num_walks_var.get()),
                    "max_steps": int(walk_length_var.get()),
                    "weighted": weighted,
                    "algorithm": "monte_carlo"
                }
        except ValueError:
            status_label.configure(text="Invalid parameter values.")
            return

        status_label.configure(text="Running Personalized PageRank…")

        try:
            app.run_ppr(**params)
            status_label.configure(text="Analysis finished. Showing results…")
            app.show_page(3)
        except Exception as e:
            status_label.configure(text=f"Error during analysis: {e}")

    # ---- دکمه‌های پایین ----
    button_bar = ttk.Frame(frame)
    button_bar.grid(row=7, column=0, columnspan=3, sticky="e", padx=24, pady=24)

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
