import tkinter as tk
import tkinter.font as tkFont
from components.widgets import ScrollFrame, TagButton, TagMessage


class Application(tk.Frame):

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        # --------Variables----------------
        self.flag = False
        self.todo_id = None

        # ------------Fonts---------------
        self.normal_Font = tkFont.Font(family="Helvetica", size=15, overstrike=0)
        self.strike_Font = tkFont.Font(family="Helvetica", size=15, overstrike=1)

        # ---------Title Frame-------------------
        self.title_frame = tk.Frame(root, bg='blue')
        self.title = tk.Label(self.title_frame, text='Todo:', font='Helvetica, 25', bg='blue', fg='white', justify='left')
        self.title.pack(side='left', fill='x')
        self.title_frame.pack(fill='x')

        # ----------Check Frame-----------------
        self.check_frame = tk.Frame(root)
        self.check = tk.IntVar()
        self.c1 = tk.Checkbutton(self.check_frame, text='Completed', variable=self.check, relief=tk.FLAT, font='12')
        self.c1.pack(side='left', fill='x')
        self.check_frame.pack(fill='x')

        # ---------Form Frame--------------------
        self.form_frame = tk.Frame(root)
        f = tk.Frame(self.form_frame)
        self.e1 = tk.Entry(f, width=26, bg='lightblue', relief=tk.SUNKEN, bd=10, font=self.normal_Font)
        self.e1.pack(side='left', fill='x')
        self.btn_create = tk.Button(f, text='Create', command=None, bg='lightblue', relief=tk.RAISED, bd=4, font=self.normal_Font)
        self.btn_create.pack(side='right')
        f.pack()

        self.form_frame.pack()

        #-------------Status Frame--------------------
        self.status_frame = tk.Frame(root, bg='blue')
        self.status_label = tk.Label(self.status_frame, text='Status:', bd=1, bg='blue', fg='white', font='Helvetica 12 bold')
        self.status_label.pack(side='left', fill='x')
        self.status_frame.pack(side='bottom', fill='x')


if __name__ == '__main__':
    root = tk.Tk()
    root.title('To-do list')
    root.geometry('400x500+200+200')
    root.resizable(False, False)
    Application(root)
    root.mainloop()
