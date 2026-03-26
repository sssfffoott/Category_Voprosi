import json
import os
from datetime import datetime
from models import Category


class DataManager:
    def __init__(self, filename='quiz_data.json'):
        self.filename = filename
        self.categories = []
        self.results = []
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.categories = [Category.from_dict(c) for c in data.get('categories', [])]
                    self.results = data.get('results', [])
            except Exception as e:
                print(f"Ошибка загрузки: {e}")
                self.categories = []
                self.results = []

    def save_data(self):
        data = {
            'categories': [c.to_dict() for c in self.categories],
            'results': self.results
        }
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Сохранено: {len(self.categories)} категорий")  # отладка
        except Exception as e:
            print(f"Ошибка сохранения: {e}")

    def add_category(self, category):
        self.categories = [c for c in self.categories if c.name != category.name]
        self.categories.append(category)
        self.save_data()

    def remove_category(self, name):
        self.categories = [c for c in self.categories if c.name != name]
        self.save_data()

    def get_category(self, name):
        return next((c for c in self.categories if c.name == name), None)

    def add_result(self, user, score, total):
        percent = round((score / total) * 100, 1)
        self.results.append({
            'time': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'user': user,
            'score': score,
            'total': total,
            'percent': percent
        })
        self.save_data()