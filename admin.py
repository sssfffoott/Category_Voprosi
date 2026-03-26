import tkinter as tk
from tkinter import messagebox, ttk
from models import Question, Category


class AdminPanel:
    def __init__(self, app):
        self.app = app

    def show_menu(self):
        self.app.create_frame()
        
        # Создаем контейнер для центрирования
        container = tk.Frame(self.app.frame, bg='lightblue')
        container.pack(fill=tk.BOTH, expand=True)
        
        title = tk.Label(container, text="АДМИНИСТРАТОР",
                         font=('Arial', 24, 'bold'), bg='lightblue')
        title.pack(pady=30)

        btn_frame1 = tk.Frame(container, bg='lightblue')
        btn_frame1.pack(pady=10)
        tk.Button(btn_frame1, text="Добавить тему",
                  command=self.add_category_window, bg='lightgreen',
                  font=('Arial', 14), width=18, height=2).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame1, text="Редактировать",
                  command=self.edit_category_window, bg='yellow',
                  font=('Arial', 14), width=18, height=2).pack(side=tk.LEFT, padx=10)

        btn_frame2 = tk.Frame(container, bg='lightblue')
        btn_frame2.pack(pady=10)
        tk.Button(btn_frame2, text="Удалить тему",
                  command=self.delete_category_window, bg='lightcoral',
                  font=('Arial', 14), width=18, height=2).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame2, text="Результаты",
                  command=self.show_results, bg='lightcyan',
                  font=('Arial', 14), width=18, height=2).pack(side=tk.LEFT, padx=10)

        tk.Button(container, text="Главное меню",
                  command=self.app.show_login, font=('Arial', 14),
                  bg='orange').pack(pady=20)

    def add_category_window(self):
        win = tk.Toplevel(self.app.root)
        win.title("Новая тема")
        win.geometry("700x600")
        win.minsize(600, 500)

        # Настройка сетки для масштабирования
        win.grid_rowconfigure(4, weight=1)
        win.grid_columnconfigure(0, weight=1)

        tk.Label(win, text="Название:", font=('Arial', 14, 'bold')).grid(row=0, column=0, pady=10)
        name_entry = tk.Entry(win, font=('Arial', 13), width=50)
        name_entry.grid(row=1, column=0, pady=5)

        tk.Label(win, text="Вопросы (текст|опц1|опц2|опц3|опц4|индекс):\nкаждый вопрос - новая строка",
                 font=('Arial', 11), anchor='w', justify='left').grid(row=2, column=0, pady=(10, 5), padx=20)

        text_area = tk.Text(win, font=('Arial', 10))
        text_area.grid(row=3, column=0, pady=10, padx=20, sticky="nsew")

        def save():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Ошибка", "Название не может быть пустым!")
                return
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

            for q in questions:
                q.category = name

            category = Category(name, questions)
            self.app.data_manager.add_category(category)
            messagebox.showinfo("Успех", f"Добавлено {len(questions)} вопросов!")
            win.destroy()

        tk.Button(win, text="СОХРАНИТЬ", command=save, bg='green',
                  fg='white', font=('Arial', 14, 'bold'), width=20, height=2).grid(row=4, column=0, pady=20)

    def parse_questions(self, text):
        questions = []
        for line in text.strip().split('\n'):
            line = line.strip()
            if '|' not in line or not line:
                continue

            parts = [p.strip() for p in line.split('|')]
            if len(parts) == 6:
                try:
                    corr = int(parts[5])
                    if 0 <= corr < 4:
                        q = Question(parts[0], parts[1:5], corr, "")
                        questions.append(q)
                except (ValueError, IndexError):
                    continue
        return questions

    def edit_category_window(self):
        if not self.app.data_manager.categories:
            messagebox.showinfo("Инфо", "Нет тем для редактирования")
            return

        win = tk.Toplevel(self.app.root)
        win.title("Редактировать тему")
        win.geometry("700x600")
        win.minsize(600, 500)

        win.grid_rowconfigure(6, weight=1)
        win.grid_columnconfigure(0, weight=1)

        tk.Label(win, text="Выберите тему:", font=('Arial', 14, 'bold')).grid(row=0, column=0, pady=10)
        combo = ttk.Combobox(win,
                             values=[c.name for c in self.app.data_manager.categories],
                             font=('Arial', 13), width=30, state='readonly')
        combo.grid(row=1, column=0, pady=5)

        tk.Label(win, text="Новое название:", font=('Arial', 14)).grid(row=2, column=0, pady=(10, 5))
        name_entry = tk.Entry(win, font=('Arial', 13), width=50)
        name_entry.grid(row=3, column=0, pady=5)

        tk.Label(win, text="Вопросы (текст|опц1|опц2|опц3|опц4|индекс):", 
                 font=('Arial', 11)).grid(row=4, column=0, pady=(10, 5))
        
        text_area = tk.Text(win, font=('Arial', 10))
        text_area.grid(row=5, column=0, pady=10, padx=20, sticky="nsew")

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
                  bg='blue', fg='white', font=('Arial', 12)).grid(row=1, column=0, pady=5)

        def save():
            questions = self.parse_questions(text_area.get("1.0", tk.END))
            if len(questions) < 1:
                messagebox.showerror("Ошибка", "Нет вопросов!")
                return
            new_name = name_entry.get().strip()
            if not new_name:
                messagebox.showerror("Ошибка", "Название не может быть пустым!")
                return
            
            for q in questions:
                q.category = new_name
                
            new_cat = Category(new_name, questions)
            old_name = combo.get()
            if not old_name:
                messagebox.showerror("Ошибка", "Сначала выберите тему!")
                return
            self.app.data_manager.remove_category(old_name)
            self.app.data_manager.add_category(new_cat)
            messagebox.showinfo("Успех", "Сохранено!")
            win.destroy()

        tk.Button(win, text="СОХРАНИТЬ", command=save, bg='green',
                  fg='white', font=('Arial', 14, 'bold'), width=20).grid(row=6, column=0, pady=20)

    def delete_category_window(self):
        if not self.app.data_manager.categories:
            messagebox.showinfo("Инфо", "Нет тем")
            return

        win = tk.Toplevel(self.app.root)
        win.title("Удалить тему")
        win.geometry("400x250")
        win.resizable(False, False)

        tk.Label(win, text="Выберите тему для удаления:", font=('Arial', 14)).pack(pady=20)
        combo = ttk.Combobox(win,
                             values=[c.name for c in self.app.data_manager.categories],
                             width=30, state='readonly')
        combo.pack(pady=10)

        def delete():
            name = combo.get()
            if not name:
                messagebox.showerror("Ошибка", "Сначала выберите тему!")
                return
            if messagebox.askyesno("Подтверждение", f"Удалить тему '{name}'?"):
                self.app.data_manager.remove_category(name)
                messagebox.showinfo("Успех", "Тема удалена!")
                win.destroy()

        tk.Button(win, text="УДАЛИТЬ", command=delete, bg='red',
                  fg='white', font=('Arial', 14, 'bold'), width=15).pack(pady=20)

    def show_results(self):
        self.app.create_frame()
        
        container = tk.Frame(self.app.frame, bg='lightblue')
        container.pack(fill=tk.BOTH, expand=True)
        
        title = tk.Label(container, text="РЕЗУЛЬТАТЫ",
                         font=('Arial', 22, 'bold'), bg='lightblue')
        title.pack(pady=20)

        if not self.app.data_manager.results:
            tk.Label(container, text="Нет результатов",
                     font=('Arial', 18), fg='gray', bg='lightblue').pack(pady=50)
        else:
            # Создаем фрейм для таблицы с прокруткой
            tree_frame = tk.Frame(container)
            tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            scrollbar = ttk.Scrollbar(tree_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            cols = ('Время', 'Пользователь', 'Очки', '%')
            tree = ttk.Treeview(tree_frame, columns=cols, show='headings', 
                                yscrollcommand=scrollbar.set, height=15)
            scrollbar.config(command=tree.yview)

            for col in cols:
                tree.heading(col, text=col)
                tree.column(col, width=150, anchor='center')
            tree.pack(fill=tk.BOTH, expand=True)

            for result in sorted(self.app.data_manager.results,
                                 key=lambda x: x['time'], reverse=True)[:20]:
                tree.insert('', 'end', values=(
                    result['time'],
                    result['user'],
                    f"{result['score']}/{result['total']}",
                    f"{result['percent']}%"
                ))

        tk.Button(container, text="Админ панель",
                  command=self.show_menu, font=('Arial', 14)).pack(pady=15)