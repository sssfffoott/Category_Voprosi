import tkinter as tk
from tkinter import ttk, messagebox

class TestMode:
    def __init__(self, app):
        self.app = app

    def show_menu(self):
        """Временная заглушка"""
        self.app.create_frame()
        label = tk.Label(self.app.frame, text="Режим тестирования (в разработке)", 
                         font=('Arial', 20), bg='lightblue')
        label.pack(pady=50)
        
        btn = tk.Button(self.app.frame, text="Назад", 
                        command=self.app.show_login, font=('Arial', 14))
        btn.pack(pady=20)

    def start_quiz(self):
        """Заглушка"""
        messagebox.showinfo("В разработке", "Функция тестирования будет доступна позже")