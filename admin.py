import tkinter as tk
from tkinter import messagebox, ttk
from models import Question, Category


class AdminPanel:
    def __init__(self, app):
        self.app = app

    def show_menu(self):
        self.app.create_frame()

        # Контейнер для центрирования
        container = tk.Frame(self.app.frame, bg='lightblue')
        container.pack(expand=True)

        title = tk.Label(container, text="АДМИНИСТРАТОР",
                         font=('Arial', 24, 'bold'), bg='lightblue')
        title.pack(pady=40)

        btn_frame1 = tk.Frame(container, bg='lightblue')
        btn_frame1.pack(pady=15)
        tk.Button(btn_frame1, text="Добавить тему",
                  command=self.add_category_window, bg='lightgreen',
                  font=('Arial', 16), width=18, height=2).pack(side=tk.LEFT, padx=15)
        tk.Button(btn_frame1, text="Редактировать",
                  command=self.edit_category_window, bg='yellow',
                  font=('Arial', 16), width=18, height=2).pack(side=tk.LEFT, padx=15)

        btn_frame2 = tk.Frame(container, bg='lightblue')
        btn_frame2.pack(pady=15)
        tk.Button(btn_frame2, text="Удалить тему",
                  command=self.delete_category_window, bg='lightcoral',
                  font=('Arial', 16), width=18, height=2).pack(side=tk.LEFT, padx=15)
        tk.Button(btn_frame2, text="Результаты",
                  command=self.show_results, bg='lightcyan',
                  font=('Arial', 16), width=18, height=2).pack(side=tk.LEFT, padx=15)

        tk.Button(container, text="Главное меню",
                  command=self.app.show_login, font=('Arial', 14),
                  bg='orange').pack(pady=30)

    def add_category_window(self):
        win = tk.Toplevel(self.app.root)
        win.title("Добавить тему")
        win.geometry("950x700")

        main_container = tk.Frame(win)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        tk.Label(main_container, text="Название темы:", font=('Arial', 12, 'bold')).pack(pady=10)
        name_entry = tk.Entry(main_container, font=('Arial', 12), width=50)
        name_entry.pack(pady=5)

        tk.Label(main_container, text="Вопросы (каждый вопрос с новой строки):",
                 font=('Arial', 12, 'bold')).pack(pady=10)
        tk.Label(main_container,
                 text="Формат: текст вопроса | вариант1 | вариант2 | вариант3 | вариант4 | номер_правильного(0-3)",
                 font=('Arial', 9), fg='gray').pack()

        text_frame = tk.Frame(main_container)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_area = tk.Text(text_frame, font=('Arial', 10), yscrollcommand=scrollbar.set)
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_area.yview)


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
                messagebox.showerror("Ошибка", "Добавьте минимум 3 вопроса!")
                return

            self.app.data_manager.add_category(Category(name, questions))
            messagebox.showinfo("Успех", f"Тема '{name}' добавлена! ({len(questions)} вопросов)")
            win.destroy()

        tk.Button(main_container, text="СОХРАНИТЬ", command=save,
                  bg='green', fg='white', font=('Arial', 14, 'bold'),
                  width=20, height=2).pack(pady=20)

    def edit_category_window(self):
        if not self.app.data_manager.categories:
            messagebox.showinfo("Инфо", "Нет тем для редактирования")
            return

        win = tk.Toplevel(self.app.root)
        win.title("Редактировать тему")
        win.geometry("950x750")
        win.minsize(700, 550)

        # Настройка сетки для масштабирования всего окна
        win.grid_rowconfigure(0, weight=1)
        win.grid_columnconfigure(0, weight=1)

        # Основной контейнер
        main_container = tk.Frame(win)
        main_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_container.grid_rowconfigure(4, weight=1)  # Строка с текстовым полем расширяется
        main_container.grid_columnconfigure(0, weight=1)

        # Выбор темы
        tk.Label(main_container, text="Выберите тему для редактирования:",
                 font=('Arial', 12, 'bold')).grid(row=0, column=0, pady=(0, 5), sticky="w")

        combo_frame = tk.Frame(main_container)
        combo_frame.grid(row=1, column=0, pady=(0, 10), sticky="ew")
        combo_frame.grid_columnconfigure(0, weight=1)

        combo = ttk.Combobox(combo_frame,
                             values=[c.name for c in self.app.data_manager.categories],
                             font=('Arial', 12), state='readonly')
        combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        tk.Button(combo_frame, text="Загрузить",
                  command=lambda: load_data(),
                  bg='blue', fg='white', font=('Arial', 11),
                  width=12).pack(side=tk.RIGHT)

        # Разделитель
        ttk.Separator(main_container, orient='horizontal').grid(row=2, column=0, sticky="ew", pady=10)

        # Название темы
        tk.Label(main_container, text="Название темы:", font=('Arial', 12, 'bold')).grid(row=3, column=0, pady=(10, 5),
                                                                                         sticky="w")
        name_entry = tk.Entry(main_container, font=('Arial', 12))
        name_entry.grid(row=4, column=0, sticky="ew", pady=(0, 10))

        # Вопросы
        tk.Label(main_container, text="Вопросы (формат: текст|вар1|вар2|вар3|вар4|индекс):",
                 font=('Arial', 12, 'bold')).grid(row=5, column=0, pady=(10, 5), sticky="w")

        # Текстовое поле с прокруткой
        text_frame = tk.Frame(main_container)
        text_frame.grid(row=6, column=0, sticky="nsew", pady=5)
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.grid(row=0, column=1, sticky="ns")

        text_area = tk.Text(text_frame, font=('Arial', 10),
                            yscrollcommand=scrollbar.set, wrap=tk.WORD)
        text_area.grid(row=0, column=0, sticky="nsew")
        scrollbar.config(command=text_area.yview)

        # Кнопки
        btn_frame = tk.Frame(main_container)
        btn_frame.grid(row=7, column=0, pady=20)

        tk.Button(btn_frame, text="СОХРАНИТЬ", command=lambda: save(),
                  bg='green', fg='white', font=('Arial', 12, 'bold'),
                  width=15, height=2).pack(side=tk.LEFT, padx=10)

        tk.Button(btn_frame, text="ОТМЕНА", command=win.destroy,
                  bg='red', fg='white', font=('Arial', 12, 'bold'),
                  width=15, height=2).pack(side=tk.LEFT, padx=10)

        # Подсказка
        hint_frame = tk.Frame(win, bg='lightyellow', height=35)
        hint_frame.grid(row=1, column=0, sticky="ew")
        hint_frame.grid_propagate(False)

        tk.Label(hint_frame,
                 text="💡 Формат: текст вопроса | вариант1 | вариант2 | вариант3 | вариант4 | номер_правильного(1-4)",
                 font=('Arial', 9), bg='lightyellow', fg='brown'
                 ).pack(expand=True)

        def load_data():
            cat_name = combo.get()
            if not cat_name:
                messagebox.showerror("Ошибка", "Выберите тему!")
                return

            cat = self.app.data_manager.get_category(cat_name)
            if cat:
                name_entry.delete(0, tk.END)
                name_entry.insert(0, cat.name)
                text_area.delete("1.0", tk.END)
                for q in cat.questions:
                    line = f"{q.text}|{q.options[0]}|{q.options[1]}|{q.options[2]}|{q.options[3]}|{q.correct_index}\n"
                    text_area.insert(tk.END, line)
            else:
                messagebox.showerror("Ошибка", "Не удалось загрузить тему!")

        def save():
            new_name = name_entry.get().strip()
            old_name = combo.get()

            if not new_name:
                messagebox.showerror("Ошибка", "Введите название темы!")
                return

            if not old_name:
                messagebox.showerror("Ошибка", "Сначала выберите тему для редактирования!")
                return

            if new_name != old_name and new_name in [c.name for c in self.app.data_manager.categories]:
                messagebox.showerror("Ошибка", "Тема с таким названием уже существует!")
                return

            questions = []
            errors = []

            for line_num, line in enumerate(text_area.get("1.0", tk.END).strip().split('\n'), 1):
                line = line.strip()
                if not line:
                    continue

                if '|' not in line:
                    errors.append(f"Строка {line_num}: отсутствуют разделители '|'")
                    continue

                parts = [p.strip() for p in line.split('|')]
                if len(parts) != 6:
                    errors.append(f"Строка {line_num}: должно быть 6 частей, найдено {len(parts)}")
                    continue

                try:
                    text = parts[0]
                    options = parts[1:5]
                    correct = int(parts[5])

                    if not text:
                        errors.append(f"Строка {line_num}: текст вопроса пуст")
                        continue

                    if any(not opt for opt in options):
                        errors.append(f"Строка {line_num}: некоторые варианты ответа пусты")
                        continue

                    if correct < 0 or correct > 3:
                        errors.append(f"Строка {line_num}: индекс правильного ответа должен быть от 0 до 3")
                        continue

                    questions.append(Question(text, options, correct, new_name))

                except ValueError:
                    errors.append(f"Строка {line_num}: индекс правильного ответа должен быть числом")
                except Exception as e:
                    errors.append(f"Строка {line_num}: ошибка формата - {str(e)}")

            if errors:
                error_msg = "Ошибки в вопросах:\n" + "\n".join(errors[:10])
                if len(errors) > 10:
                    error_msg += f"\n... и еще {len(errors) - 10} ошибок"
                messagebox.showerror("Ошибка валидации", error_msg)
                return

            if len(questions) < 3:
                messagebox.showerror("Ошибка", f"Добавьте минимум 3 вопроса! (сейчас {len(questions)})")
                return

            # Удаляем старую тему и добавляем новую
            self.app.data_manager.remove_category(old_name)
            self.app.data_manager.add_category(Category(new_name, questions))

            messagebox.showinfo("Успех", f"Тема '{new_name}' успешно обновлена!\nВопросов: {len(questions)}")
            win.destroy()

    def delete_category_window(self):
        if not self.app.data_manager.categories:
            messagebox.showinfo("Инфо", "Нет тем")
            return

        win = tk.Toplevel(self.app.root)
        win.title("Удалить тему")
        win.geometry("400x250")
        win.resizable(False, False)

        container = tk.Frame(win)
        container.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        tk.Label(container, text="Выберите тему для удаления:", font=('Arial', 14)).pack(pady=20)
        combo = ttk.Combobox(container,
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

        tk.Button(container, text="УДАЛИТЬ", command=delete, bg='red',
                  fg='white', font=('Arial', 14, 'bold')).pack(pady=20)

    def show_results(self):
        self.app.create_frame()

        container = tk.Frame(self.app.frame, bg='lightblue')
        container.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        title = tk.Label(container, text="РЕЗУЛЬТАТЫ",
                         font=('Arial', 22, 'bold'), bg='lightblue')
        title.pack(pady=30)

        if not self.app.data_manager.results:
            tk.Label(container, text="Нет результатов",
                     font=('Arial', 18), fg='gray', bg='lightblue').pack(expand=True)
        else:
            tree_frame = tk.Frame(container)
            tree_frame.pack(fill=tk.BOTH, expand=True)

            scrollbar = ttk.Scrollbar(tree_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            cols = ('Время', 'Пользователь', 'Очки', '%')
            tree = ttk.Treeview(tree_frame, columns=cols, show='headings',
                                yscrollcommand=scrollbar.set, height=15)
            scrollbar.config(command=tree.yview)

            for col in cols:
                tree.heading(col, text=col)
                tree.column(col, width=120, anchor='center')
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
                  command=self.show_menu, font=('Arial', 14)).pack(pady=20)