import tkinter as tk
from tkinter import ttk, messagebox

"""
Aircraft / Air‑Vehicle Code Generator
====================================
Supports:   Plane ✈️, Helicopter 🚁, Dirigible 🛩️, VTOL 🛫
Code style: <craft>-<engine>@S<speed>|W<weight>k|B<tanks>
Example:    heli-jet@S320|W9k|B3 → вертолёт • реактивный • 320 км/ч • 9 т • 3 бака
"""

# ----------------------------------
# Dictionaries
# ----------------------------------
CRAFT_TYPES = [
    ("plane", "Самолёт"),
    ("heli", "Вертолёт"),
    ("dir", "Дирижабль"),
    ("vtol", "VTOL (верт.)"),
]

ENGINES = [
    ("prop", "Пропеллерный"),
    ("turb", "Турбовинтовой"),
    ("jet", "Реактивный"),
    ("rocket", "Ракетный"),
    ("elec", "Электрический"),
]

# ----------------------------------
# Helper
# ----------------------------------

def generate_code():
    craft_code = craft_var.get()
    engine_code = engine_var.get()
    speed = speed_var.get()
    weight = weight_var.get()
    tanks = tanks_var.get()

    # Validation
    if not craft_code:
        messagebox.showerror("Ошибка", "Выберите тип аппарата.")
        return
    if not engine_code:
        messagebox.showerror("Ошибка", "Выберите тип двигателя.")
        return
    if not (speed.isdigit() and int(speed) > 0):
        messagebox.showerror("Ошибка", "Скорость должна быть положительным целым числом (км/ч).")
        return
    if not (weight.isdigit() and int(weight) > 0):
        messagebox.showerror("Ошибка", "Вес должен быть положительным целым числом (т).")
        return
    if not (tanks.isdigit() and 0 < int(tanks) < 10):
        messagebox.showerror("Ошибка", "Кол-во баков 1‑9.")
        return

    code = f"{craft_code}-{engine_code}@S{speed}|W{weight}k|B{tanks}"
    result_var.set(code)

    root.clipboard_clear()
    root.clipboard_append(code)
    messagebox.showinfo("Код скопирован", code)

# ----------------------------------
# UI
# ----------------------------------
root = tk.Tk()
root.title("Air‑Vehicle Code Generator")
root.resizable(False, False)

main = ttk.Frame(root, padding=12)
main.grid(sticky=(tk.N, tk.W, tk.E, tk.S))

# Variables
craft_var = tk.StringVar()
engine_var = tk.StringVar()
speed_var = tk.StringVar()
weight_var = tk.StringVar()
tanks_var = tk.StringVar()
result_var = tk.StringVar()

# Craft type
ttk.Label(main, text="Тип аппарата:").grid(row=0, column=0, sticky=tk.W)
craft_combo = ttk.Combobox(main, state="readonly", width=18)
craft_combo['values'] = [f"{c[0]} — {c[1]}" for c in CRAFT_TYPES]
craft_combo.grid(row=0, column=1, pady=2, sticky=tk.EW)
craft_combo.bind("<<ComboboxSelected>>", lambda e: craft_var.set(craft_combo.get().split(' ')[0]))

# Engine type
ttk.Label(main, text="Тип двигателя:").grid(row=1, column=0, sticky=tk.W)
engine_combo = ttk.Combobox(main, state="readonly", width=18)
engine_combo['values'] = [f"{e[0]} — {e[1]}" for e in ENGINES]
engine_combo.grid(row=1, column=1, pady=2, sticky=tk.EW)
engine_combo.bind("<<ComboboxSelected>>", lambda e: engine_var.set(engine_combo.get().split(' ')[0]))

# Speed
ttk.Label(main, text="Скорость (км/ч):").grid(row=2, column=0, sticky=tk.W)
entry_speed = ttk.Entry(main, textvariable=speed_var, width=20)
entry_speed.grid(row=2, column=1, pady=2, sticky=tk.EW)

# Weight
ttk.Label(main, text="Вес (т):").grid(row=3, column=0, sticky=tk.W)
entry_weight = ttk.Entry(main, textvariable=weight_var, width=20)
entry_weight.grid(row=3, column=1, pady=2, sticky=tk.EW)

# Tanks
ttk.Label(main, text="Баков:").grid(row=4, column=0, sticky=tk.W)
entry_tanks = ttk.Entry(main, textvariable=tanks_var, width=20)
entry_tanks.grid(row=4, column=1, pady=2, sticky=tk.EW)

# Generate button
btn = ttk.Button(main, text="Сгенерировать код", command=generate_code)
btn.grid(row=5, column=0, columnspan=2, pady=(6, 4))

# Result
ttk.Label(main, text="Код:").grid(row=6, column=0, sticky=tk.W)
entry_result = ttk.Entry(main, textvariable=result_var, width=30, state="readonly")
entry_result.grid(row=6, column=1, pady=2, sticky=tk.EW)

# Padding
for child in main.winfo_children():
    child.grid_configure(padx=4)

root.mainloop()
