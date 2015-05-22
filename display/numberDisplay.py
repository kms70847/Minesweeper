from imageGrid import ImageGrid
from Tkinter import *
from geometry import Point

class NumberDisplay(ImageGrid):
    def __init__(self, root, digits=3):
        names = {str(x): "images/big_{}.png".format(x) for x in range(10)}
        names["empty"] = "images/big_empty.png"
        names["minus"] = "images/big_minus.png"
        ImageGrid.__init__(self, root, names=names, rows=1, cols=digits, default="empty")
        self.digits = digits
        self.max_value = 10**self.digits - 1
        self.value = None
    def get(self):
        return self.value
    def set(self, value):
        self.value = value
        if value is None:
            for i in range(self.digits):
                self.set_image(Point(i,0), "empty")
        elif isinstance(value, int):
            s = str(value)
            assert len(s) <= self.digits
            while len(s) < self.digits:
                s = " " + s
            for idx, c in enumerate(s):
                name = {" ": "empty", "-": "minus"}.get(c,c)
                self.set_image(Point(idx,0), name)
        else:
            raise ValueError("value may only be integer or None")