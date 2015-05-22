from Tkinter import *

def try_load(filename, default=None):
    try:
        with open(filename) as file:
            return json.load(file)
    except IOError:
        return default

def get_scores():
    default = (
        ("Beginner", "Kevin", 999),
        ("Intermediate", "Kevin", 999),
        ("Expert", "Kevin", 999)
    )
    return try_load("high_scores.txt", default)

class HighScoreWindow(Toplevel):
    def __init__(self, root):
        Toplevel.__init__(self, root)
        self.resizable(0,0)
        self.title("High Scores")
        scores = get_scores()

        label_frame = Frame(self)
        label_frame.pack()
        for y, data in enumerate(scores):
            for x, value in enumerate(data):
                Label(label_frame, text=value).grid(column=x, row=y)

        Button(self, text="OK", command=self.destroy).pack()