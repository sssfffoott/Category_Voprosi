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
        """Окно добавления темы (улучшенное)"""
        win = tk.Toplevel(self.app.root)
        win.title("Добавить тему")
        win.geometry("700x600")
        

        tk.Label(win, text="Название темы:", font=('Arial', 12, 'bold')).pack(pady=10)
        name_entry = tk.Entry(win, font=('Arial', 12), width=50)
        name_entry.pack(pady=5)
        
        tk.Label(win, text="Вопросы (каждый вопрос с новой строки):", 
                 font=('Arial', 12, 'bold')).pack(pady=10)
        tk.Label(win, text="Формат: текст вопроса | вариант1 | вариант2 | вариант3 | вариант4 | номер_правильного(0-4)", 
                 font=('Arial', 9), fg='gray').pack()
        
        text_area = tk.Text(win, font=('Arial', 10), height=15)
        text_area.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        

        def save():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Ошибка", "Введите название темы!")
                return
            if name in [c.name for c in self.app.data_manager.categories]:
                messagebox.showerror("Ошибка", "Такая тема уже существует!")
                return
            
            questions = []
            for line in text_area.get("1.0", tk.END).strip().split('\n'):
                if '|' not in line:
                    continue
                parts = [p.strip() for p in line.split('|')]
                if len(parts) == 6:
                    try:
                        q = Question(parts[0], parts[1:5], int(parts[5]), name)
                        questions.append(q)
                    except:
                        continue
            
            if len(questions) < 3:
                messagebox.showerror("Ошибка", "Добавьте минимум 3 вопроса!\nФормат: текст|вар1|вар2|вар3|вар4|индекс")
                return
            
            self.app.data_manager.add_category(Category(name, questions))
            messagebox.showinfo("Успех", f"Тема '{name}' добавлена! ({len(questions)} вопросов)")
            win.destroy()
        
        tk.Button(win, text="СОХРАНИТЬ", command=save, 
                  bg='green', fg='white', font=('Arial', 14, 'bold'),
                  width=20, height=2).pack(pady=20)

    def edit_category_window(self):
        if not self.app.data_manager.categories:
            messagebox.showinfo("Инфо", "Нет тем для редактирования")
            return

        win = tk.Toplevel(self.app.root)
        win.title("Редактировать")
        win.geometry("700x600")

        tk.Label(win, text="Выберите тему:", font=('Arial', 14, 'bold')).pack(pady=15)
        combo = ttk.Combobox(win,
                             values=[c.name for c in self.app.data_manager.categories],
                             font=('Arial', 13), width=30, state='readonly')
        combo.pack(pady=10)

        tk.Label(win, text="Новое название:", font=('Arial', 14)).pack(pady=(20, 5))
        name_entry = tk.Entry(win, font=('Arial', 13), width=50)
        name_entry.pack(pady=5)

        text_area = tk.Text(win, font=('Arial', 10))
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
            questions = []
            for line in text_area.get("1.0", tk.END).strip().split('\n'):
                if '|' not in line:
                    continue
                parts = [p.strip() for p in line.split('|')]
                if len(parts) == 6:
                    try:
                        q = Question(parts[0], parts[1:5], int(parts[5]), name_entry.get().strip())
                        questions.append(q)
                    except:
                        continue
            if len(questions) < 1:
                messagebox.showerror("Ошибка", "Нет вопросов!")
                return
            new_cat = Category(name_entry.get().strip(), questions)
            old_name = combo.get()
            if not old_name:
                messagebox.showerror("Ошибка", "Сначала выберите тему!")
                return
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
        win.geometry("400x250")

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
            self.app.data_manager.remove_category(name)
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

            for result in sorted(self.app.data_manager.results,
                                 key=lambda x: x['time'], reverse=True)[:20]:
                tree.insert('', 'end', values=(
                    result['time'],
                    result['user'],
                    f"{result['score']}/{result['total']}",
                    f"{result['percent']}%"
                ))

        tk.Button(self.app.frame, text="Админ панель",
                  command=self.show_menu, font=('Arial', 14)).pack(pady=20)