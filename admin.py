import tkinter as tk
from tkinter import messagebox, ttk

class AdminPanel:
    def __init__(self, app):
        self.app = app

    def show_menu(self):
        """Временная заглушка — позже Разработчик 3 реализует полностью"""
        self.app.create_frame()
        label = tk.Label(self.app.frame, text="Админ-панель (в разработке)", 
                         font=('Arial', 20), bg='lightblue')
        label.pack(pady=50)
        
        btn = tk.Button(self.app.frame, text="Назад", 
                        command=self.app.show_login, font=('Arial', 14))
        btn.pack(pady=20)

    def add_category_window(self):
        """Заглушка — будет реализована позже"""
        messagebox.showinfo("В разработке", "Функция добавления темы будет доступна позже")

    def edit_category_window(self):
        """Заглушка"""
        messagebox.showinfo("В разработке", "Функция редактирования темы будет доступна позже")

    def delete_category_window(self):
        """Заглушка"""
        messagebox.showinfo("В разработке", "Функция удаления темы будет доступна позже")

    def show_results(self):
        """Заглушка"""
        messagebox.showinfo("В разработке", "Функция просмотра результатов будет доступна позже")