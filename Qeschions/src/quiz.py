import tkinter as tk
from tkinter import messagebox
from models import Question


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
        self.parent.minsize(700, 500)
        self.parent.geometry("800x600")
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
        self.show_question()

    def show_question(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

        if self.current >= len(self.questions):
            self.show_results()
            return

        main_frame = tk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        q = self.questions[self.current]

        header_frame = tk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        tk.Label(header_frame, text=f"Вопрос {self.current + 1}/{len(self.questions)}",
                 font=('Arial', 14, 'bold')).pack()

        # Текст вопроса
        question_frame = tk.Frame(main_frame)
        question_frame.pack(fill=tk.X, pady=(0, 20))
        tk.Label(question_frame, text=q.text, font=('Arial', 12),
                 wraplength=700, justify='left').pack()

        self.var = tk.StringVar()
        answers_frame = tk.Frame(main_frame)
        answers_frame.pack(fill=tk.BOTH, expand=True)
        for i, option in enumerate(q.options):
            rb = tk.Radiobutton(answers_frame, text=option, variable=self.var,
                                value=str(i), font=('Arial', 11), anchor='w',
                                wraplength=650)
            rb.pack(fill=tk.X, padx=(20, 0), pady=2, anchor='w')

        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=20)

        tk.Button(btn_frame, text="Далее", command=self.next_question,
                  font=('Arial', 12, 'bold'), bg='lightblue').pack(side=tk.LEFT, padx=(0, 10))
        tk.Button(btn_frame, text="Главное меню", command=self.go_to_main_menu,
                  font=('Arial', 12), bg='orange').pack(side=tk.LEFT)

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
        percent = (self.score / len(self.questions)) * 100
        result_text = f"Результат: {self.score}/{len(self.questions)} ({percent:.1f}%)"

        main_frame = tk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(main_frame, text=result_text, font=('Arial', 20, 'bold'),
                 fg='green').pack(pady=50)

        self.data_manager.add_result(self.user, self.score, len(self.questions))

        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Новое тестирование",
                  command=self.restart_quiz, font=('Arial', 14), bg='lightgreen').pack(side=tk.LEFT, padx=(0, 10))
        tk.Button(btn_frame, text="Главное меню", command=self.go_to_main_menu,
                  font=('Arial', 14), bg='orange').pack(side=tk.LEFT)

    def restart_quiz(self):
        self.current = 0
        self.score = 0
        self.answers = {}
        self.show_question()

    def go_to_main_menu(self):
        self.parent.destroy()
        self.app.test_mode.show_menu()
