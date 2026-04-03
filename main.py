# main.py
import tkinter as tk
from tkinter import messagebox
from data_manager import DataManager
from admin import AdminPanel
from test_mode import TestMode


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VOPROSNIk")
        self.root.geometry("1280x1080")
        self.root.minsize(900, 600)
        
        # Киберпанк цветовая схема
        self.colors = {
            'bg': '#0a0a0f',
            'bg_card': '#0f0f1a',
            'primary': '#00ffcc',
            'primary_light': '#66ffe0',
            'primary_dark': '#00ccaa',
            'secondary': '#ff00ff',
            'success': '#00ff88',
            'danger': '#ff3366',
            'warning': '#ffaa00',
            'dark': '#050508',
            'light': '#1a1a2e',
            'card_bg': '#0f0f1a',
            'text': '#e0e0e0',
            'text_muted': '#8888aa',
            'border': '#00ffcc'
        }
        
        # Шрифты
        self.fonts = {
            'title': ('Share Tech Mono', 28, 'bold'),
            'subtitle': ('Share Tech Mono', 16, 'bold'),
            'body': ('Segoe UI', 11),
            'button': ('Share Tech Mono', 11, 'bold'),
            'small': ('Share Tech Mono', 9)
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        self.data_manager = DataManager()
        self.current_user = None
        self.admin_panel = AdminPanel(self)
        self.test_mode = TestMode(self)
        self.admin_credentials = {"admin": "123"}
        
        self.show_role_selection()
    
    def create_card(self, parent, **kwargs):
        card = tk.Frame(parent, bg=self.colors['card_bg'], relief=tk.FLAT, bd=2)
        card.configure(highlightbackground=self.colors['primary'], highlightthickness=1)
        return card
    
    def create_frame(self):
        if hasattr(self, 'frame') and self.frame:
            self.frame.destroy()
        self.frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.frame.pack(fill=tk.BOTH, expand=True)
    
    def show_role_selection(self):
        self.create_frame()
        
        center_frame = tk.Frame(self.frame, bg=self.colors['bg'])
        center_frame.pack(expand=True)
        
        title_frame = tk.Frame(center_frame, bg=self.colors['bg'])
        title_frame.pack(pady=(0, 40))
        
        title = tk.Label(title_frame, text="VOPROSNIk", 
                         font=self.fonts['title'], fg=self.colors['primary'], 
                         bg=self.colors['bg'])
        title.pack()
        
        subtitle = tk.Label(title_frame, text=">> тестики <<", 
                           font=self.fonts['body'], fg=self.colors['secondary'], 
                           bg=self.colors['bg'])
        subtitle.pack()
        
        card = self.create_card(center_frame)
        card.pack(pady=20, padx=40, ipadx=50, ipady=35)
        
        tk.Label(card, text="[ ВЫБЕРИТЕ РЕЖИМ ]", font=self.fonts['subtitle'], 
                fg=self.colors['primary'], bg=self.colors['card_bg']).pack(pady=(0, 25))
        
        tester_btn = tk.Button(card, text="> ТЕСТИРОВЩИК <", command=self.show_tester_login,
                              bg=self.colors['success'], fg='#000000', font=self.fonts['button'],
                              width=25, height=2, relief=tk.FLAT, bd=0,
                              activebackground=self.colors['success'], activeforeground='#000000')
        tester_btn.pack(pady=8)
        
        admin_btn = tk.Button(card, text="> АДМИНИСТРАТОР <", command=self.show_admin_login,
                             bg=self.colors['warning'], fg='#000000', font=self.fonts['button'],
                             width=25, height=2, relief=tk.FLAT, bd=0,
                             activebackground=self.colors['warning'], activeforeground='#000000')
        admin_btn.pack(pady=8)
        
        exit_btn = tk.Button(card, text="> ВЫХОД <", command=self.root.quit,
                            bg=self.colors['danger'], fg='#000000', font=self.fonts['button'],
                            width=25, height=2, relief=tk.FLAT, bd=0,
                            activebackground=self.colors['danger'], activeforeground='#000000')
        exit_btn.pack(pady=8)
        
        for btn in [tester_btn, admin_btn, exit_btn]:
            original_bg = btn.cget('bg')
            btn.bind("<Enter>", lambda e, b=btn, bg=original_bg: b.configure(bg=self.colors['primary'], fg='#000000'))
            btn.bind("<Leave>", lambda e, b=btn, bg=original_bg: b.configure(bg=bg, fg='#000000'))
    
    def show_tester_login(self):
        self.create_frame()
        
        top_bar = tk.Frame(self.frame, bg=self.colors['dark'], height=55)
        top_bar.pack(fill=tk.X, side=tk.TOP)
        top_bar.pack_propagate(False)
        
        back_btn = tk.Button(top_bar, text="[ НАЗАД ]", command=self.show_role_selection,
                            bg=self.colors['dark'], fg=self.colors['primary'], 
                            font=self.fonts['button'], relief=tk.FLAT, bd=0,
                            activebackground=self.colors['dark'], activeforeground=self.colors['primary'])
        back_btn.pack(side=tk.LEFT, padx=20, pady=15)
        
        center_frame = tk.Frame(self.frame, bg=self.colors['bg'])
        center_frame.pack(expand=True)
        
        card = self.create_card(center_frame)
        card.pack(pady=60, padx=40, ipadx=50, ipady=40)
        
        tk.Label(card, text="[ ВХОД ДЛЯ ТЕСТИРОВЩИКА ]", font=self.fonts['subtitle'],
                fg=self.colors['primary'], bg=self.colors['card_bg']).pack(pady=(0, 25))
        
        tk.Label(card, text="ВВЕДИТЕ ВАШЕ ИМЯ:", font=self.fonts['body'],
                fg=self.colors['text_muted'], bg=self.colors['card_bg']).pack()
        
        self.tester_name_entry = tk.Entry(card, font=self.fonts['body'], width=30,
                                          bg=self.colors['dark'], fg=self.colors['primary'],
                                          insertbackground=self.colors['primary'],
                                          relief=tk.GROOVE, bd=2, highlightthickness=0)
        self.tester_name_entry.pack(pady=15, ipady=8)
        self.tester_name_entry.bind('<Return>', lambda event: self.tester_login())
        
        btn_frame = tk.Frame(card, bg=self.colors['card_bg'])
        btn_frame.pack(pady=15)
        
        login_btn = tk.Button(btn_frame, text="[ ВОЙТИ ]", command=self.tester_login,
                             bg=self.colors['success'], fg='#000000', font=self.fonts['button'],
                             width=12, height=1, relief=tk.FLAT, bd=0,
                             activebackground=self.colors['success'], activeforeground='#000000')
        login_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(btn_frame, text="[ ОТМЕНА ]", command=self.show_role_selection,
                              bg=self.colors['danger'], fg='#000000', font=self.fonts['button'],
                              width=12, height=1, relief=tk.FLAT, bd=0,
                              activebackground=self.colors['danger'], activeforeground='#000000')
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def tester_login(self):
        username = self.tester_name_entry.get().strip()
        if not username:
            messagebox.showerror("ОШИБКА", "Пожалуйста, введите ваше имя!")
            return
        self.current_user = username
        self.data_manager.authenticate_user(username)
        self.test_mode.show_menu()
    
    def show_admin_login(self):
        self.create_frame()
        
        top_bar = tk.Frame(self.frame, bg=self.colors['dark'], height=55)
        top_bar.pack(fill=tk.X, side=tk.TOP)
        top_bar.pack_propagate(False)
        
        back_btn = tk.Button(top_bar, text="[ НАЗАД ]", command=self.show_role_selection,
                            bg=self.colors['dark'], fg=self.colors['primary'], 
                            font=self.fonts['button'], relief=tk.FLAT, bd=0,
                            activebackground=self.colors['dark'], activeforeground=self.colors['primary'])
        back_btn.pack(side=tk.LEFT, padx=20, pady=15)
        
        center_frame = tk.Frame(self.frame, bg=self.colors['bg'])
        center_frame.pack(expand=True)
        
        card = self.create_card(center_frame)
        card.pack(pady=60, padx=40, ipadx=50, ipady=40)
        
        tk.Label(card, text="[ ВХОД ДЛЯ АДМИНИСТРАТОРА ]", font=self.fonts['subtitle'],
                fg=self.colors['primary'], bg=self.colors['card_bg']).pack(pady=(0, 25))
        
        tk.Label(card, text="ЛОГИН:", font=self.fonts['body'],
                fg=self.colors['text_muted'], bg=self.colors['card_bg']).pack(anchor='w', pady=(10, 0))
        self.admin_login_entry = tk.Entry(card, font=self.fonts['body'], width=30,
                                          bg=self.colors['dark'], fg=self.colors['primary'],
                                          insertbackground=self.colors['primary'],
                                          relief=tk.GROOVE, bd=2)
        self.admin_login_entry.pack(pady=5, ipady=8)
        
        tk.Label(card, text="ПАРОЛЬ:", font=self.fonts['body'],
                fg=self.colors['text_muted'], bg=self.colors['card_bg']).pack(anchor='w', pady=(10, 0))
        self.admin_password_entry = tk.Entry(card, font=self.fonts['body'], width=30,
                                             bg=self.colors['dark'], fg=self.colors['primary'],
                                             insertbackground=self.colors['primary'],
                                             relief=tk.GROOVE, bd=2, show="*")
        self.admin_password_entry.pack(pady=5, ipady=8)
        
        btn_frame = tk.Frame(card, bg=self.colors['card_bg'])
        btn_frame.pack(pady=20)
        
        login_btn = tk.Button(btn_frame, text="[ ВОЙТИ ]", command=self.admin_login,
                             bg=self.colors['warning'], fg='#000000', font=self.fonts['button'],
                             width=12, height=1, relief=tk.FLAT, bd=0,
                             activebackground=self.colors['warning'], activeforeground='#000000')
        login_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(btn_frame, text="[ ОТМЕНА ]", command=self.show_role_selection,
                              bg=self.colors['danger'], fg='#000000', font=self.fonts['button'],
                              width=12, height=1, relief=tk.FLAT, bd=0,
                              activebackground=self.colors['danger'], activeforeground='#000000')
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
    
    def admin_login(self):
        login = self.admin_login_entry.get().strip()
        password = self.admin_password_entry.get().strip()
        if not login or not password:
            messagebox.showerror("ОШИБКА", "Введите логин и пароль!")
            return
        if login in self.admin_credentials and self.admin_credentials[login] == password:
            self.admin_panel.show_menu()
        else:
            messagebox.showerror("ОШИБКА", "Неверный логин или пароль!")


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()