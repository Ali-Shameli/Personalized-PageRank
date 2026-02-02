# src/gui/pages/how_page.py
from __future__ import annotations
import tkinter as tk
from tkinter import ttk

def build_how_page(frame: ttk.Frame, app) -> None:
    """Page explaining how the fraud detection system works."""
    # Grid layout configuration
    frame.columnconfigure(0, weight=1)
    for r in range(6):
        frame.rowconfigure(r, weight=0)
    frame.rowconfigure(2, weight=1)  # Main content expands

    # --- Title Section ---
    title = ttk.Label(
        frame,
        text="How It Works",
        style="Title.TLabel",
        anchor="w",
    )
    title.grid(row=0, column=0, sticky="we", padx=24, pady=(24, 8))

    subtitle = ttk.Label(
        frame,
        text="Fraud detection using Personalized PageRank in 4 steps",
        style="Small.TLabel",
        anchor="w",
        justify="left",
    )
    subtitle.grid(row=1, column=0, sticky="we", padx=24, pady=(0, 20))

    # --- Core Concepts Container ---
    concepts_container = ttk.Frame(frame)
    concepts_container.grid(row=2, column=0, sticky="nsew", padx=24, pady=(0, 16))
    concepts_container.columnconfigure(0, weight=1)

    # --- Algorithm Selection Tabs ---
    notebook = ttk.Notebook(concepts_container)
    notebook.grid(row=0, column=0, sticky="nsew", pady=(0, 16))

    # Power Iteration Tab
    power_tab = ttk.Frame(notebook)
    notebook.add(power_tab, text="Power Iteration (Accurate)")
    
    power_text = ttk.Label(
        power_tab,
        text=(
            "• Exact solution using matrix operations\n"
            "• Guaranteed convergence\n"
            "• Best for medium-sized graphs\n"
            "• Supports incremental updates\n"
            "• Complexity: O(k × E) where k ≈ 50-100 iterations"
        ),
        style="Small.TLabel",
        anchor="w",
        justify="left",
    )
    power_text.pack(fill="both", expand=True, padx=12, pady=12)

    # Monte Carlo Tab
    monte_tab = ttk.Frame(notebook)
    notebook.add(monte_tab, text="Monte Carlo (Fast Approximate)")
    
    monte_text = ttk.Label(
        monte_tab,
        text=(
            "• Statistical approximation using random walks\n"
            "• Faster for very large graphs\n"
            "• Independent of graph size\n"
            "• Easy to parallelize\n"
            "• Approximate results with sampling error"
        ),
        style="Small.TLabel",
        anchor="w",
        justify="left",
    )
    monte_text.pack(fill="both", expand=True, padx=12, pady=12)

    # --- Key Concepts Frame ---
    concepts_frame = ttk.LabelFrame(concepts_container, text="Key Concepts", padding=15)
    concepts_frame.grid(row=1, column=0, sticky="we", pady=(0, 16))
    concepts_frame.columnconfigure(0, weight=1)

    # Guilt by Association
    gba_text = ttk.Label(
        concepts_frame,
        text=(
            "🔍 Guilt by Association\n"
            "   Fraudsters tend to cluster together. If someone frequently\n"
            "   interacts with known fraudsters, they're likely high-risk too."
        ),
        style="Small.TLabel",
        anchor="w",
        justify="left",
    )
    gba_text.grid(row=0, column=0, sticky="w", padx=8, pady=8)

    # Personalized PageRank
    ppr_text = ttk.Label(
        concepts_frame,
        text=(
            "📊 Personalized PageRank\n"
            "   Spreads 'suspicion score' from known fraud seeds through\n"
            "   the network, measuring proximity to bad actors."
        ),
        style="Small.TLabel",
        anchor="w",
        justify="left",
    )
    ppr_text.grid(row=1, column=0, sticky="w", padx=8, pady=8)

    # Precision@K
    pk_text = ttk.Label(
        concepts_frame,
        text=(
            "🎯 Precision@K Evaluation\n"
            "   Measures how many of the top-K flagged nodes are\n"
            "   actually fraudulent. Higher = better detection."
        ),
        style="Small.TLabel",
        anchor="w",
        justify="left",
    )
    pk_text.grid(row=2, column=0, sticky="w", padx=8, pady=8)

    # --- Pipeline Steps ---
    pipeline = ttk.LabelFrame(frame, text="4-Step Analysis Pipeline", padding=15)
    pipeline.grid(row=3, column=0, sticky="nwe", padx=24, pady=(0, 16))
    pipeline.columnconfigure(0, weight=1)

    steps = [
        ("1️⃣", "Build Graph", "Convert transaction data into a network graph"),
        ("2️⃣", "Mark Seeds", "Identify known fraudsters as starting points"),
        ("3️⃣", "Run PPR", "Compute suspicion scores for all nodes"),
        ("4️⃣", "Evaluate", "Rank nodes and calculate Precision@K")
    ]

    for i, (icon, title_text, desc) in enumerate(steps):
        step_frame = ttk.Frame(pipeline)
        step_frame.grid(row=i, column=0, sticky="we", pady=4)
        
        icon_label = ttk.Label(step_frame, text=icon, font=("Arial", 14))
        icon_label.pack(side="left", padx=(0, 10))
        
        title_label = ttk.Label(step_frame, text=title_text, style="Small.TLabel", font=("Arial", 10, "bold"))
        title_label.pack(side="left", padx=(0, 10))
        
        desc_label = ttk.Label(step_frame, text=desc, style="Small.TLabel")
        desc_label.pack(side="left")

    # --- Bottom Button Bar ---
    button_bar = ttk.Frame(frame)
    button_bar.grid(row=4, column=0, sticky="e", padx=24, pady=(0, 24))

    back_btn = ttk.Button(
        button_bar,
        text="Back to Home",
        command=lambda: app.show_page(0),
    )
    back_btn.pack(side="right")