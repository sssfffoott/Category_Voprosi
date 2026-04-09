# quiz.py
import tkinter as tk
from tkinter import messagebox


class Quiz:
    def __init__(self, parent_frame, app, questions, user, data_manager, category_name):
        self.parent_frame = parent_frame
        self.app = app
        self.questions = questions
        self.user = user
        self.data_manager = data_manager
        self.category_name = category_name
        self.current = 0
        self.score = 0
        self.answers = {}

    def start(self):
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        self.show_question()

    def show_question(self):
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        if self.current >= len(self.questions):
            self.show_results()
            return

        top_bar = tk.Frame(self.parent_frame, bg=self.app.colors['dark'], height=50)
        top_bar.pack(fill=tk.X, side=tk.TOP)
        top_bar.pack_propagate(False)

        info_frame = tk.Frame(top_bar, bg=self.app.colors['dark'])
        info_frame.pack(fill=tk.X, padx=30, pady=10)

        tk.Label(info_frame, text=f"Тема: {self.category_name}",
                 font=self.app.fonts['body'],
                 fg=self.app.colors['primary'],
                 bg=self.app.colors['dark']).pack(side=tk.LEFT)

        tk.Label(info_frame, text=f"Вопрос {self.current + 1} из {len(self.questions)}",
                 font=self.app.fonts['body'],
                 fg=self.app.colors['text_muted'],
                 bg=self.app.colors['dark']).pack(side=tk.RIGHT)

        center_frame = tk.Frame(self.parent_frame, bg=self.app.colors['bg'])
        center_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=30)

        card = self.app.create_card(center_frame)
        card.pack(fill=tk.BOTH, expand=True, pady=20, ipadx=20, ipady=20)

        q = self.questions[self.current]

        tk.Label(card, text=q.text,
                 font=('Segoe UI', 16),
                 fg=self.app.colors['text'],
                 bg=self.app.colors['card_bg'],
                 wraplength=700, justify='left').pack(pady=(0, 30))

        self.var = tk.StringVar()

        answers_frame = tk.Frame(card, bg=self.app.colors['card_bg'])
        answers_frame.pack(fill=tk.BOTH, expand=True)

        for i, option in enumerate(q.options):
            rb = tk.Radiobutton(
                answers_frame,
                text=option,
                variable=self.var,
                value=str(i),
                font=self.app.fonts['body'],
                anchor='w',
                bg=self.app.colors['card_bg'],
                fg=self.app.colors['text'],
                selectcolor=self.app.colors['card_bg']
            )
            rb.pack(fill=tk.X, pady=8, padx=20)

        btn_frame = tk.Frame(card, bg=self.app.colors['card_bg'])
        btn_frame.pack(fill=tk.X, pady=20)

        next_btn = tk.Button(btn_frame, text="ДАЛЕЕ",
                             command=self.next_question,
                             bg=self.app.colors['primary'],
                             fg='black',
                             font=self.app.fonts['button'],
                             width=15)
        next_btn.pack(side=tk.RIGHT, padx=5)

        interrupt_btn = tk.Button(btn_frame, text="ПРЕРВАТЬ",
                                  command=self.interrupt_quiz,
                                  bg=self.app.colors['danger'],
                                  fg='white',
                                  font=self.app.fonts['button'],
                                  width=15)
        interrupt_btn.pack(side=tk.LEFT, padx=5)

    def next_question(self):
        selected = self.var.get()

        if selected == "":
            messagebox.showwarning("Ошибка", "Выбери ответ!")
            return

        selected = int(selected)
        q = self.questions[self.current]

        self.answers[self.current] = selected

        if selected == q.correct_index:
            self.score += 1

        self.current += 1
        self.show_question()

    def interrupt_quiz(self):
        if messagebox.askyesno("Выход", "Прервать тест? Результат не будет сохранен!"):
            self.go_to_menu()

    def show_results(self):
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        percent = (self.score / len(self.questions)) * 100

        if percent >= 80:
            grade = "ОТЛИЧНО!"
            grade_color = self.app.colors['success']
        elif percent >= 60:
            grade = "ХОРОШО!"
            grade_color = self.app.colors['warning']
        else:
            grade = "УЧИТЕСЬ ЛУЧШЕ!"
            grade_color = self.app.colors['danger']

        center_frame = tk.Frame(self.parent_frame, bg=self.app.colors['bg'])
        center_frame.pack(expand=True)

        card = self.app.create_card(center_frame)
        card.pack(pady=50, padx=40, ipadx=50, ipady=40)

        tk.Label(card, text=grade,
                 font=self.app.fonts['title'],
                 fg=grade_color,
                 bg=self.app.colors['card_bg']).pack(pady=10)

        tk.Label(card, text=f"{self.score} / {len(self.questions)}",
                 font=('Segoe UI', 24, 'bold'),
                 fg=self.app.colors['primary'],
                 bg=self.app.colors['card_bg']).pack(pady=10)

        tk.Label(card, text=f"{percent:.1f}%",
                 font=('Segoe UI', 18),
                 fg=self.app.colors['text'],
                 bg=self.app.colors['card_bg']).pack(pady=5)

        self.data_manager.add_result(
            self.user,
            self.category_name,
            self.score,
            len(self.questions)
        )

        btn_frame = tk.Frame(card, bg=self.app.colors['card_bg'])
        btn_frame.pack(pady=30)

        restart_btn = tk.Button(btn_frame, text="ПРОЙТИ ЗАНОВО",
                                command=self.restart_quiz,
                                bg=self.app.colors['success'],
                                fg='black',
                                font=self.app.fonts['button'],
                                width=15)
        restart_btn.pack(side=tk.LEFT, padx=10)

        answers_btn = tk.Button(btn_frame, text="ПОСМОТРЕТЬ ОТВЕТЫ",
                                command=self.show_answers,
                                bg=self.app.colors['secondary'],
                                fg='black',
                                font=self.app.fonts['button'],
                                width=15)
        answers_btn.pack(side=tk.LEFT, padx=10)

        menu_btn = tk.Button(btn_frame, text="В МЕНЮ",
                             command=self.go_to_menu,
                             bg=self.app.colors['primary'],
                             fg='black',
                             font=self.app.fonts['button'],
                             width=15)
        menu_btn.pack(side=tk.LEFT, padx=10)

    def show_answers(self):
        win = tk.Toplevel(self.app.root)
        win.title("Просмотр ответов")
        win.geometry("700x500")
        win.configure(bg=self.app.colors['bg'])
        win.transient(self.app.root)
        win.grab_set()

        header = tk.Frame(win, bg=self.app.colors['primary'], height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(header, text="ПРОСМОТР ОТВЕТОВ",
                 font=self.app.fonts['subtitle'],
                 fg='black',
                 bg=self.app.colors['primary']).pack(pady=10)

        text_frame = tk.Frame(win, bg=self.app.colors['bg'])
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_area = tk.Text(text_frame, font=('Segoe UI', 11), wrap=tk.WORD,
                           yscrollcommand=scrollbar.set,
                           bg=self.app.colors['dark'],
                           fg=self.app.colors['text'],
                           relief=tk.FLAT, padx=15, pady=15)
        text_area.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_area.yview)

        for i, q in enumerate(self.questions):
            user_ans = self.answers.get(i, -1)
            correct = q.correct_index
            is_correct = (user_ans == correct)

            status = "[+]" if is_correct else "[-]"
            text_area.insert(tk.END, f"\n{status} Вопрос {i+1}: {q.text}\n")
            text_area.insert(tk.END, f"   Ваш ответ: {q.options[user_ans] if user_ans != -1 else 'Нет ответа'}\n")
            if not is_correct:
                text_area.insert(tk.END, f"   Правильный: {q.options[correct]}\n")
            text_area.insert(tk.END, "-" * 60 + "\n")

        text_area.config(state=tk.DISABLED)

        close_btn = tk.Button(win, text="ЗАКРЫТЬ",
                              command=win.destroy,
                              bg=self.app.colors['primary'],
                              fg='black',
                              font=self.app.fonts['button'],
                              width=15)
        close_btn.pack(pady=15)

    def restart_quiz(self):
        self.current = 0
        self.score = 0
        self.answers = {}
        self.show_question()

    def go_to_menu(self):
        self.app.test_mode.show_menu()