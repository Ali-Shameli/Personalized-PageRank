# src/gui/pages/results_page.py
from __future__ import annotations

import csv
import os
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


def build_results_page(frame: ttk.Frame, app) -> None:
    """Page 3: display top-K suspicious nodes, Precision@K, and export functionality."""
    # Grid layout configuration
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=0)  # Title row
    frame.rowconfigure(1, weight=0)  # Control bar
    frame.rowconfigure(2, weight=1)  # Results table (expands)
    frame.rowconfigure(3, weight=0)  # Bottom button bar

    # Page title
    title = ttk.Label(
        frame,
        text="3. Results",
        style="Title.TLabel",
        anchor="w",
    )
    title.grid(row=0, column=0, sticky="we", padx=24, pady=(24, 8))

    # --- K Control and Info Section ---
    control_bar = ttk.Frame(frame)
    control_bar.grid(row=1, column=0, sticky="we", padx=24, pady=(0, 8))
    control_bar.columnconfigure(0, weight=0)
    control_bar.columnconfigure(1, weight=0)
    control_bar.columnconfigure(2, weight=1)

    # K value input
    k_label = ttk.Label(control_bar, text="K (top-K & Precision@K):")
    k_label.grid(row=0, column=0, sticky="w", padx=(0, 8))

    k_entry = ttk.Entry(control_bar, width=6)
    k_entry.insert(0, "50")
    k_entry.grid(row=0, column=1, sticky="w")

    # Info text
    info = ttk.Label(
        control_bar,
        text="Top suspicious nodes by PPR score.",
        style="Small.TLabel",
        anchor="w",
        justify="left",
    )
    info.grid(row=1, column=0, columnspan=3, sticky="we", pady=(4, 0))

    # --- Results Table ---
    tree = ttk.Treeview(
        frame,
        columns=("rank", "node", "score", "label"),
        show="headings",
        height=15,
    )
    tree.heading("rank", text="Rank")
    tree.heading("node", text="Node ID")
    tree.heading("score", text="Score")
    tree.heading("label", text="Label")

    tree.column("rank", width=60, anchor="center")
    tree.column("node", width=80, anchor="center")
    tree.column("score", width=120, anchor="center")
    tree.column("label", width=80, anchor="center")

    tree.grid(row=2, column=0, sticky="nsew", padx=24, pady=(0, 8))
    frame.rowconfigure(2, weight=1)

    # Tag configuration for fraud nodes (label=1)
    tree.tag_configure("fraud", background="#4a2b2b")  # Dark red background

    # --- Bottom Button Bar ---
    bottom_bar = ttk.Frame(frame)
    bottom_bar.grid(row=3, column=0, sticky="e", padx=24, pady=(0, 16))

    # Check if results are available
    scores = app.state.scores
    labels = app.state.labels

    if scores is None or labels is None:
        info.configure(text="No results available. Run the analysis first.")

        # Create minimal bottom bar for navigation
        bottom_bar = ttk.Frame(frame)
        bottom_bar.grid(row=3, column=0, sticky="e", padx=24, pady=(0, 16))

        back_btn = ttk.Button(
            bottom_bar,
            text="Back",
            command=lambda: app.show_page(2),  # Back to Run page
        )
        back_btn.pack(side="left", padx=(0, 8))

        export_btn = ttk.Button(bottom_bar, text="Export CSV…", state="disabled")
        export_btn.pack(side="left", padx=(0, 8))

        close_btn = ttk.Button(
            bottom_bar,
            text="Close",
            style="Danger.TButton",
            command=app.destroy,
        )
        close_btn.pack(side="left")

        return

    n = len(scores)

    # Store current table data for export
    current_rows = []  # List of (rank, node, score, label) tuples

    def refresh_for_k() -> None:
        """Refresh table display for the specified K value."""
        nonlocal current_rows

        # Parse K value with validation
        try:
            k_value = int(k_entry.get())
        except ValueError:
            k_value = 50
            k_entry.delete(0, "end")
            k_entry.insert(0, str(k_value))

        if k_value <= 0:
            k_value = 1
            k_entry.delete(0, "end")
            k_entry.insert(0, "1")

        # Clear existing table
        for item in tree.get_children():
            tree.delete(item)
        current_rows = []

        # Sort scores in descending order
        order = np.argsort(scores)[::-1]

        # Effective K: cannot exceed total number of nodes
        k_eff = min(k_value, n)
        top_display = order[:k_eff]

        # Get reverse mapping from internal indices to original node IDs
        rev_map = getattr(app.state, "reverse_map", None)

        # Populate table with top-K results
        for idx, node in enumerate(top_display, start=1):
            score = float(scores[node])
            lab = int(labels.get(int(node), 0))

            # Map internal index to original node ID
            real_node_id = rev_map[int(node)] if rev_map else int(node)

            # Store for export
            row_values = (idx, real_node_id, score, lab)
            current_rows.append(row_values)

            # Apply visual tag for fraud nodes
            tags = ("fraud",) if lab == 1 else ()

            # Insert into table
            tree.insert(
                "",
                "end",
                values=(idx, real_node_id, f"{score:.6f}", lab),
                tags=tags,
            )

        # Calculate Precision@K
        from src.evaluation.metrics import precision_at_k
        prec_k = precision_at_k(scores, labels, k_eff)


        # Update info text with K adjustment note if needed
        if k_value > n:
            note = f" (Note: K={k_value} requested, but only {n} nodes available)"
        else:
            note = ""
        # Update info text
        info.configure(
            text=(
                f"Top suspicious nodes by PPR score (top {len(top_display)} shown).{note}\n\n"
                f"Precision@{k_eff}: {prec_k:.3f}"
            )
        )

    def export_csv() -> None:
        """Export current table data to CSV file."""
        if not current_rows:
            messagebox.showinfo("Export CSV", "No rows to export.")
            return

        default_name = "ppr_topk_results.csv"
        filepath = filedialog.asksaveasfilename(
            title="Export top-K results to CSV",
            defaultextension=".csv",
            initialfile=default_name,
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if not filepath:
            return

        try:
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["rank", "node_id", "score", "label"])
                for rank, node, score, lab in current_rows:
                    writer.writerow([rank, node, f"{score:.6f}", lab])
            messagebox.showinfo(
                "Export CSV",
                f"Exported {len(current_rows)} rows to:\n{os.path.abspath(filepath)}",
            )
        except Exception as e:
            messagebox.showerror("Export CSV", f"Failed to save file:\n{e}")

    # Apply K button
    apply_btn = ttk.Button(
        control_bar,
        text="Apply K",
        style="Nav.TButton",
        command=refresh_for_k,
    )
    apply_btn.grid(row=0, column=2, sticky="e")

    # --- Bottom Action Bar (Back / Actions / Close) ---
    bottom_bar = ttk.Frame(frame)
    bottom_bar.grid(row=3, column=0, sticky="e", padx=24, pady=(0, 16))

    # Back button
    back_btn = ttk.Button(
        bottom_bar,
        text="Back",
        command=lambda: app.show_page(2),  # Back to Run page
    )
    back_btn.pack(side="left", padx=(0, 8))

    # Actions dropdown menu button
    action_btn = ttk.Menubutton(
        bottom_bar,
        text="Actions ▼",
        style="Nav.TButton",
    )
    action_btn.pack(side="left", padx=(0, 8))

    # Actions menu
    action_menu = tk.Menu(action_btn, tearoff=0)
    action_btn["menu"] = action_menu

    # Menu items
    action_menu.add_command(
        label="📊 Visualization",
        command=lambda: app.show_page(6)  # Visualization page
    )

    action_menu.add_command(
        label="💾 Export CSV",
        command=export_csv
    )
    
    # Add Edge option (only for non-Monte Carlo algorithms)
    if app.state.last_algorithm != "monte_carlo":
        action_menu.add_separator()
        action_menu.add_command(
            label="➕ Add New Edge",
            command=lambda: app.show_page(8)  # Add Edge page
        )

    # Close button
    close_btn = ttk.Button(
        bottom_bar,
        text="Close",
        style="Danger.TButton",
        command=app.destroy,  # Exit application
    )
    close_btn.pack(side="left")

    # Initial table population
    refresh_for_k() 