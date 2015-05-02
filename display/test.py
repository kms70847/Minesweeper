from Tkinter import *
from PIL import Image, ImageTk
from stateView import StateView
from settingsWindow import SettingsWindow

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
    state = State(*cur_difficulty[1:])
    state.bind(state_changed)
    state_view = StateView(root, state)
    state_view.grid(row=1, column=0)
    reset_button.set_image("images/covered.png")

def show_settings():
    global cur_difficulty
    window = SettingsWindow(root, cur_difficulty)
    window.grab_set()
    root.wait_window(window)
    if window.setting_chosen != None:
        cur_difficulty = window.setting_chosen
        new_game()


import random
random.seed(0)

#beginner: 9,9,10
#intermediate: 16, 16, 40
#advanced: 16, 30, 99
cur_difficulty = ("Intermediate", 16, 16, 40)
root = Tk()

menubar = Menu(root)
root.config(menu=menubar)
gamemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Game", menu=gamemenu)
gamemenu.add_command(label = "New", command=new_game)
gamemenu.add_command(label = "Difficulty", command=show_settings)
gamemenu.add_command(label = "Exit", command=root.quit)

reset_button = ImageButton(root, "images/covered.png", command=new_game)
reset_button.grid(row=0, column=0)

state = None
state_view = None
new_game()

root.mainloop()