import tkinter as tk
from tkinter import ttk, messagebox


class TestMode:
    def __init__(self, app):
        self.app = app

    def show_menu(self):
        self.app.create_frame()
        title = tk.Label(self.app.frame, text="ТЕСТИРУЕМЫЙ",
                         font=('Arial', 24, 'bold'), bg='lightblue')
        title.pack(pady=40)

        if not self.app.data_manager.categories:
            tk.Label(self.app.frame, text="Нет доступных тем!",
                     font=('Arial', 18), fg='red').pack(pady=30)
            tk.Button(self.app.frame, text="Главное меню",
                      command=self.app.show_login, font=('Arial', 14)).pack(pady=20)
            return

        tk.Label(self.app.frame, text="Выберите тему:", font=('Arial', 16)).pack(pady=20)

        self.cat_combo = ttk.Combobox(self.app.frame, values=[c.name for c in self.app.data_manager.categories],
                                      font=('Arial', 14), width=35, state='readonly')
        self.cat_combo.pack(pady=15)
        if self.app.data_manager.categories:
            self.cat_combo.set(self.app.data_manager.categories[0].name)

        tk.Button(self.app.frame, text="НАЧАТЬ ТЕСТ",
                  command=self.start_quiz, bg='orange', font=('Arial', 18, 'bold'),
                  width=25, height=2).pack(pady=40)

        tk.Button(self.app.frame, text="Главное меню",
                  command=self.app.show_login, font=('Arial', 14)).pack(pady=10)

    def start_quiz(self):
        selected = self.cat_combo.get()
        category = self.app.data_manager.get_category(selected)
        if not category:
            messagebox.showerror("Ошибка", "Выберите тему!")
            return

        from quiz import Quiz
        quiz_win = tk.Toplevel(self.app.root)
        quiz_win.transient(self.app.root)
        quiz_win.grab_set()
        quiz = Quiz(quiz_win, self.app, category.questions, self.app.current_user, self.app.data_manager)
        quiz.start()

        def on_quiz_close():
            quiz_win.grab_release()
            self.show_menu()

        quiz_win.protocol("WM_DELETE_WINDOW", on_quiz_close)
