from Tkinter import *
from PIL import Image, ImageTk
from stateView import StateView

import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from state import State

class ImageButton(Button):
    def __init__(self, root, filename, **kwargs):
        self.photo = ImageTk.PhotoImage(Image.open(filename))
        Button.__init__(self, image=self.photo, **kwargs)
    def set_image(self, filename):
        self.photo = ImageTk.PhotoImage(Image.open(filename))
        self.config(image = self.photo)


#beginner: 9,9,10
#intermediate: 16, 16, 40
#advanced: 16, 30, 99
state = State(16, 16, 40)
root = Tk()

reset_button = ImageButton(root, "images/covered.png")
reset_button.grid(row=0, column=0)

state_view = StateView(root, state)
state_view.grid(row=1, column=0)
root.mainloop()