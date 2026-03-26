import tkinter as tk
from data_manager import DataManager
from models import Question, Category
from admin import AdminPanel
from test_mode import TestMode


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("СИСТЕМА ТЕСТИРОВАНИЯ v2.0")
        self.root.geometry("950x750")
        self.root.resizable(True, True)

        self.data_manager = DataManager()
        self.init_sample_data()
        self.current_user = None
        self.admin_panel = AdminPanel(self)
        self.test_mode = TestMode(self)
        
        # Настройка сетки для масштабирования основного окна
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.show_login()

    def init_sample_data(self):
        """Инициализация тестовых данных, если их нет"""
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
                Question("Бинарный поиск O(?)", ["O(n)", "O(log n)", "O(n^2)", "O(1)"], 1, "Алгоритмы"),
                Question("Big O это?", ["Время", "Память", "Худший случай", "Лучший"], 2, "Алгоритмы"),
                Question("Пузырёк O(?)", ["n log n", "n^2", "n", "log n"], 1, "Алгоритмы"),
                Question("Root в дереве?", ["Лист", "Корень", "Вершина", "Узел"], 1, "Алгоритмы"),
                Question("DFS это?", ["Ширина", "Глубина", "Оба", "Нет"], 1, "Алгоритмы")
            ] * 2  # Умножаем для увеличения количества вопросов

            db_questions = [
                Question("PRIMARY KEY?", ["Дубликаты", "Уникальный", "NULL", "Внешний"], 1, "БД"),
                Question("JOIN типы?", ["INNER", "LEFT", "RIGHT", "Все"], 3, "БД"),
                Question("INDEX ускоряет?", ["Вставку", "Выборку", "Удаление", "Все"], 1, "БД")
            ] * 4  # Умножаем для увеличения количества вопросов

            self.data_manager.categories = [
                Category("Python", python_questions),
                Category("Алгоритмы", algo_questions),
                Category("Базы данных", db_questions)
            ]
            self.data_manager.save_data()

    def create_frame(self):
        """Создание основного фрейма с настройками масштабирования"""
        # Удаляем существующий фрейм, если он есть
        if hasattr(self, 'frame') and self.frame:
            self.frame.destroy()
        
        # Создаем новый фрейм с привязкой к сетке
        self.frame = tk.Frame(self.root, bg='lightblue')
        self.frame.grid(row=0, column=0, sticky="nsew")
        
        # Настройка сетки для внутреннего фрейма
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

    def clear_frame(self):
        """Очистка фрейма"""
        if hasattr(self, 'frame') and self.frame:
            self.frame.destroy()
            self.frame = None

    def show_login(self):
        """Отображение экрана входа/выбора роли"""
        self.create_frame()
        
        # Создаем контейнер для центрирования содержимого
        container = tk.Frame(self.frame, bg='lightblue')
        container.grid(row=0, column=0, sticky="nsew")
        
        # Настройка весов для центрирования
        container.grid_rowconfigure(0, weight=1)  # Верхний отступ
        container.grid_rowconfigure(1, weight=0)  # Заголовок
        container.grid_rowconfigure(2, weight=0)  # Текст выбора
        container.grid_rowconfigure(3, weight=0)  # Радиокнопки
        container.grid_rowconfigure(4, weight=0)  # Кнопки
        container.grid_rowconfigure(5, weight=1)  # Нижний отступ
        container.grid_columnconfigure(0, weight=1)
        
        # Заголовок
        title = tk.Label(container, text="СИСТЕМА ТЕСТИРОВАНИЯ",
                         font=('Arial', 28, 'bold'), bg='lightblue')
        title.grid(row=1, column=0, pady=30)
        
        # Текст выбора роли
        tk.Label(container, text="Выберите роль:", 
                 font=('Arial', 18), bg='lightblue').grid(row=2, column=0, pady=20)
        
        # Радиокнопки для выбора роли
        self.role_var = tk.StringVar(value="test")
        role_frame = tk.Frame(container, bg='lightblue')
        role_frame.grid(row=3, column=0, pady=10)
        
        tk.Radiobutton(role_frame, text="Тестируемый", variable=self.role_var,
                       value="test", font=('Arial', 16), bg='lightblue',
                       activebackground='lightblue').pack(side=tk.LEFT, padx=40)
        tk.Radiobutton(role_frame, text="Администратор", variable=self.role_var,
                       value="admin", font=('Arial', 16), bg='lightblue',
                       activebackground='lightblue').pack(side=tk.LEFT, padx=40)
        
        # Кнопки входа и выхода
        btn_frame = tk.Frame(container, bg='lightblue')
        btn_frame.grid(row=4, column=0, pady=40)
        
        tk.Button(btn_frame, text="ВОЙТИ", command=self.login, bg='green',
                  fg='white', font=('Arial', 18, 'bold'), width=18, height=2,
                  activebackground='darkgreen', cursor='hand2'
                  ).pack(side=tk.LEFT, padx=20)
        
        tk.Button(btn_frame, text="ВЫХОД", command=self.root.quit, bg='red',
                  fg='white', font=('Arial', 18, 'bold'), width=18, height=2,
                  activebackground='darkred', cursor='hand2'
                  ).pack(side=tk.LEFT, padx=20)

    def login(self):
        """Обработка входа в систему"""
        self.current_user = self.role_var.get()
        if self.current_user == 'test':
            self.test_mode.show_menu()
        else:
            self.admin_panel.show_menu()


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()