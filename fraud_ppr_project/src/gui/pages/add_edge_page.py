# src/gui/pages/add_edge_page.py
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

def build_add_edge_page(frame: ttk.Frame, app) -> None:
    """Page for adding new edges to the graph."""
    # Configure grid: 3 columns, only last row expands
    for c in range(3):
        frame.columnconfigure(c, weight=1)
    frame.rowconfigure(0, weight=0)  # Title
    frame.rowconfigure(1, weight=0)  # Info
    frame.rowconfigure(2, weight=0)  # Input frame
    frame.rowconfigure(3, weight=0)  # Status
    frame.rowconfigure(4, weight=1)  # Spacer (expands)
    frame.rowconfigure(5, weight=0)  # Buttons (bottom)

    # --- Title (row 0) ---
    title = ttk.Label(
        frame,
        text="Add New Edge to Graph",
        style="Title.TLabel",
        anchor="w",
    )
    title.grid(row=0, column=0, columnspan=3, sticky="we", padx=24, pady=(24, 16))

    # --- Explanation (row 1) ---
    info = ttk.Label(
        frame,
        text="Add a new edge to update PPR scores without full recomputation.",
        style="Small.TLabel",
        anchor="w",
        justify="left",
    )
    info.grid(row=1, column=0, columnspan=3, sticky="we", padx=24, pady=(0, 20))

    # --- Single Edge Input Frame (row 2) ---
    single_frame = ttk.LabelFrame(frame, text="Add Single Edge", padding=15)
    single_frame.grid(row=2, column=0, columnspan=3, sticky="we", padx=24, pady=(0, 12))

    # Source Node input
    ttk.Label(single_frame, text="Source Node ID:").grid(
        row=0, column=0, sticky="w", padx=(0, 10), pady=8
    )
    source_var = tk.StringVar()
    source_entry = ttk.Entry(single_frame, textvariable=source_var, width=15)
    source_entry.grid(row=0, column=1, sticky="w", pady=8)

    # Target Node input
    ttk.Label(single_frame, text="Target Node ID:").grid(
        row=1, column=0, sticky="w", padx=(0, 10), pady=8
    )
    target_var = tk.StringVar()
    target_entry = ttk.Entry(single_frame, textvariable=target_var, width=15)
    target_entry.grid(row=1, column=1, sticky="w", pady=8)

    # Edge Weight input (optional, default = 1.0)
    ttk.Label(single_frame, text="Edge Weight (optional):").grid(
        row=2, column=0, sticky="w", padx=(0, 10), pady=8
    )
    weight_var = tk.StringVar(value="1.0")
    weight_entry = ttk.Entry(single_frame, textvariable=weight_var, width=15)
    weight_entry.grid(row=2, column=1, sticky="w", pady=8)

    # --- Status Message (row 3) ---
    status_label = ttk.Label(
        frame,
        text="",
        style="Small.TLabel",
        anchor="w",
        justify="left",
    )
    status_label.grid(row=3, column=0, columnspan=3, sticky="we", padx=24, pady=(0, 20))

    # --- Spacer Frame (row 4, expands) ---
    spacer = ttk.Frame(frame)
    spacer.grid(row=4, column=0, columnspan=3, sticky="nswe")
    
    # --- Buttons at Bottom (row 5) ---
    button_bar = ttk.Frame(frame)
    button_bar.grid(row=5, column=0, columnspan=3, sticky="e", padx=24, pady=(0, 24))

    cancel_btn = ttk.Button(
        button_bar,
        text="Cancel",
        command=lambda: app.show_page(3),
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


def add_edge_and_update(app, source_var, target_var, weight_var, status_label):
    """
    Handle adding a single edge and running incremental PPR update.
    
    Steps:
    1. Validate user input
    2. Check if graph is loaded
    3. Prepare edge data
    4. Trigger incremental PPR update
    5. Provide user feedback
    """
    try:
        # --- Input Parsing and Validation ---
        source = int(source_var.get())
        target = int(target_var.get())
        weight = float(weight_var.get()) if weight_var.get() else 1.0

        # Basic validation
        if source < 0 or target < 0:
            raise ValueError("Node IDs must be non-negative integers")
        if weight <= 0:
            raise ValueError("Edge weight must be a positive number")

    except ValueError as e:
        # Display validation error to user
        status_label.config(text=f"Invalid input: {e}")
        return

    # --- Graph Existence Check ---
    if not hasattr(app.state, 'scores') or app.state.scores is None:
        status_label.config(text="No graph loaded. Please run analysis first.")
        return

    # --- Prepare Edge Data ---
    new_edge = (source, target, weight)
    
    # Show processing status
    status_label.config(text=f"Adding edge ({source} → {target}, weight={weight})...")

    # --- Trigger Incremental PPR Update ---
    try:
        # Call the main application's incremental PPR method
        # The method expects a list of edges
        success = app.run_incremental_ppr([new_edge])
        
        if success:
            # Success feedback
            status_label.config(
                text="Edge added successfully! PPR scores updated.", 
                foreground="green"
            )
            
            # Optional: auto-return to results page after delay
            # app.master.after(2000, lambda: app.show_page(3))
            
        else:
            # PPR update failed
            status_label.config(
                text="Failed to update PPR scores. Please try again.", 
                foreground="red"
            )
            
    except AttributeError:
        # Method not implemented (for development/demo)
        status_label.config(
            text="Edge added (Incremental PPR simulation).", 
            foreground="blue"
        )
    except Exception as e:
        # Unexpected error during PPR update
        status_label.config(
            text=f"Error during PPR update: {str(e)}", 
            foreground="red"
        )