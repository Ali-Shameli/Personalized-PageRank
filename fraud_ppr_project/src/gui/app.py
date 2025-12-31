# gui/app.py
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from gui.theme import apply_dark_theme
from gui.pages.welcome_page import build_welcome_page


class WizardApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Fraud Detection via Personalized PageRank")
        self.geometry("900x600")
        self.minsize(800, 500)

        # تم
        self.style = apply_dark_theme(self)

        # کانتینر اصلی برای صفحات
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        # فقط صفحه‌ی welcome برای این کامیت
        self.current_frame = ttk.Frame(container)
        self.current_frame.grid(row=0, column=0, sticky="nsew")

        build_welcome_page(self.current_frame, go_next=self._go_next_placeholder)

    def _go_next_placeholder(self) -> None:
        # بعداً این را به logic واقعی ویزارد وصل می‌کنیم
        print("Next page (not implemented yet)")


def run_app() -> None:
    app = WizardApp()
    app.mainloop()
