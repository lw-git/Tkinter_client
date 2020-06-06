import tkinter as tk
import tkinter.font as tkFont
from components.widgets import ScrollFrame, TagButton, TagMessage
from components.utils import SaveThread
import requests
import time
import threading


class Application(tk.Frame):

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        # --------Variables----------------
        self.flag = False
        self.todo_id = None
        self.endpoint = 'http://127.0.0.1:8000/api/'
        self.todos = None
        self.todo = tk.StringVar()
        self.todo.trace("w", lambda *args: self.character_limit())
        self.thread_flag = False

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
                           textvariable=self.todo, relief=tk.SUNKEN,
                           bd=10, font=self.normal_Font)
        self.e1.pack(side='left', fill='x')
        self.btn_create = tk.Button(self.form_frame, text='Create',
                                    command=self.create_todo, bg='lightblue',
                                    relief=tk.RAISED, bd=4,
                                    font=self.normal_Font)
        self.btn_create.pack(side='right')
        self.form_frame.pack()

        # --------------Load todos---------------------
        self.scrollFrame = ScrollFrame(root, height=430)
        self.after(500, self.start_get_todos)

        # -------------Preloader---------------------
        self.preloader = tk.Frame(root)
        self.label = tk.Label(self.preloader)
        self.label.pack()
        self.frames = [tk.PhotoImage(file='images/spinner.gif',
                            format='gif -index %i' % (i)) for i in range(1, 12)]

        # -------------Status Frame--------------------
        self.status_frame = tk.Frame(root, bg='blue')
        self.status_label = tk.Label(self.status_frame, text='Status:',
                                     bd=1, bg='blue', fg='white',
                                     font='Helvetica 12 bold')
        self.status_label.pack(side='left', fill='x')
        self.status_frame.pack(side='bottom', fill='x')

    def toggle_spinner(self):
        self.flag = not self.flag
        if self.flag:
            threading.Thread(target=self.spinner).start()
            self.scrollFrame.forget()
            self.preloader.pack()
        else:
            self.preloader.forget()
            self.scrollFrame.pack()

    def spinner(self, ind=1):
        while self.flag:
            frame = self.frames[ind % len(self.frames)]
            ind += 1
            self.label.configure(image=frame)
            time.sleep(0.1)

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

    def on_thread_finished(self, data):
        self.thread_flag = True

    def do_request(self, method='get', query='', data={}):
        params = {
            'method': method,
            'query': query,
            'data': data,
            'num': self.endpoint + query
        }
        t = SaveThread(self.on_thread_finished,
                       target=self.request_thread,
                       kwargs=params)
        t.start()

    def request_thread(self, **kwargs):
        r = requests.request(kwargs['method'],
                             self.endpoint + kwargs['query'],
                             data=kwargs.get('data'))
        if len(r.text) > 0:
            self.todos = r.json()

    def start_get_todos(self):
        threading.Thread(target=self.get_todos).start()

    def get_todos(self):
        self.toggle_spinner()
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
                text.bind('<Button-1>', self.prepare_update)
                text.pack(side='left', fill='x')
                btn = TagButton(task, text='X', tag=i, bg='black',
                                fg='white', font='bold')
                btn.bind('<Button-1>', self.delete_todo)
                btn.pack(side='right')
                task.pack(fill='x')

            self.scrollFrame.pack()
        finally:
            self.toggle_spinner()

    def character_limit(self):
        if len(self.todo.get()) > 200:
            self.todo.set(self.todo.get()[:200])

    def create_todo(self):
        self.btn_create.config(state='disabled')
        data = {
            'title': self.todo.get(),
            'completed': bool(self.check.get())
        }
        if self.todo.get() != '':
            response = 'Error'
            try:
                response = requests.post(self.endpoint + 'create/', data)
            except IOError:
                self.get_status(response)
            else:
                self.get_status(response)
                self.start_get_todos()
            finally:
                self.btn_create.config(state='normal')
                self.todo.set('')
        else:
            self.btn_create.config(state='normal')

    def prepare_update(self, e):
        updated_todo = self.todos[e.widget.tag]
        self.check.set(updated_todo['completed'])
        self.todo.set(updated_todo['title'])
        self.todo_id = (updated_todo['id'])
        self.btn_create.config(text='Update', command=self.update_todo)

        for i in self.scrollFrame.viewPort.winfo_children():
            for j in i.winfo_children():
                if isinstance(j, TagButton):
                    j.forget()

    def update_todo(self):
        data = {
            'title': self.todo.get(),
            'completed': bool(self.check.get())
        }
        if self.todo.get() != '':
            response = 'Error'
            try:
                response = requests.put(
                            self.endpoint + f'{self.todo_id}/update/',
                            data)
            except IOError:
                self.get_status(response)
            else:
                self.get_status(response)
                self.start_get_todos()
                self.btn_create.config(text='Create', command=self.create_todo)
                self.check.set(0)
                self.todo.set('')

        for i in self.scrollFrame.viewPort.winfo_children():
            for j in i.winfo_children():
                if isinstance(j, TagButton):
                    j.pack()

    def delete_todo(self, e):
        self.todo_id = self.todos[e.widget.tag]['id']
        if self.todo_id:
            response = 'Error'
            try:
                response = requests.delete(
                    self.endpoint + f'{self.todo_id}/delete/')
            except IOError:
                self.get_status(response)
            else:
                self.get_status(response)
                self.start_get_todos()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('To-do list')
    root.geometry('400x500+200+200')
    root.resizable(False, False)
    Application(root)
    root.mainloop()
