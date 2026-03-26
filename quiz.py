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
        self.answers = {}
        self.is_finished = False

    def start(self):
        self.parent.title("Тест")
        self.parent.minsize(600, 500)
        
        # Настройка сетки для масштабирования
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
        
        self.show_question()

    def show_question(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

        if self.current >= len(self.questions):
            self.show_results()
            return

        # Создаем контейнер с сеткой для масштабирования
        main_frame = tk.Frame(self.parent)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        q = self.questions[self.current]

        header_frame = tk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky="ew", pady=10)
        header_frame.grid_columnconfigure(0, weight=1)
        
        tk.Label(header_frame, text=f"Вопрос {self.current + 1}/{len(self.questions)}",
                 font=('Arial', 14, 'bold')).pack()

        question_frame = tk.Frame(main_frame)
        question_frame.grid(row=1, column=0, sticky="ew", pady=20, padx=20)
        question_frame.grid_columnconfigure(0, weight=1)
        
        tk.Label(question_frame, text=q.text, font=('Arial', 12),
                 wraplength=700, justify='left').pack(fill=tk.X)

        self.var = tk.StringVar()
        answers_frame = tk.Frame(main_frame)
        answers_frame.grid(row=2, column=0, sticky="nsew", pady=10, padx=20)
        answers_frame.grid_columnconfigure(0, weight=1)
        
        for i, option in enumerate(q.options):
            rb = tk.Radiobutton(answers_frame, text=option, variable=self.var,
                                value=str(i), font=('Arial', 11), anchor='w',
                                wraplength=650)
            rb.pack(fill=tk.X, pady=5, anchor='w')

        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=3, column=0, sticky="ew", pady=20)
        btn_frame.grid_columnconfigure(0, weight=1)
        
        btn_inner = tk.Frame(btn_frame)
        btn_inner.pack()
        
        tk.Button(btn_inner, text="Далее", command=self.next_question,
                  font=('Arial', 12, 'bold'), bg='lightblue', width=12).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_inner, text="Главное меню", command=self.go_to_main_menu,
                  font=('Arial', 12), bg='orange', width=12).pack(side=tk.LEFT, padx=10)

    def next_question(self):
        if not self.var.get():
            messagebox.showwarning("Внимание", "Выберите ответ!")
            return

        answer = int(self.var.get())
        self.answers[self.current] = answer
        if answer == self.questions[self.current].correct_index:
            self.score += 1

        self.current += 1
        self.show_question()

    def show_results(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

        percent = (self.score / len(self.questions)) * 100
        result_text = f"Результат: {self.score}/{len(self.questions)} ({percent:.1f}%)"

        main_frame = tk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(main_frame, text=result_text, font=('Arial', 24, 'bold'),
                 fg='green').pack(pady=50)

        self.data_manager.add_result(self.user, self.score, len(self.questions))

        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=30)
        tk.Button(btn_frame, text="Новое тестирование",
                  command=self.restart_quiz, font=('Arial', 14), bg='lightgreen', width=15).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Главное меню", command=self.go_to_main_menu,
                  font=('Arial', 14), bg='orange', width=15).pack(side=tk.LEFT, padx=10)

    def restart_quiz(self):
        self.current = 0
        self.score = 0
        self.answers = {}
        self.show_question()

    def go_to_main_menu(self):
        self.parent.destroy()
        self.app.show_login()