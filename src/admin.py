# admin.py
import tkinter as tk
from tkinter import messagebox, ttk
from models import Question, Category


class AdminPanel:
    def __init__(self, app):
        self.app = app

    def show_menu(self):
        self.app.create_frame()
        
        top_bar = tk.Frame(self.app.frame, bg=self.app.colors['dark'], height=55)
        top_bar.pack(fill=tk.X, side=tk.TOP)
        top_bar.pack_propagate(False)
        
        back_btn = tk.Button(top_bar, text="[ ГЛАВНОЕ МЕНЮ ]", command=self.app.show_role_selection,
                             bg=self.app.colors['dark'], fg=self.app.colors['primary'],
                             font=self.app.fonts['button'], relief=tk.FLAT, bd=0,
                             activebackground=self.app.colors['dark'], activeforeground=self.app.colors['primary'])
        back_btn.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Центрируем карточку
        center_frame = tk.Frame(self.app.frame, bg=self.app.colors['bg'])
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        card = self.app.create_card(center_frame)
        card.pack(pady=20, padx=40, ipadx=50, ipady=35)
        
        tk.Label(card, text="[ ПАНЕЛЬ АДМИНИСТРАТОРА ]", font=self.app.fonts['subtitle'],
                 fg=self.app.colors['primary'], bg=self.app.colors['card_bg']).pack(pady=(0, 25))
        
        btn_add = tk.Button(card, text="> ДОБАВИТЬ ТЕМУ <", command=self.add_category,
                            bg=self.app.colors['success'], fg='#000000',
                            font=self.app.fonts['button'], width=25, height=2,
                            relief=tk.FLAT, bd=0,
                            activebackground=self.app.colors['success'], activeforeground='#000000')
        btn_add.pack(pady=6)
        
        btn_edit = tk.Button(card, text="> РЕДАКТИРОВАТЬ ТЕМУ <", command=self.edit_category,
                             bg=self.app.colors['warning'], fg='#000000',
                             font=self.app.fonts['button'], width=25, height=2,
                             relief=tk.FLAT, bd=0,
                             activebackground=self.app.colors['warning'], activeforeground='#000000')
        btn_edit.pack(pady=6)
        
        btn_delete = tk.Button(card, text="> УДАЛИТЬ ТЕМУ <", command=self.delete_category,
                               bg=self.app.colors['danger'], fg='#000000',
                               font=self.app.fonts['button'], width=25, height=2,
                               relief=tk.FLAT, bd=0,
                               activebackground=self.app.colors['danger'], activeforeground='#000000')
        btn_delete.pack(pady=6)
        
        btn_results = tk.Button(card, text="> ВСЕ РЕЗУЛЬТАТЫ <", command=self.show_all_results,
                                bg=self.app.colors['secondary'], fg='#000000',
                                font=self.app.fonts['button'], width=25, height=2,
                                relief=tk.FLAT, bd=0,
                                activebackground=self.app.colors['secondary'], activeforeground='#000000')
        btn_results.pack(pady=6)
        
        btn_reset = tk.Button(card, text="> СБРОСИТЬ ТЕМЫ <", command=self.reset_categories,
                              bg=self.app.colors['primary'], fg='#000000',
                              font=self.app.fonts['button'], width=25, height=2,
                              relief=tk.FLAT, bd=0,
                              activebackground=self.app.colors['primary'], activeforeground='#000000')
        btn_reset.pack(pady=6)
        
        for btn in [btn_add, btn_edit, btn_delete, btn_results, btn_reset]:
            original_bg = btn.cget('bg')
            btn.bind("<Enter>", lambda e, b=btn, bg=original_bg: b.configure(bg=self.app.colors['primary'], fg='#000000'))
            btn.bind("<Leave>", lambda e, b=btn, bg=original_bg: b.configure(bg=bg, fg='#000000'))

    def reset_categories(self):
        if messagebox.askyesno("ПОДТВЕРЖДЕНИЕ", "Восстановить стандартные темы (Python, Алгоритмы, Базы данных)?"):
            self.app.data_manager.reset_to_sample_data()
            messagebox.showinfo("УСПЕХ", "Темы восстановлены!")
            self.show_menu()

    def add_category(self):
        self.app.create_frame()
        
        top_bar = tk.Frame(self.app.frame, bg=self.app.colors['dark'], height=55)
        top_bar.pack(fill=tk.X, side=tk.TOP)
        top_bar.pack_propagate(False)
        back_btn = tk.Button(top_bar, text="[ НАЗАД ]", command=self.show_menu,
                             bg=self.app.colors['dark'], fg=self.app.colors['primary'],
                             font=self.app.fonts['button'], relief=tk.FLAT, bd=0,
                             activebackground=self.app.colors['dark'], activeforeground=self.app.colors['primary'])
        back_btn.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Центрируем карточку
        center_frame = tk.Frame(self.app.frame, bg=self.app.colors['bg'])
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        card = self.app.create_card(center_frame)
        card.pack(pady=20, padx=40, ipadx=30, ipady=20)
        
        tk.Label(card, text="[ ДОБАВЛЕНИЕ ТЕМЫ ]", font=self.app.fonts['subtitle'],
                 fg=self.app.colors['primary'], bg=self.app.colors['card_bg']).pack(pady=(0, 15))
        
        tk.Label(card, text="НАЗВАНИЕ ТЕМЫ:", font=self.app.fonts['body'],
                 fg=self.app.colors['text_muted'], bg=self.app.colors['card_bg']).pack(anchor='w')
        name_entry = tk.Entry(card, font=self.app.fonts['body'], width=50,
                              bg=self.app.colors['dark'], fg=self.app.colors['primary'],
                              insertbackground=self.app.colors['primary'],
                              relief=tk.GROOVE, bd=2)
        name_entry.pack(pady=5, ipady=6, fill=tk.X)
        
        tk.Label(card, text="ВОПРОСЫ (КАЖДЫЙ ВОПРОС С НОВОЙ СТРОКИ):", font=self.app.fonts['body'],
                 fg=self.app.colors['text_muted'], bg=self.app.colors['card_bg']).pack(anchor='w', pady=(15, 0))
        format_label = tk.Label(card, text="ФОРМАТ: вопрос | вариант1 | вариант2 | вариант3 | вариант4 | номер(0-3)",
                                font=self.app.fonts['small'], fg=self.app.colors['secondary'],
                                bg=self.app.colors['card_bg'])
        format_label.pack(anchor='w', pady=(0, 5))
        
        # Текстовое поле с внутренней прокруткой
        text_frame = tk.Frame(card, bg=self.app.colors['card_bg'])
        text_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        text_scroll = ttk.Scrollbar(text_frame)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        text_area = tk.Text(text_frame, font=self.app.fonts['body'],
                            yscrollcommand=text_scroll.set,
                            bg=self.app.colors['dark'], fg=self.app.colors['text'],
                            insertbackground=self.app.colors['primary'],
                            relief=tk.FLAT, bd=0, padx=10, pady=10, height=12)
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_scroll.config(command=text_area.yview)
        
        def save():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("ОШИБКА", "Введите название темы!")
                return
            if name in [c.name for c in self.app.data_manager.categories]:
                messagebox.showerror("ОШИБКА", "Такая тема уже существует!")
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
                messagebox.showerror("ОШИБКА", "Добавьте минимум 3 вопроса!")
                return
            self.app.data_manager.add_category(Category(name, questions))
            messagebox.showinfo("УСПЕХ", f"Тема '{name}' добавлена! ({len(questions)} вопросов)")
            self.show_menu()
        
        btn_frame = tk.Frame(card, bg=self.app.colors['card_bg'])
        btn_frame.pack(pady=15)
        save_btn = tk.Button(btn_frame, text="[ СОХРАНИТЬ ]", command=save,
                             bg=self.app.colors['success'], fg='#000000', font=self.app.fonts['button'],
                             width=15, height=1, relief=tk.FLAT, bd=0,
                             activebackground=self.app.colors['success'], activeforeground='#000000')
        save_btn.pack()
        save_btn.bind("<Enter>", lambda e: save_btn.configure(bg=self.app.colors['primary']))
        save_btn.bind("<Leave>", lambda e: save_btn.configure(bg=self.app.colors['success']))

    def edit_category(self):
        if not self.app.data_manager.categories:
            messagebox.showinfo("ИНФОРМАЦИЯ", "Нет тем для редактирования")
            return
        self.app.create_frame()
        
        top_bar = tk.Frame(self.app.frame, bg=self.app.colors['dark'], height=55)
        top_bar.pack(fill=tk.X, side=tk.TOP)
        top_bar.pack_propagate(False)
        back_btn = tk.Button(top_bar, text="[ НАЗАД ]", command=self.show_menu,
                             bg=self.app.colors['dark'], fg=self.app.colors['primary'],
                             font=self.app.fonts['button'], relief=tk.FLAT, bd=0,
                             activebackground=self.app.colors['dark'], activeforeground=self.app.colors['primary'])
        back_btn.pack(side=tk.LEFT, padx=20, pady=15)
        
        center_frame = tk.Frame(self.app.frame, bg=self.app.colors['bg'])
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        card = self.app.create_card(center_frame)
        card.pack(pady=20, padx=40, ipadx=30, ipady=20)
        
        tk.Label(card, text="[ РЕДАКТИРОВАНИЕ ТЕМЫ ]", font=self.app.fonts['subtitle'],
                 fg=self.app.colors['primary'], bg=self.app.colors['card_bg']).pack(pady=(0, 15))
        
        tk.Label(card, text="ВЫБЕРИТЕ ТЕМУ:", font=self.app.fonts['body'],
                 fg=self.app.colors['text_muted'], bg=self.app.colors['card_bg']).pack(anchor='w')
        combo = ttk.Combobox(card, values=[c.name for c in self.app.data_manager.categories],
                              font=self.app.fonts['body'], width=45, state='readonly')
        combo.pack(pady=5, ipady=5, fill=tk.X)
        load_btn = tk.Button(card, text="[ ЗАГРУЗИТЬ ]", command=lambda: load_data(),
                             bg=self.app.colors['primary'], fg='#000000', font=self.app.fonts['button'],
                             width=15, height=1, relief=tk.FLAT, bd=0,
                             activebackground=self.app.colors['primary'], activeforeground='#000000')
        load_btn.pack(pady=10)
        
        tk.Label(card, text="НАЗВАНИЕ ТЕМЫ:", font=self.app.fonts['body'],
                 fg=self.app.colors['text_muted'], bg=self.app.colors['card_bg']).pack(anchor='w', pady=(15, 0))
        name_entry = tk.Entry(card, font=self.app.fonts['body'], width=50,
                              bg=self.app.colors['dark'], fg=self.app.colors['primary'],
                              insertbackground=self.app.colors['primary'],
                              relief=tk.GROOVE, bd=2)
        name_entry.pack(pady=5, ipady=6, fill=tk.X)
        
        tk.Label(card, text="ВОПРОСЫ:", font=self.app.fonts['body'],
                 fg=self.app.colors['text_muted'], bg=self.app.colors['card_bg']).pack(anchor='w', pady=(15, 0))
        text_frame = tk.Frame(card, bg=self.app.colors['card_bg'])
        text_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        text_scroll = ttk.Scrollbar(text_frame)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        text_area = tk.Text(text_frame, font=self.app.fonts['body'],
                            yscrollcommand=text_scroll.set,
                            bg=self.app.colors['dark'], fg=self.app.colors['text'],
                            insertbackground=self.app.colors['primary'],
                            relief=tk.FLAT, bd=0, padx=10, pady=10, height=12)
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_scroll.config(command=text_area.yview)
        
        def load_data():
            cat_name = combo.get()
            if not cat_name:
                messagebox.showerror("ОШИБКА", "Выберите тему!")
                return
            cat = self.app.data_manager.get_category(cat_name)
            if cat:
                name_entry.delete(0, tk.END)
                name_entry.insert(0, cat.name)
                text_area.delete("1.0", tk.END)
                for q in cat.questions:
                    line = f"{q.text}|{q.options[0]}|{q.options[1]}|{q.options[2]}|{q.options[3]}|{q.correct_index}\n"
                    text_area.insert(tk.END, line)
        
        def save():
            new_name = name_entry.get().strip()
            old_name = combo.get()
            if not new_name:
                messagebox.showerror("ОШИБКА", "Введите название темы!")
                return
            if not old_name:
                messagebox.showerror("ОШИБКА", "Сначала загрузите тему!")
                return
            if new_name != old_name and new_name in [c.name for c in self.app.data_manager.categories]:
                messagebox.showerror("ОШИБКА", "Тема с таким названием уже существует!")
                return
            questions = []
            for line in text_area.get("1.0", tk.END).strip().split('\n'):
                if not line or '|' not in line:
                    continue
                parts = [p.strip() for p in line.split('|')]
                if len(parts) == 6:
                    try:
                        q = Question(parts[0], parts[1:5], int(parts[5]), new_name)
                        questions.append(q)
                    except:
                        continue
            if len(questions) < 3:
                messagebox.showerror("ОШИБКА", "Добавьте минимум 3 вопроса!")
                return
            self.app.data_manager.remove_category(old_name)
            self.app.data_manager.add_category(Category(new_name, questions))
            messagebox.showinfo("УСПЕХ", f"Тема '{new_name}' обновлена!")
            self.show_menu()
        
        btn_frame = tk.Frame(card, bg=self.app.colors['card_bg'])
        btn_frame.pack(pady=15)
        save_btn = tk.Button(btn_frame, text="[ СОХРАНИТЬ ]", command=save,
                             bg=self.app.colors['success'], fg='#000000', font=self.app.fonts['button'],
                             width=15, height=1, relief=tk.FLAT, bd=0,
                             activebackground=self.app.colors['success'], activeforeground='#000000')
        save_btn.pack()

    def delete_category(self):
        if not self.app.data_manager.categories:
            messagebox.showinfo("ИНФОРМАЦИЯ", "Нет тем для удаления")
            return
        self.app.create_frame()
        
        top_bar = tk.Frame(self.app.frame, bg=self.app.colors['dark'], height=55)
        top_bar.pack(fill=tk.X, side=tk.TOP)
        top_bar.pack_propagate(False)
        back_btn = tk.Button(top_bar, text="[ НАЗАД ]", command=self.show_menu,
                             bg=self.app.colors['dark'], fg=self.app.colors['primary'],
                             font=self.app.fonts['button'], relief=tk.FLAT, bd=0,
                             activebackground=self.app.colors['dark'], activeforeground=self.app.colors['primary'])
        back_btn.pack(side=tk.LEFT, padx=20, pady=15)
        
        center_frame = tk.Frame(self.app.frame, bg=self.app.colors['bg'])
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        card = self.app.create_card(center_frame)
        card.pack(pady=20, padx=40, ipadx=50, ipady=40)
        
        tk.Label(card, text="[ УДАЛЕНИЕ ТЕМЫ ]", font=self.app.fonts['subtitle'],
                 fg=self.app.colors['primary'], bg=self.app.colors['card_bg']).pack(pady=(0, 25))
        
        tk.Label(card, text="ВЫБЕРИТЕ ТЕМУ ДЛЯ УДАЛЕНИЯ:", font=self.app.fonts['body'],
                 fg=self.app.colors['text_muted'], bg=self.app.colors['card_bg']).pack()
        combo = ttk.Combobox(card, values=[c.name for c in self.app.data_manager.categories],
                              font=self.app.fonts['body'], width=35, state='readonly')
        combo.pack(pady=15, ipady=5)
        
        def delete():
            name = combo.get()
            if not name:
                messagebox.showerror("ОШИБКА", "Выберите тему!")
                return
            if messagebox.askyesno("ПОДТВЕРЖДЕНИЕ", f"Удалить тему '{name}'?"):
                self.app.data_manager.remove_category(name)
                messagebox.showinfo("УСПЕХ", f"Тема '{name}' удалена!")
                self.show_menu()
        
        delete_btn = tk.Button(card, text="[ УДАЛИТЬ ]", command=delete,
                               bg=self.app.colors['danger'], fg='#000000', font=self.app.fonts['button'],
                               width=20, height=1, relief=tk.FLAT, bd=0,
                               activebackground=self.app.colors['danger'], activeforeground='#000000')
        delete_btn.pack(pady=10)

    def show_all_results(self):
        self.app.create_frame()
        
        top_bar = tk.Frame(self.app.frame, bg=self.app.colors['dark'], height=55)
        top_bar.pack(fill=tk.X, side=tk.TOP)
        top_bar.pack_propagate(False)
        back_btn = tk.Button(top_bar, text="[ НАЗАД ]", command=self.show_menu,
                             bg=self.app.colors['dark'], fg=self.app.colors['primary'],
                             font=self.app.fonts['button'], relief=tk.FLAT, bd=0,
                             activebackground=self.app.colors['dark'], activeforeground=self.app.colors['primary'])
        back_btn.pack(side=tk.LEFT, padx=20, pady=15)
        
        center_frame = tk.Frame(self.app.frame, bg=self.app.colors['bg'])
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        card = self.app.create_card(center_frame)
        card.pack(pady=20, padx=40, ipadx=30, ipady=20)
        
        tk.Label(card, text="[ ВСЕ РЕЗУЛЬТАТЫ ]", font=self.app.fonts['subtitle'],
                 fg=self.app.colors['primary'], bg=self.app.colors['card_bg']).pack(pady=(0, 15))
        
        all_results = self.app.data_manager.get_all_results()
        if not all_results:
            tk.Label(card, text="НЕТ РЕЗУЛЬТАТОВ", font=self.app.fonts['body'],
                     fg=self.app.colors['text_muted'], bg=self.app.colors['card_bg']).pack(expand=True)
        else:
            tree_frame = tk.Frame(card, bg=self.app.colors['card_bg'])
            tree_frame.pack(fill=tk.BOTH, expand=True)
            scroll_y = ttk.Scrollbar(tree_frame)
            scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
            scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
            scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
            cols = ('ДАТА', 'ПОЛЬЗОВАТЕЛЬ', 'ТЕМА', 'РЕЗУЛЬТАТ', '%')
            tree = ttk.Treeview(tree_frame, columns=cols, show='headings',
                                yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, height=15)
            scroll_y.config(command=tree.yview)
            scroll_x.config(command=tree.xview)
            style = ttk.Style()
            style.configure("Treeview", background=self.app.colors['dark'], foreground=self.app.colors['primary'],
                            fieldbackground=self.app.colors['dark'])
            style.configure("Treeview.Heading", background=self.app.colors['secondary'],
                            foreground='#000000', font=self.app.fonts['button'])
            for col, width in zip(cols, [140, 120, 150, 80, 70]):
                tree.heading(col, text=col)
                tree.column(col, width=width, anchor='center')
            tree.pack(fill=tk.BOTH, expand=True)
            for result in all_results[:50]:
                tree.insert('', 'end', values=(result['time'], result['username'], result['category'],
                                               f"{result['score']}/{result['total']}", f"{result['percent']}%"))
        
        btn_frame = tk.Frame(card, bg=self.app.colors['card_bg'])
        btn_frame.pack(pady=15)
        clear_btn = tk.Button(btn_frame, text="[ ОЧИСТИТЬ ВСЕ РЕЗУЛЬТАТЫ ]", command=self.clear_all_results,
                              bg=self.app.colors['danger'], fg='#000000', font=self.app.fonts['button'],
                              width=25, height=1, relief=tk.FLAT, bd=0,
                              activebackground=self.app.colors['danger'], activeforeground='#000000')
        clear_btn.pack()

    def clear_all_results(self):
        if messagebox.askyesno("ПОДТВЕРЖДЕНИЕ", "Удалить все результаты всех пользователей?"):
            for user in self.app.data_manager.users:
                user.results = []
            self.app.data_manager.save_users()
            messagebox.showinfo("УСПЕХ", "Все результаты очищены!")
            self.show_all_results()