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