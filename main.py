import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os
from datetime import datetime

# Предопределённые задачи с типами
PREDEFINED_TASKS = [
    {"text": "Прочитать статью", "type": "учёба"},
    {"text": "Сделать зарядку", "type": "спорт"},
    {"text": "Написать отчёт", "type": "работа"},
    {"text": "Выучить 10 новых слов", "type": "учёба"},
    {"text": "Пробежка 30 минут", "type": "спорт"},
    {"text": "Провести встречу", "type": "работа"},
    {"text": "Посмотреть лекцию", "type": "учёба"},
    {"text": "Отжимания", "type": "спорт"},
    {"text": "Сделать бэклог", "type": "работа"}
]

HISTORY_FILE = "tasks.json"

class TaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("600x500")
        self.root.resizable(True, True)

        # Хранилище истории задач
        self.history = []  # каждый элемент: {"task": str, "type": str, "timestamp": str}
        self.load_history()

        # Переменные фильтра
        self.filter_var = tk.StringVar(value="все")

        # Интерфейс
        self.create_widgets()
        self.update_history_display()

    def create_widgets(self):
        # Рамка для генерации
        frame_gen = tk.LabelFrame(self.root, text="Генерация задачи", padx=10, pady=10)
        frame_gen.pack(fill="x", padx=10, pady=5)

        self.btn_generate = tk.Button(frame_gen, text="Сгенерировать задачу", command=self.generate_task, bg="lightblue")
        self.btn_generate.pack(pady=5)

        self.lbl_task = tk.Label(frame_gen, text="Нажмите кнопку", font=("Arial", 12, "bold"), fg="green")
        self.lbl_task.pack(pady=5)

        # Рамка для добавления новой задачи
        frame_add = tk.LabelFrame(self.root, text="Добавить новую задачу", padx=10, pady=10)
        frame_add.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_add, text="Задача:").grid(row=0, column=0, sticky="w")
        self.entry_task = tk.Entry(frame_add, width=30)
        self.entry_task.grid(row=0, column=1, padx=5)

        tk.Label(frame_add, text="Тип:").grid(row=1, column=0, sticky="w")
        self.combo_type = ttk.Combobox(frame_add, values=["учёба", "спорт", "работа"], state="readonly")
        self.combo_type.grid(row=1, column=1, padx=5)
        self.combo_type.current(0)

        self.btn_add = tk.Button(frame_add, text="Добавить", command=self.add_task)
        self.btn_add.grid(row=2, column=0, columnspan=2, pady=5)

        # Фильтр
        frame_filter = tk.LabelFrame(self.root, text="Фильтр по типу", padx=10, pady=10)
        frame_filter.pack(fill="x", padx=10, pady=5)

        filter_frame = tk.Frame(frame_filter)
        filter_frame.pack()

        tk.Radiobutton(filter_frame, text="Все", variable=self.filter_var, value="все", command=self.update_history_display).pack(side="left", padx=10)
        tk.Radiobutton(filter_frame, text="Учёба", variable=self.filter_var, value="учёба", command=self.update_history_display).pack(side="left", padx=10)
        tk.Radiobutton(filter_frame, text="Спорт", variable=self.filter_var, value="спорт", command=self.update_history_display).pack(side="left", padx=10)
        tk.Radiobutton(filter_frame, text="Работа", variable=self.filter_var, value="работа", command=self.update_history_display).pack(side="left", padx=10)

        # История
        frame_history = tk.LabelFrame(self.root, text="История задач", padx=10, pady=10)
        frame_history.pack(fill="both", expand=True, padx=10, pady=5)

        scrollbar = tk.Scrollbar(frame_history)
        scrollbar.pack(side="right", fill="y")

        self.listbox_history = tk.Listbox(frame_history, yscrollcommand=scrollbar.set, height=12)
        self.listbox_history.pack(fill="both", expand=True)

        scrollbar.config(command=self.listbox_history.yview)

        # Кнопка очистки истории
        self.btn_clear = tk.Button(self.root, text="Очистить историю", command=self.clear_history, bg="salmon")
        self.btn_clear.pack(pady=5)

    def generate_task(self):
        """Выбирает случайную задачу из предопределённого списка + пользовательских"""
        all_tasks = PREDEFINED_TASKS + self.get_custom_tasks_from_history()
        if not all_tasks:
            messagebox.showwarning("Нет задач", "Добавьте хотя бы одну задачу вручную или перезапустите программу.")
            return

        chosen = random.choice(all_tasks)
        task_text = chosen["text"]
        task_type = chosen["type"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.history.append({
            "task": task_text,
            "type": task_type,
            "timestamp": timestamp
        })
        self.save_history()
        self.lbl_task.config(text=f"🎲 {task_text} ({task_type})")
        self.update_history_display()

    def get_custom_tasks_from_history(self):
        """Извлекает уникальные пользовательские задачи (не из PREDEFINED_TASKS)"""
        predefined_texts = {t["text"] for t in PREDEFINED_TASKS}
        custom = []
        for item in self.history:
            if item["task"] not in predefined_texts:
                custom.append({"text": item["task"], "type": item["type"]})
        # Уникальность по тексту
        seen = set()
        unique = []
        for c in custom:
            if c["text"] not in seen:
                seen.add(c["text"])
                unique.append(c)
        return unique

    def add_task(self):
        """Добавляет новую задачу в историю (как сгенерированную пользователем)"""
        task_text = self.entry_task.get().strip()
        task_type = self.combo_type.get()

        if not task_text:
            messagebox.showerror("Ошибка", "Задача не может быть пустой строкой.")
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append({
            "task": task_text,
            "type": task_type,
            "timestamp": timestamp + " (добавлено вручную)"
        })
        self.save_history()
        self.update_history_display()
        self.entry_task.delete(0, tk.END)
        messagebox.showinfo("Успех", f"Задача '{task_text}' добавлена!")

    def update_history_display(self):
        """Обновляет список истории с учётом фильтра"""
        self.listbox_history.delete(0, tk.END)
        filter_value = self.filter_var.get()

        filtered = self.history
        if filter_value != "все":
            filtered = [item for item in self.history if item["type"] == filter_value]

        for item in filtered:
            display_text = f"[{item['timestamp']}] {item['task']} ({item['type']})"
            self.listbox_history.insert(tk.END, display_text)

    def save_history(self):
        """Сохраняет историю в JSON"""
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def load_history(self):
        """Загружает историю из JSON, если файл существует"""
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except:
                self.history = []
        else:
            self.history = []

    def clear_history(self):
        """Очищает историю после подтверждения"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            self.history = []
            self.save_history()
            self.update_history_display()
            self.lbl_task.config(text="История очищена")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGeneratorApp(root)
    root.mainloop()