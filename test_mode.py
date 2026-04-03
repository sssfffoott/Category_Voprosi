# test_mode.py - киберпанк версия
import tkinter as tk
from tkinter import ttk, messagebox


class TestMode:
    def __init__(self, app):
        self.app = app
    
    def show_menu(self):
        self.app.create_frame()
        
        top_bar = tk.Frame(self.app.frame, bg=self.app.colors['dark'], height=55)
        top_bar.pack(fill=tk.X, side=tk.TOP)
        top_bar.pack_propagate(False)
        
        back_btn = tk.Button(top_bar, text="[ ГЛАВНОЕ МЕНЮ ]", command=self.app.show_role_selection,
                            bg=self.app.colors['dark'], fg=self.app.colors['primary'], 
                            font=self.app.fonts['button'], relief=tk.FLAT, bd=0,
                            activebackground=self.app.colors['dark'], activeforeground=self.app.colors['primary'])
        back_btn.pack(side=tk.LEFT, padx=20, pady=15)
        
        welcome = tk.Label(top_bar, text=f">> {self.app.current_user} <<", 
                          font=self.app.fonts['body'], fg=self.app.colors['secondary'],
                          bg=self.app.colors['dark'])
        welcome.pack(side=tk.RIGHT, padx=20)
        
        center_frame = tk.Frame(self.app.frame, bg=self.app.colors['bg'])
        center_frame.pack(expand=True)
        
        card = self.app.create_card(center_frame)
        card.pack(pady=50, padx=40, ipadx=50, ipady=35)
        
        tk.Label(card, text="[ ВЫБЕРИТЕ ТЕМУ ]", font=self.app.fonts['subtitle'],
                fg=self.app.colors['primary'], bg=self.app.colors['card_bg']).pack(pady=(0, 25))
        
        if not self.app.data_manager.categories:
            tk.Label(card, text="[ НЕТ ДОСТУПНЫХ ТЕМ ]", font=self.app.fonts['body'],
                    fg=self.app.colors['danger'], bg=self.app.colors['card_bg']).pack(pady=20)
            return
        
        self.cat_combo = ttk.Combobox(card, values=[c.name for c in self.app.data_manager.categories],
                                      font=self.app.fonts['body'], width=35, state='readonly')
        self.cat_combo.pack(pady=10, ipady=8)
        if self.app.data_manager.categories:
            self.cat_combo.set(self.app.data_manager.categories[0].name)
        
        start_btn = tk.Button(card, text="> НАЧАТЬ ТЕСТ <", command=self.start_quiz,
                             bg=self.app.colors['success'], fg='#000000', font=self.app.fonts['button'],
                             width=25, height=2, relief=tk.FLAT, bd=0,
                             activebackground=self.app.colors['success'], activeforeground='#000000')
        start_btn.pack(pady=25)
        
        start_btn.bind("<Enter>", lambda e: start_btn.configure(bg=self.app.colors['primary'], fg='#000000'))
        start_btn.bind("<Leave>", lambda e: start_btn.configure(bg=self.app.colors['success'], fg='#000000'))
    
    def start_quiz(self):
        selected = self.cat_combo.get()
        if not selected:
            messagebox.showerror("ОШИБКА", "Выберите тему!")
            return
        
        category = self.app.data_manager.get_category(selected)
        if not category:
            messagebox.showerror("ОШИБКА", "Тема не найдена!")
            return
        
        from quiz import Quiz
        
        for widget in self.app.frame.winfo_children():
            widget.destroy()
        
        quiz = Quiz(self.app.frame, self.app, category.questions, 
                    self.app.current_user, self.app.data_manager, category.name)
        quiz.start()