from tkinter_ex import *
from collections import OrderedDict
import pickle

score_filename = "high_scores.txt"

def try_load(filename, default=None):
    try:
        with open(filename) as file:
            return pickle.load(file)
    except IOError:
        return default

def get_scores():
    default = (
        ("Beginner",     ("Kevin", 999)),
        ("Intermediate", ("Kevin", 999)),
        ("Expert",       ("Kevin", 999))
    )
    default = OrderedDict(default)
    return try_load(score_filename, default)

def qualifies(level, score):
    scores = get_scores()
    return level in scores and score < scores[level]

def update_scores(level, name, score):
    scores = get_scores()
    scores[level] = (name, score)
    with open(score_filename, "w") as file:
        pickle.dump(scores, file)

class HighScoreWindow(Toplevel):
    def __init__(self, root):
        Toplevel.__init__(self, root)
        self.resizable(0,0)
        self.title("High Scores")
        scores = get_scores()

        label_frame = Frame(self)
        label_frame.pack()
        for y, (key, values) in enumerate(scores.items()):
            data = (key,) + values
            for x, value in enumerate(data):
                Label(label_frame, text=value).grid(column=x, row=y)

        Button(self, text="OK", command=self.destroy).pack()