import tkinter as tk
from tkinter import messagebox, ttk
from models import Question, Category


class AdminPanel:
    def __init__(self, app):
        self.app = app

    def show_menu(self):
        self.app.create_frame()
        title = tk.Label(self.app.frame, text="АДМИНИСТРАТОР",
                         font=('Arial', 24, 'bold'), bg='lightblue')
        title.pack(pady=40)

        btn_frame1 = tk.Frame(self.app.frame)
        btn_frame1.pack(pady=15)
        tk.Button(btn_frame1, text="Добавить тему",
                  command=self.add_category_window, bg='lightgreen',
                  font=('Arial', 16), width=18, height=2).pack(side=tk.LEFT, padx=15)
        tk.Button(btn_frame1, text="Редактировать",
                  command=self.edit_category_window, bg='yellow',
                  font=('Arial', 16), width=18, height=2).pack(side=tk.LEFT, padx=15)

        btn_frame2 = tk.Frame(self.app.frame)
        btn_frame2.pack(pady=15)
        tk.Button(btn_frame2, text="Удалить тему",
                  command=self.delete_category_window, bg='lightcoral',
                  font=('Arial', 16), width=18, height=2).pack(side=tk.LEFT, padx=15)
        tk.Button(btn_frame2, text="Результаты",
                  command=self.show_results, bg='lightcyan',
                  font=('Arial', 16), width=18, height=2).pack(side=tk.LEFT, padx=15)

        tk.Button(self.app.frame, text="Главное меню",
                  command=self.app.show_login, font=('Arial', 14),
                  bg='orange').pack(pady=30)

    def add_category_window(self):
        win = tk.Toplevel(self.app.root)
        win.title("Новая тема")
        win.geometry("650x650")
        win.resizable(False, False)

        tk.Label(win, text="Название:", font=('Arial', 14, 'bold')).pack(pady=15)
        name_entry = tk.Entry(win, font=('Arial', 13), width=50)
        name_entry.pack(pady=5)

        tk.Label(win, text="Вопросы (текст|опц1|опц2|опц3|опц4|индекс): каждый - новая строка",
                 font=('Arial', 11), anchor='w').pack(pady=(20, 5), padx=20)

        text_area = tk.Text(win, height=28, width=75, font=('Arial', 10))
        text_area.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        def save():
            name = name_entry.get().strip()
            if name in [c.name for c in self.app.data_manager.categories]:
                messagebox.showerror("Ошибка", "Тема существует!")
                return
            if len(name) < 3:
                messagebox.showerror("Ошибка", "Название короче 3 символов!")
                return

            questions = self.parse_questions(text_area.get("1.0", tk.END))
            if len(questions) < 3:
                messagebox.showerror("Ошибка", "Минимум 3 вопроса!")
                return

            category = Category(name, questions)
            self.app.data_manager.add_category(category)
            messagebox.showinfo("Успех", f"Добавлено {len(questions)} вопросов!")
            win.destroy()

        tk.Button(win, text="СОХРАНИТЬ", command=save, bg='green',
                  fg='white', font=('Arial', 14, 'bold'), width=20, height=2).pack(pady=20)

    def parse_questions(self, text):
        questions = []
        for line_num, line in enumerate(text.strip().split('\n'), 1):
            line = line.strip()
            if '|' not in line or not line: continue

            parts = [p.strip() for p in line.split('|')]
            if len(parts) == 6:
                try:
                    corr = int(parts[5])
                    if 0 <= corr < 4:
                        q = Question(parts[0], parts[1:5], corr, "")
                        questions.append(q)
                except ValueError:
                    continue
        return questions

    def edit_category_window(self):
        if not self.app.data_manager.categories:
            messagebox.showinfo("Инфо", "Нет тем для редактирования")
            return

        win = tk.Toplevel(self.app.root)
        win.title("Редактировать")
        win.geometry("650x650")

        tk.Label(win, text="Выберите тему:", font=('Arial', 14, 'bold')).pack(pady=15)
        combo = ttk.Combobox(win, values=[c.name for c in self.app.data_manager.categories],
                             font=('Arial', 13), width=30, state='readonly')
        combo.pack(pady=10)

        tk.Label(win, text="Новое название:", font=('Arial', 14)).pack(pady=(20, 5))
        name_entry = tk.Entry(win, font=('Arial', 13), width=50)
        name_entry.pack(pady=5)

        text_area = tk.Text(win, height=25, width=75, font=('Arial', 10))
        text_area.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        def load_data():
            cat = self.app.data_manager.get_category(combo.get())
            if cat:
                name_entry.delete(0, tk.END)
                name_entry.insert(0, cat.name)
                text_area.delete("1.0", tk.END)
                for q in cat.questions:
                    line = f"{q.text}|{q.options[0]}|{q.options[1]}|{q.options[2]}|{q.options[3]}|{q.correct_index}"
                    text_area.insert(tk.END, line + '\n')

        tk.Button(win, text="Загрузить", command=load_data,
                  bg='blue', fg='white').pack(pady=10)

        def save():
            questions = self.parse_questions(text_area.get("1.0", tk.END))
            if len(questions) < 1:
                messagebox.showerror("Ошибка", "Нет вопросов!")
                return
            new_cat = Category(name_entry.get().strip(), questions)
            old_name = combo.get()
            self.app.data_manager.remove_category(old_name)
            self.app.data_manager.add_category(new_cat)
            messagebox.showinfo("Успех", "Сохранено!")
            win.destroy()

        tk.Button(win, text="СОХРАНИТЬ", command=save, bg='green',
                  fg='white', font=('Arial', 14, 'bold')).pack(pady=20)

    def delete_category_window(self):
        if not self.app.data_manager.categories:
            messagebox.showinfo("Инфо", "Нет тем")
            return

        win = tk.Toplevel(self.app.root)
        win.title("Удалить")
        win.geometry("400x200")

        tk.Label(win, text="Выберите тему для удаления:", font=('Arial', 14)).pack(pady=20)
        combo = ttk.Combobox(win, values=[c.name for c in self.app.data_manager.categories],
                             width=30, state='readonly')
        combo.pack(pady=10)

        def delete():
            self.app.data_manager.remove_category(combo.get())
            messagebox.showinfo("Успех", "Удалено!")
            win.destroy()

        tk.Button(win, text="УДАЛИТЬ", command=delete, bg='red',
                  fg='white', font=('Arial', 14, 'bold')).pack(pady=20)

    def show_results(self):
        self.app.create_frame()
        title = tk.Label(self.app.frame, text="РЕЗУЛЬТАТЫ",
                         font=('Arial', 22, 'bold'), bg='lightblue')
        title.pack(pady=30)

        if not self.app.data_manager.results:
            tk.Label(self.app.frame, text="Нет результатов",
                     font=('Arial', 18), fg='gray').pack(pady=50)
        else:
            cols = ('Время', 'Пользователь', 'Очки', '%')
            tree = ttk.Treeview(self.app.frame, columns=cols, show='headings', height=15)

            for col in cols:
                tree.heading(col, text=col)
                tree.column(col, width=120)
            tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

            for result in sorted(self.app.data_manager.results, key=lambda x: x['time'], reverse=True)[:20]:
                tree.insert('', 'end', values((
                    result['time'],
                    result['user'],
                    f"{result['score']}/{result['total']}",
                    f"{result['percent']}%"
                )))

        tk.Button(self.app.frame, text="Админ панель",
                  command=self.show_menu, font=('Arial', 14)).pack(pady=20)
