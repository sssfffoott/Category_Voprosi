# models.py
from datetime import datetime


class Question:
    def __init__(self, text, options, correct_index, category):
        self.text = text
        self.options = options
        self.correct_index = correct_index
        self.category = category

    def to_dict(self):
        return {
            'text': self.text,
            'options': self.options,
            'correct_index': self.correct_index,
            'category': self.category
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['text'],
            data['options'],
            data['correct_index'],
            data['category']
        )


class Category:
    def __init__(self, name, questions):
        self.name = name
        self.questions = questions

    def to_dict(self):
        return {
            'name': self.name,
            'questions': [q.to_dict() for q in self.questions]
        }

    @classmethod
    def from_dict(cls, data):
        questions = [Question.from_dict(q) for q in data['questions']]
        return cls(data['name'], questions)


class User:
    def __init__(self, username):
        self.username = username
        self.results = []

    def add_result(self, category_name, score, total, percent):
        self.results.append({
            'time': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'category': category_name,
            'score': score,
            'total': total,
            'percent': percent
        })

    def get_results(self, category_name=None):
        if category_name:
            return [r for r in self.results if r['category'] == category_name]
        return self.results

    def to_dict(self):
        return {
            'username': self.username,
            'results': self.results
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(data['username'])
        user.results = data.get('results', [])
        return user