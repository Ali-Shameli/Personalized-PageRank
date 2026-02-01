# src/gui/pages/add_edge_page.py
from __future__ import annotations

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import numpy as np


def build_add_edge_page(frame: ttk.Frame, app) -> None:
    """Page for adding new edges to the graph."""
    for c in range(3):
        frame.columnconfigure(c, weight=1)
    for r in range(7):
        frame.rowconfigure(r, weight=0)
    frame.rowconfigure(7, weight=1)

    # Title
    title = ttk.Label(
        frame,
        text="Add New Edge to Graph",
        style="Title.TLabel",
        anchor="w",
    )
    title.grid(row=0, column=0, columnspan=3, sticky="we", padx=24, pady=(24, 16))

    # Explanation
    info = ttk.Label(
        frame,
        text="Add a new edge to update PPR scores without full recomputation.",
        style="Small.TLabel",
        anchor="w",
        justify="left",
    )
    info.grid(row=1, column=0, columnspan=3, sticky="we", padx=24, pady=(0, 20))

    # --- Single Edge Frame ---
    single_frame = ttk.LabelFrame(frame, text="Add Single Edge", padding=15)
    single_frame.grid(row=2, column=0, columnspan=3, sticky="we", padx=24, pady=(0, 12))

    # Source Node
    ttk.Label(single_frame, text="Source Node ID:").grid(
        row=0, column=0, sticky="w", padx=(0, 10), pady=8
    )
    source_var = tk.StringVar()
    source_entry = ttk.Entry(single_frame, textvariable=source_var, width=15)
    source_entry.grid(row=0, column=1, sticky="w", pady=8)

    # Target Node
    ttk.Label(single_frame, text="Target Node ID:").grid(
        row=1, column=0, sticky="w", padx=(0, 10), pady=8
    )
    target_var = tk.StringVar()
    target_entry = ttk.Entry(single_frame, textvariable=target_var, width=15)
    target_entry.grid(row=1, column=1, sticky="w", pady=8)

    # Weight
    ttk.Label(single_frame, text="Edge Weight (optional):").grid(
        row=2, column=0, sticky="w", padx=(0, 10), pady=8
    )
    weight_var = tk.StringVar(value="1.0")
    weight_entry = ttk.Entry(single_frame, textvariable=weight_var, width=15)
    weight_entry.grid(row=2, column=1, sticky="w", pady=8)

    # --- Multiple Edges Frame ---
    multi_frame = ttk.LabelFrame(frame, text="Add Multiple Edges from CSV", padding=15)
    multi_frame.grid(row=3, column=0, columnspan=3, sticky="we", padx=24, pady=(12, 20))

    csv_info = ttk.Label(
        multi_frame,
        text="CSV format: source,target,weight (weight optional)",
        style="Small.TLabel",
    )
    csv_info.pack(anchor="w", pady=(0, 10))

    csv_btn = ttk.Button(
        multi_frame,
        text="Browse CSV File...",
        command=lambda: browse_csv(app, csv_status),
    )
    csv_btn.pack(side="left", padx=(0, 10))

    csv_status = ttk.Label(multi_frame, text="No file selected")
    csv_status.pack(side="left")

    # Status message
    status_label = ttk.Label(
        frame,
        text="",
        style="Small.TLabel",
        anchor="w",
        justify="left",
    )
    status_label.grid(row=4, column=0, columnspan=3, sticky="we", padx=24, pady=(0, 20))

    # --- Buttons ---
    button_bar = ttk.Frame(frame)
    button_bar.grid(row=5, column=0, columnspan=3, sticky="e", padx=24, pady=(0, 24))

    cancel_btn = ttk.Button(
        button_bar,
        text="Cancel",
        command=lambda: app.show_page(3),  # Back to Results
    )
    cancel_btn.pack(side="left", padx=(0, 8))

    add_btn = ttk.Button(
        button_bar,
        text="Add Edge & Update Scores",
        style="Nav.TButton",
        command=lambda: add_edge_and_update(
            app, source_var, target_var, weight_var, status_label
        ),
    )
    add_btn.pack(side="left")


def browse_csv(app, status_label):
    """Open file dialog for CSV selection."""
    filepath = filedialog.askopenfilename(
        title="Select CSV file with edges",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    
    if filepath:
        status_label.config(text=f"Selected: {filepath.split('/')[-1]}")
        # Store filepath in app state or process immediately
        app.state.edge_csv_path = filepath
    else:
        status_label.config(text="No file selected")


def add_edge_and_update(app, source_var, target_var, weight_var, status_label):
    """Handle adding edge and running incremental PPR."""
    try:
        # Get values
        source = int(source_var.get())
        target = int(target_var.get())
        weight = float(weight_var.get()) if weight_var.get() else 1.0
        
        # Validate
        if source < 0 or target < 0:
            raise ValueError("Node IDs must be non-negative")
        if weight <= 0:
            raise ValueError("Weight must be positive")
            
    except ValueError as e:
        status_label.config(text=f"Invalid input: {e}")
        return
    
    # Check if graph exists
    if not hasattr(app.state, 'scores') or app.state.scores is None:
        status_label.config(text="No graph loaded. Run analysis first.")
        return
    
    # Store edge for processing
    new_edge = (source, target, weight)
    
    # Show status
    status_label.config(text=f"Adding edge ({source} → {target}, weight={weight})...")
    
    # TODO: Call incremental PPR here
    # app.run_incremental_ppr(new_edge)
        # ... (کد قبلی)
    
    # Call incremental PPR via App method
    app.run_incremental_ppr([new_edge])  # لیست شامل یک تاپل

    # Show success (messagebox is already shown in app.run_incremental_ppr usually,
    # or show it here if you prefer)
    status_label.config(text="Graph updated successfully!")
    
    # Return to results automatically after a delay?
    # frame.after(1000, lambda: app.show_page(3))

    # For now, just show message
    status_label.config(text="Edge added successfully. (Incremental PPR not implemented yet)")
    
    # After processing, go back to results
    # app.show_page(3)


# Register this page in app.py
# در app.py در تابع _create_page اضافه کن:
# elif index == 8:
#     build_add_edge_page(frame, app=self)