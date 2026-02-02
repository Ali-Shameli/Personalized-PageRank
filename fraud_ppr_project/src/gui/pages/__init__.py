# در فایل src/gui/pages/results_page.py

def build_results_page(frame: ttk.Frame, app: "WizardApp") -> None:
    # ... (کدهای تایتل و اینپوت‌ها در ردیف‌های ۰ و ۱) ...

    # ... (کدهای جدول Treeview که در ردیف ۲ هستند) ...
    # tree.grid(row=2, column=0, sticky="nsew", padx=24, pady=(0, 8)) <-- معمولاً اینجا تمام می‌شود

    # ==========================================
    # ### شروع تغییرات جدید (تایم پایین جدول) ###

    # ۱. تبدیل ثانیه به میلی‌ثانیه (ضرب در ۱۰۰۰)
    ms_time = app.state.execution_time * 1000

    # ۲. ساخت متن (مثلاً: Execution Time: 45.20 ms)
    # اگر متد پاور بود اسمش رو بنویس، اگر نه مونته کارلو
    algo_name = "Power Iteration" if app.state.last_algorithm == "power" else "Monte Carlo"
    time_text = f"Method: {algo_name}  |  Time: {ms_time:.2f} ms"

    # ۳. نمایش در پایین صفحه سمت چپ (Row 3)
    # استایل Small.TLabel برای اینکه خیلی گنده نباشه، ولی خوانا باشه
    time_label = ttk.Label(
        frame,
        text=time_text,
        style="Small.TLabel",
        foreground="#4caf50"  # رنگ سبز ملایم (یا هر رنگی که دوست داری)
    )
    # sticky="w" یعنی بچسبه به سمت چپ (West)
    time_label.grid(row=3, column=0, sticky="w", padx=24, pady=(5, 0))

    # ### پایان تغییرات ###
    # ==========================================

    # (ادامه کدها: دکمه‌های نویگیشن و غیره...)