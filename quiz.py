import tkinter as tk
from tkinter import messagebox

class Quiz:
    def __init__(self, parent, app, questions, user, data_manager):
        self.parent = parent
        self.app = app
        self.questions = questions
        self.user = user
        self.data_manager = data_manager
        self.current = 0
        self.score = 0

    def start(self):
        """Временная заглушка"""
        messagebox.showinfo("В разработке", "Тестирование скоро будет доступно")
        self.parent.destroy()
        self.app.test_mode.show_menu()