import tkinter

NEWLINE = "\n"
ARIAL = "Arial"
ARIALBOLD = "Arial Bold"

class Document:
    def __init__(self, width=200, height=200, title="pydocument", bg="white"):
        self.app = tkinter.Tk()
        self.width = width
        self.height = height
        self.bg = bg

        self.app.geometry(f"{width}x{height}")
        self.app.configure(bg=self.bg)
        self.app.title(title)

    def start(self):
        self.app.mainloop()

    def set_title(self, title: str):
        self.app.title(title)

    def disable_maximize(self):
        self.app.resizable(0, 0)

    def enable_maximize(self):
        self.app.resizable(1, 1)

    def change_width(self, width: int):
        self.width = width
        self.app.geometry(f"{self.width}x{self.height}")

    def change_height(self, height: int):
        self.height = height
        self.app.geometry(f"{self.width}x{self.height}")

    def change_size(self, width: int, height: int):
        self.width = width
        self.height = height
        self.app.geometry(f"{self.width}x{self.height}")

    def add_text(self, text: str, font="Arial", font_size=20, bg=None):
        label = tkinter.Label(self.app, text=text, font=(font, font_size))

        if bg:
            label.configure(bg=bg)
        else:
            label.configure(bg=self.bg)

        label.pack()

    def add_arial_text(self, text: str, font_size=20, bg=None):
        self.add_text(text, "Arial", font_size, bg)

    def add_arial_bold_text(self, text: str, font_size=20, bg=None):
        self.add_text(text, "Arial Bold", font_size, bg)

    def add_space(self, spaces=1, bg=None):
        for _ in range(spaces):
            label = tkinter.Label(self.app)

            if bg:
                label.configure(bg=bg)
            else:
                label.configure(bg=self.bg)

            label.pack()

    def add_newline(self, spaces=1, bg=None):
        self.add_space(spaces, bg)
