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

def state_changed(event, *args):
    if event == "game_ended":
        if state.game_state == state.lost:
            reset_button.set_image("images/mine.png")
        elif state.game_state == state.won:
            reset_button.set_image("images/flagged.png")

def new_game():
    global state_view, state
    if state_view is not None:
        print "new game!"
        state_view.grid_forget()
        state.unbind(state_view.state_changed) #bit of an encapsulation violation here...
    state = State(16, 16, 4)
    state.bind(state_changed)
    state_view = StateView(root, state)
    state_view.grid(row=1, column=0)
    reset_button.set_image("images/covered.png")

import random
random.seed(0)

#beginner: 9,9,10
#intermediate: 16, 16, 40
#advanced: 16, 30, 99
root = Tk()

reset_button = ImageButton(root, "images/covered.png", command=new_game)
reset_button.grid(row=0, column=0)

state = None
state_view = None
new_game()

root.mainloop()