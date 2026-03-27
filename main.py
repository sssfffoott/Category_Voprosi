import tkinter as tk
from tkinter import messagebox
from data_manager import DataManager
from models import Question, Category
from admin import AdminPanel
from test_mode import TestMode


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ОПРОСНИК v1.2")
        self.root.geometry("950x750")
        self.root.resizable(True, True)

        self.data_manager = DataManager()
        self.init_sample_data()
        self.current_user = None
        self.admin_panel = AdminPanel(self)
        self.test_mode = TestMode(self)

        self.admin_credentials = {"admin": "123"}

        self.show_login()

    def init_sample_data(self):
        if not self.data_manager.categories:
            python_questions = [
                Question("Что такое список?", ["Массив", "Словарь", "Последовательность", "Функция"], 2, "Python"),
                Question("Неизменяемый тип?", ["list", "dict", "tuple", "set"], 2, "Python"),
                Question("len() возвращает?", ["Длину", "Минимум", "Максимум", "Сумму"], 0, "Python"),
                Question("Оператор 'или'?", ["and", "or", "not", "is"], 1, "Python"),
                Question("Что такое lambda?", ["Цикл", "Анонимная функция", "Класс", "Импорт"], 1, "Python"),
                Question("Индексация с?", ["1", "0", "-1", "None"], 1, "Python"),
                Question("def используется для?", ["Переменная", "Функция", "Класс", "Импорт"], 1, "Python"),
                Question("append() делает?", ["Удаляет", "Добавляет в конец", "Вставляет", "Сортирует"], 1, "Python"),
                Question("True == 1?", ["False", "True", "Error", "None"], 1, "Python"),
                Question("Срезы включают?", ["Конец", "Начало", "Оба", "Ни один"], 0, "Python")
            ]

            algo_questions = [
                                 Question("Бинарный поиск O(?)", ["O(n)", "O(log n)", "O(n^2)", "O(1)"], 1,
                                          "Алгоритмы"),
                                 Question("Big O это?", ["Время", "Память", "Худший случай", "Лучший"], 2, "Алгоритмы"),
                                 Question("Пузырёк O(?)", ["n log n", "n^2", "n", "log n"], 1, "Алгоритмы"),
                                 Question("Root в дереве?", ["Лист", "Корень", "Вершина", "Узел"], 1, "Алгоритмы"),
                                 Question("DFS это?", ["Ширина", "Глубина", "Оба", "Нет"], 1, "Алгоритмы")
                             ] * 2

            db_questions = [
                               Question("PRIMARY KEY?", ["Дубликаты", "Уникальный", "NULL", "Внешний"], 1, "БД"),
                               Question("JOIN типы?", ["INNER", "LEFT", "RIGHT", "Все"], 3, "БД"),
                               Question("INDEX ускоряет?", ["Вставку", "Выборку", "Удаление", "Все"], 1, "БД")
                           ] * 4

            self.data_manager.categories = [
                Category("Python", python_questions),
                Category("Алгоритмы", algo_questions),
                Category("Базы данных", db_questions)
            ]
            self.data_manager.save_data()

    def create_frame(self):
        if hasattr(self, 'frame') and self.frame:
            self.frame.destroy()
        self.frame = tk.Frame(self.root, bg='lightblue')
        self.frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

    def clear_frame(self):
        if hasattr(self, 'frame') and self.frame:
            self.frame.destroy()
            self.frame = None

    def show_login(self):
        self.create_frame()

        # Создаем контейнер для центрирования
        container = tk.Frame(self.frame, bg='lightblue')
        container.pack(expand=True)

        title = tk.Label(container, text="СИСТЕМА ТЕСТИРОВАНИЯ",
                         font=('Arial', 28, 'bold'), bg='lightblue')
        title.pack(pady=50)

        tk.Label(container, text="Выберите роль:", font=('Arial', 18), bg='lightblue').pack(pady=20)

        self.role_var = tk.StringVar(value="test")
        role_frame = tk.Frame(container, bg='lightblue')
        role_frame.pack(pady=20)

        tk.Radiobutton(role_frame, text="Тестируемый", variable=self.role_var,
                       value="test", font=('Arial', 16), bg='lightblue').pack(side=tk.LEFT, padx=40)
        tk.Radiobutton(role_frame, text="Администратор", variable=self.role_var,
                       value="admin", font=('Arial', 16), bg='lightblue').pack(side=tk.LEFT, padx=40)

        btn_frame = tk.Frame(container, bg='lightblue')
        btn_frame.pack(pady=50)
        tk.Button(btn_frame, text="ВОЙТИ", command=self.login, bg='green',
                  fg='white', font=('Arial', 18, 'bold'), width=18, height=2
                  ).pack(side=tk.LEFT, padx=20)
        tk.Button(btn_frame, text="ВЫХОД", command=self.root.quit, bg='red',
                  fg='white', font=('Arial', 18, 'bold'), width=18, height=2
                  ).pack(side=tk.LEFT, padx=20)

    def show_admin_login(self):
        login_win = tk.Toplevel(self.root)
        login_win.title("Вход администратора")
        login_win.geometry("400x350")
        login_win.resizable(False, False)
        login_win.grab_set()
        login_win.transient(self.root)

        # Контейнер для центрирования
        container = tk.Frame(login_win)
        container.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        tk.Label(container, text="АВТОРИЗАЦИЯ АДМИНИСТРАТОРА",
                 font=('Arial', 14, 'bold'), fg='darkblue').pack(pady=20)

        tk.Label(container, text="Логин:", font=('Arial', 12)).pack(pady=(20, 5))
        login_entry = tk.Entry(container, font=('Arial', 12), width=30)
        login_entry.pack(pady=5)
        login_entry.focus()

        tk.Label(container, text="Пароль:", font=('Arial', 12)).pack(pady=(10, 5))
        password_entry = tk.Entry(container, font=('Arial', 12), width=30, show="*")
        password_entry.pack(pady=5)

        def on_enter(event):
            check_login()

        login_entry.bind('<Return>', on_enter)
        password_entry.bind('<Return>', on_enter)

        def check_login():
            login = login_entry.get().strip()
            password = password_entry.get().strip()

            if not login or not password:
                messagebox.showerror("Ошибка", "Введите логин и пароль!")
                return

            if login in self.admin_credentials and self.admin_credentials[login] == password:
                login_win.destroy()
                self.admin_panel.show_menu()
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль!")
                login_entry.delete(0, tk.END)
                password_entry.delete(0, tk.END)
                login_entry.focus()

        btn_frame = tk.Frame(container)
        btn_frame.pack(pady=30)

        tk.Button(btn_frame, text="ВОЙТИ", command=check_login,
                  bg='green', fg='white', font=('Arial', 12, 'bold'),
                  width=12, height=1).pack(side=tk.LEFT, padx=10)

        tk.Button(btn_frame, text="ОТМЕНА", command=login_win.destroy,
                  bg='red', fg='white', font=('Arial', 12, 'bold'),
                  width=12, height=1).pack(side=tk.LEFT, padx=10)

        tk.Label(container, text="По умолчанию: admin / admin123",
                 font=('Arial', 9), fg='gray').pack(pady=15)

    def login(self):
        self.current_user = self.role_var.get()
        if self.current_user == 'test':
            self.test_mode.show_menu()
        else:
            self.show_admin_login()


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()