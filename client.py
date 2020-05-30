import tkinter as tk
import tkinter.font as tkFont
from components.widgets import ScrollFrame, TagButton, TagMessage
import requests


class Application(tk.Frame):

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        # --------Variables----------------
        self.flag = False
        self.todo_id = None
        self.endpoint = 'http://127.0.0.1:8000/api/'
        self.todos = None

        # ------------Fonts---------------
        self.normal_Font = tkFont.Font(family="Helvetica", size=15, overstrike=0)
        self.strike_Font = tkFont.Font(family="Helvetica", size=15, overstrike=1)

        # ---------Title Frame-------------------
        self.title_frame = tk.Frame(root, bg='blue')
        self.title = tk.Label(self.title_frame, text='Todo:',
                              font='Helvetica, 25', bg='blue',
                              fg='white', justify='left')
        self.title.pack(side='left', fill='x')
        self.title_frame.pack(fill='x')

        # ----------Check Frame-----------------
        self.check_frame = tk.Frame(root)
        self.check = tk.IntVar()
        self.c1 = tk.Checkbutton(self.check_frame, text='Completed',
                                 variable=self.check, relief=tk.FLAT,
                                 font='12')
        self.c1.pack(side='left', fill='x')
        self.check_frame.pack(fill='x')

        # ---------Form Frame--------------------
        self.form_frame = tk.Frame(root)
        self.e1 = tk.Entry(self.form_frame, width=26, bg='lightblue',
                           relief=tk.SUNKEN, bd=10, font=self.normal_Font)
        self.e1.pack(side='left', fill='x')
        self.btn_create = tk.Button(self.form_frame, text='Create',
                                    command=None, bg='lightblue',
                                    relief=tk.RAISED, bd=4,
                                    font=self.normal_Font)
        self.btn_create.pack(side='right')
        self.form_frame.pack()

        # --------------Load todos---------------------
        self.scrollFrame = ScrollFrame(root, height=430)
        self.after(500, self.get_todos)

        # -------------Status Frame--------------------
        self.status_frame = tk.Frame(root, bg='blue')
        self.status_label = tk.Label(self.status_frame, text='Status:',
                                     bd=1, bg='blue', fg='white',
                                     font='Helvetica 12 bold')
        self.status_label.pack(side='left', fill='x')
        self.status_frame.pack(side='bottom', fill='x')

    def get_status(self, response):
        error = False
        if hasattr(response, 'status_code'):
            if response.status_code > 204:
                error = True
        else:
            error = True

        if not error:
            self.status_label.config(text='Status: ok', bg='blue')
            self.status_frame.config(bg='blue')
        else:
            self.status_label.config(text='Status: error', bg='red')
            self.status_frame.config(bg='red')

    def get_todos(self):
        response = 'Error'
        try:
            response = requests.get(self.endpoint)
            self.todos = response.json()
        except IOError:
            self.get_status(response)
        else:
            self.get_status(response)
            for widget in self.scrollFrame.viewPort.winfo_children():
                widget.destroy()

            for i, todo in enumerate(self.todos):
                task = tk.Frame(self.scrollFrame.viewPort, bg='lightblue',
                                relief=tk.SUNKEN, bd=10)
                text = TagMessage(task, text=todo['title'], justify='center',
                                  width=300, tag=i, pady=10, bg='lightblue')
                if todo['completed']:
                    text.configure(font=self.strike_Font)
                else:
                    text.configure(font=self.normal_Font)
                text.pack(side='left', fill='x')
                btn = TagButton(task, text='X', tag=i, bg='black',
                                fg='white', font='bold')
                btn.pack(side='right')
                task.pack(fill='x')

            self.scrollFrame.pack()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('To-do list')
    root.geometry('400x500+200+200')
    root.resizable(False, False)
    Application(root)
    root.mainloop()
