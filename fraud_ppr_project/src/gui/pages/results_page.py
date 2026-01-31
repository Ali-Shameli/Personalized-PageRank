# src/gui/pages/results_page.py
from __future__ import annotations

import csv
import os
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


def build_results_page(frame: ttk.Frame, app) -> None:
    """Page 3: show top-K suspicious nodes, Precision@K, export."""
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=0)
    frame.rowconfigure(1, weight=0)
    frame.rowconfigure(2, weight=1)
    frame.rowconfigure(3, weight=0)

    title = ttk.Label(
        frame,
        text="3. Results",
        style="Title.TLabel",
        anchor="w",
    )
    title.grid(row=0, column=0, sticky="we", padx=24, pady=(24, 8))

    # --- کنترل K و متن توضیح ---
    control_bar = ttk.Frame(frame)
    control_bar.grid(row=1, column=0, sticky="we", padx=24, pady=(0, 8))
    control_bar.columnconfigure(0, weight=0)
    control_bar.columnconfigure(1, weight=0)
    control_bar.columnconfigure(2, weight=1)

    k_label = ttk.Label(control_bar, text="K (top-K & Precision@K):")
    k_label.grid(row=0, column=0, sticky="w", padx=(0, 8))

    k_entry = ttk.Entry(control_bar, width=6)
    k_entry.insert(0, "50")
    k_entry.grid(row=0, column=1, sticky="w")

    info = ttk.Label(
    control_bar,
    text="Top suspicious nodes by PPR score.",
    style="Small.TLabel",
    anchor="w",
    justify="left",
)

    info.grid(row=1, column=0, columnspan=3, sticky="we", pady=(4, 0))

    # --- جدول ---
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

    # Tag برای fraudها (label=1)
    tree.tag_configure("fraud", background="#4a2b2b")  # قرمز تیره ملایم

    # --- نوار پایین: Export ---
    bottom_bar = ttk.Frame(frame)
    bottom_bar.grid(row=3, column=0, sticky="e", padx=24, pady=(0, 16))

    scores = app.state.scores
    labels = app.state.labels

    if scores is None or labels is None:
        info.configure(text="No results available. Run the analysis first.")

        bottom_bar = ttk.Frame(frame)
        bottom_bar.grid(row=3, column=0, sticky="e", padx=24, pady=(0, 16))

        back_btn = ttk.Button(
            bottom_bar,
            text="Back",
            command=lambda: app.show_page(2),
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

    # داده‌ی آخرین جدول (برای export)
    current_rows = []  # list of (rank, node, score, label)

    def refresh_for_k() -> None:
        nonlocal current_rows

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

        # پاک کردن جدول
        for item in tree.get_children():
            tree.delete(item)
        current_rows = []

        # مرتب‌سازی نزولی؛ برای UI حداکثر 20 سطر نشان بده
        order = np.argsort(scores)[::-1]

        # حداکثر تعداد ردیف قابل نمایش (برای کند نشدن UI)
        max_rows = 200
        n_rows = min(k_value, n, max_rows)

        top_display = order[:n_rows]


        # Retrieve the reverse map from the app state
        # Use getattr to avoid errors if reverse_map is not set yet
        rev_map = getattr(app.state, "reverse_map", None)

        for idx, node in enumerate(top_display, start=1):
            score = float(scores[node])
            lab = int(labels.get(int(node), 0))

            # Translate internal index to real node ID using reverse_map
            # If map exists, look it up; otherwise fallback to internal index
            real_node_id = rev_map[int(node)] if rev_map else int(node)

            # Use real_node_id for export data
            row_values = (idx, real_node_id, score, lab)
            current_rows.append(row_values)

            tags = ("fraud",) if lab == 1 else ()

            # Display real_node_id in the GUI table
            tree.insert(
                "",
                "end",
                values=(idx, real_node_id, f"{score:.6f}", lab),
                tags=tags,
            )


        # Precision@K
        from src.evaluation.metrics import precision_at_k

        k_eff = min(k_value, n)
        prec_k = precision_at_k(scores, labels, k_eff)

        extra = ""
        if k_value > max_rows:
            extra = f"\nOnly top {max_rows} rows shown in the table for performance."

        info.configure(
            text=(
                f"Top suspicious nodes by PPR score (top {len(top_display)} shown)."
                f"{extra}\n"
                f"Precision@{k_eff}: {prec_k:.3f}"
            )
        )


    def export_csv() -> None:
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

    # دکمه‌ی Apply K و Export
    apply_btn = ttk.Button(
        control_bar,
        text="Apply K",
        style="Nav.TButton",
        command=refresh_for_k,
    )
    apply_btn.grid(row=0, column=2, sticky="e")

        # --- نوار پایین: Back / Export / Close ---
    bottom_bar = ttk.Frame(frame)
    bottom_bar.grid(row=3, column=0, sticky="e", padx=24, pady=(0, 16))

    back_btn = ttk.Button(
        bottom_bar,
        text="Back",
        command=lambda: app.show_page(2),  # برگشت به صفحه Run
    )
    back_btn.pack(side="left", padx=(0, 8))

    # ایجاد Menubutton
    action_btn = ttk.Menubutton(
        bottom_bar,
        text="Actions ▼",
        style="Nav.TButton",  # اگر style داری
    )
    action_btn.pack(side="left", padx=(0, 8))

    # ایجاد منو
    action_menu = tk.Menu(action_btn, tearoff=0)
    action_btn["menu"] = action_menu

    # آیتم‌های منو
    action_menu.add_command(
        label="📊 Visualization",
        command=lambda: app.show_page(6)  # صفحه visualization
    )

    action_menu.add_command(
        label="💾 Export CSV",
        command=export_csv
    )

    action_menu.add_separator()  # خط جداکننده

    action_menu.add_command(
        label="➕ Add New Edge",
        command=lambda: app.show_page(8)  # صفحه add_edge (ایندکس جدید)
    )

    close_btn = ttk.Button(
        bottom_bar,
        text="Close",
        style="Danger.TButton",
        command=app.destroy,  # بستن کل برنامه
    )
    close_btn.pack(side="left")

    # اولین بار
    refresh_for_k()
