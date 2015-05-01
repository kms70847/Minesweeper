from Tkinter import *

from stateView import StateView

import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from state import State

#beginner: 9,9,10
#intermediate: 16, 16, 40
#advanced: 16, 30, 99
state = State(16, 16, 40)
root = Tk()
x = StateView(root, state)
x.pack()
root.mainloop()