# data_manager.py
import json
import os
from datetime import datetime
from models import Category, User


class DataManager:
    def __init__(self, users_filename='users.json'):
        self.users_filename = users_filename
        self.categories = []
        self.users = []
        self.current_user = None
        self.load_users()
        self.load_all_categories()

    def load_users(self):
        if os.path.exists(self.users_filename):
            try:
                with open(self.users_filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.users = [User.from_dict(u) for u in data.get('users', [])]
            except Exception as e:
                print(f"Ошибка загрузки пользователей: {e}")
                self.users = []
        else:
            self.users = []

    def save_users(self):
        data = {'users': [u.to_dict() for u in self.users]}
        try:
            with open(self.users_filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения пользователей: {e}")

    def load_all_categories(self):
        self.categories = []
        if not os.path.exists('categories'):
            os.makedirs('categories')
            self.init_sample_data()
        else:
            for filename in os.listdir('categories'):
                if filename.endswith('.json'):
                    try:
                        with open(os.path.join('categories', filename), 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            category = Category.from_dict(data)
                            self.categories.append(category)
                    except Exception as e:
                        print(f"Ошибка загрузки {filename}: {e}")

    def save_category(self, category):
        if not os.path.exists('categories'):
            os.makedirs('categories')
        safe_name = "".join(c for c in category.name if c.isalnum() or c in ' _-')
        filename = os.path.join('categories', f"{safe_name}.json")
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(category.to_dict(), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения категории: {e}")

    def delete_category_file(self, category_name):
        safe_name = "".join(c for c in category_name if c.isalnum() or c in ' _-')
        filename = os.path.join('categories', f"{safe_name}.json")
        if os.path.exists(filename):
            os.remove(filename)

    def init_sample_data(self):
        from models import Question
        
        # Python - 10 вопросов
        python_questions = [
            Question("Что такое список?", ["Массив", "Словарь", "Последовательность", "Функция"], 2, "Python"),
            Question("Неизменяемый тип?", ["list", "dict", "tuple", "set"], 2, "Python"),
            Question("len() возвращает?", ["Длину", "Минимум", "Максимум", "Сумму"], 0, "Python"),
            Question("Оператор 'или'?", ["and", "or", "not", "is"], 1, "Python"),
            Question("Что такое lambda?", ["Цикл", "Анонимная функция", "Класс", "Импорт"], 1, "Python"),
            Question("Индексация начинается с?", ["1", "0", "-1", "None"], 1, "Python"),
            Question("def используется для?", ["Переменная", "Функция", "Класс", "Импорт"], 1, "Python"),
            Question("append() делает?", ["Удаляет", "Добавляет в конец", "Вставляет", "Сортирует"], 1, "Python"),
            Question("True == 1?", ["False", "True", "Error", "None"], 1, "Python"),
            Question("Срезы включают?", ["Конец", "Начало", "Оба", "Ни один"], 1, "Python")
        ]
        
        # Алгоритмы - 10 вопросов
        algo_questions = [
            Question("Бинарный поиск O(?)", ["O(n)", "O(log n)", "O(n^2)", "O(1)"], 1, "Алгоритмы"),
            Question("Big O это?", ["Время", "Память", "Худший случай", "Лучший случай"], 2, "Алгоритмы"),
            Question("Пузырёк O(?)", ["n log n", "n^2", "n", "log n"], 1, "Алгоритмы"),
            Question("Root в дереве?", ["Лист", "Корень", "Вершина", "Узел"], 1, "Алгоритмы"),
            Question("DFS это?", ["Ширина", "Глубина", "Оба", "Нет"], 1, "Алгоритмы"),
            Question("BFS это?", ["Ширина", "Глубина", "Оба", "Нет"], 0, "Алгоритмы"),
            Question("Быстрая сортировка O(?)", ["n^2", "n log n", "n", "log n"], 1, "Алгоритмы"),
            Question("Стек работает по принципу?", ["FIFO", "LIFO", "FILO", "LILO"], 1, "Алгоритмы"),
            Question("Очередь работает по принципу?", ["FIFO", "LIFO", "FILO", "LILO"], 0, "Алгоритмы"),
            Question("Хеш-таблица это?", ["Массив", "Словарь", "Список", "Кортеж"], 1, "Алгоритмы")
        ]
        
        # Базы данных - 10 вопросов
        db_questions = [
            Question("PRIMARY KEY?", ["Дубликаты", "Уникальный", "NULL", "Внешний"], 1, "Базы данных"),
            Question("JOIN типы?", ["INNER", "LEFT", "RIGHT", "Все"], 3, "Базы данных"),
            Question("INDEX ускоряет?", ["Вставку", "Выборку", "Удаление", "Все"], 1, "Базы данных"),
            Question("SQL расшифровка?", ["Structured Query Language", "Simple Query Language", "Standard Query Language", "System Query Language"], 0, "Базы данных"),
            Question("DELETE vs TRUNCATE?", ["Можно отменить", "Быстрее", "Оба", "Ничего"], 0, "Базы данных"),
            Question("Что такое NULL?", ["Ноль", "Пусто", "Не определено", "Ошибка"], 2, "Базы данных"),
            Question("Нормализация это?", ["Удаление дубликатов", "Оптимизация", "Разделение таблиц", "Объединение"], 0, "Базы данных"),
            Question("ACID свойства?", ["Atomicity", "Consistency", "Isolation", "Все"], 3, "Базы данных"),
            Question("Что такое транзакция?", ["Запрос", "Группа операций", "Таблица", "Индекс"], 1, "Базы данных"),
            Question("VIEW это?", ["Таблица", "Виртуальная таблица", "Индекс", "Хранимая процедура"], 1, "Базы данных")
        ]
        
        self.add_category(Category("Python", python_questions))
        self.add_category(Category("Алгоритмы", algo_questions))
        self.add_category(Category("Базы данных", db_questions))

    def add_category(self, category):
        self.categories = [c for c in self.categories if c.name != category.name]
        self.categories.append(category)
        self.save_category(category)

    def remove_category(self, name):
        self.categories = [c for c in self.categories if c.name != name]
        self.delete_category_file(name)

    def get_category(self, name):
        return next((c for c in self.categories if c.name == name), None)

    def authenticate_user(self, username):
        username = username.strip()
        if not username:
            return False
        
        user = next((u for u in self.users if u.username == username), None)
        if not user:
            user = User(username)
            self.users.append(user)
            self.save_users()
        
        self.current_user = user
        return True

    def add_result(self, username, category_name, score, total):
        user = next((u for u in self.users if u.username == username), None)
        if user:
            percent = round((score / total) * 100, 1)
            user.add_result(category_name, score, total, percent)
            self.save_users()

    def get_all_results(self):
        all_results = []
        for user in self.users:
            for result in user.results:
                all_results.append({
                    'username': user.username,
                    'time': result['time'],
                    'category': result['category'],
                    'score': result['score'],
                    'total': result['total'],
                    'percent': result['percent']
                })
        return sorted(all_results, key=lambda x: x['time'], reverse=True)