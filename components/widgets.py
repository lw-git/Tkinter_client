import tkinter as tk


class ScrollFrame(tk.Frame):
    def __init__(self, parent, height):
        super().__init__(parent)

        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.viewPort = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(self, orient="vertical",
                                command=self.canvas.yview)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(height=height)
        self.canvas_window = self.canvas.create_window((4, 4),
                                                       window=self.viewPort,
                                                       anchor="nw",
                                                       tags="self.viewPort")

        self.viewPort.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind("<Configure>", self.onCanvasConfigure)

        self.onFrameConfigure(None)

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def onCanvasConfigure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)


class TagMessage(tk.Label):
    def __init__(self, master, tag=None, *args, **kwargs):
        tk.Message.__init__(self, master, *args, **kwargs)
        self.tag = tag


class TagButton(tk.Button):
    def __init__(self, master, tag=None, *args, **kwargs):
        tk.Button.__init__(self, master, *args, **kwargs)
        self.tag = tag
