from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Dict

from .pages.load_page import build_load_page
from .theme import apply_dark_theme
from .pages.welcome_page import build_welcome_page
# بعداً: از این‌جا load/run/results را هم ایمپورت می‌کنیم

class AppState:
    def __init__(self) -> None:
        self.data_path: str | None = None
        self.data_source: str | None = None  # e.g. "sample_small", "sample_bitcoin", "custom"

class WizardApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.state = AppState()

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

        # نگه‌داری صفحات
        self._container = container
        self.frames: Dict[int, ttk.Frame] = {}

        # فعلاً فقط صفحه ۰ (Welcome)
        self._create_page(0)

        # نمایش صفحه اول
        self.show_page(0)

    # ---------- صفحه‌ها ----------

    def _create_page(self, index: int) -> None:
        if index in self.frames:
            return

        frame = ttk.Frame(self._container)
        frame.grid(row=0, column=0, sticky="nsew")
        self.frames[index] = frame

        if index == 0:
            build_welcome_page(frame, app=self)
        elif index == 1:
            build_load_page(frame, app=self)
        # بعداً: elif index == 2: build_run_page(...)
        #       elif index == 3: build_results_page(...)

    def show_page(self, index: int) -> None:
        """Show the page with given index."""
        # اگر ساخته نشده، بساز
        self._create_page(index)

        frame = self.frames[index]
        frame.tkraise()

    # این‌ها را فعلاً ساده نگه می‌داریم، بعداً پرشان می‌کنیم
    def show_how_it_works(self) -> None:
        tk.messagebox.showinfo(
            "How it works",
            "This will explain the Personalized PageRank-based fraud detection.",
        )

    def show_about(self) -> None:
        tk.messagebox.showinfo(
            "About",
            "Fraud Detection via Personalized PageRank.\nCourse project.",
        )


def run_app() -> None:
    app = WizardApp()
    app.mainloop()
