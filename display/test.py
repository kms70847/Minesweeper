from Tkinter import *
import tkSimpleDialog
from PIL import Image, ImageTk
from time import time

from stateView import StateView
from settingsWindow import SettingsWindow
from numberDisplay import NumberDisplay
import highscores

import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from state import State

class ImageButton(Button):
    def __init__(self, root, filename, **kwargs):
        self.photo = ImageTk.PhotoImage(Image.open(filename))
        Button.__init__(self, root, image=self.photo, **kwargs)
    def set_image(self, filename):
        self.photo = ImageTk.PhotoImage(Image.open(filename))
        self.config(image = self.photo)

def state_changed(event, *args):
    global start_time
    mine_counter.set(state.num_mines - state.state_count(state.flagged))
    if event == "started":
        start_time = time()
    elif event == "game_ended":
        if state.game_state == state.lost:
            reset_button.set_image("images/mine.png")
        elif state.game_state == state.won:
            reset_button.set_image("images/flagged.png")
            cur_time = int(time() - start_time)
            if highscores.qualifies(cur_difficulty[0], cur_time):
                name = tkSimpleDialog.askstring("Enter name", "New high score! Enter name:", initialvalue = "Anonymous", parent=root)
                if name:
                    highscores.update_scores(cur_difficulty[0], name, cur_time)
                

def on_idle():
    if state.game_state == state.in_progress:
        cur_time = int(time() - start_time)
        timer.set(min(cur_time, 999))
    root.after(100, on_idle)

def new_game():
    global state_view, state, start_time
    if state_view is not None:
        state_view.grid_forget()
        state.unbind(state_view.state_changed) #bit of an encapsulation violation here...
    state = State(*cur_difficulty[1:])
    state.bind(state_changed)
    state_view = StateView(root, state)
    state_view.grid(row=1, column=0)
    reset_button.set_image("images/covered.png")
    mine_counter.set(state.num_mines)
    timer.set(None)

def show_settings():
    global cur_difficulty
    window = SettingsWindow(root, cur_difficulty)
    window.grab_set()
    root.wait_window(window)
    if window.setting_chosen != None:
        cur_difficulty = window.setting_chosen
        new_game()

def show_high_scores():
    window = highscores.HighScoreWindow(root)
    window.grab_set()
    root.wait_window(window)

import random

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
gamemenu.add_command(label = "High Scores", command=show_high_scores)
gamemenu.add_command(label = "Exit", command=root.quit)

action_bar = Frame(root)
action_bar.grid_columnconfigure(0, weight=1)
action_bar.grid_columnconfigure(1, weight=1)
action_bar.grid_columnconfigure(2, weight=1)

timer = NumberDisplay(action_bar)
timer.grid(row=0, column=0, sticky="w")

reset_button = ImageButton(action_bar, "images/covered.png", command=new_game)
reset_button.grid(row=0, column=1)

mine_counter = NumberDisplay(action_bar)
mine_counter.grid(row=0,column=2, sticky="e")

action_bar.grid(row=0, column=0, sticky="we")


state = None
state_view = None
start_time = None
new_game()

root.after(100, on_idle)
root.mainloop()