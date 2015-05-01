from Tkinter import *

from stateView import StateView

import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from state import State


state = State(10, 10, 5)
root = Tk()
x = StateView(root, state)
x.pack()
root.mainloop()