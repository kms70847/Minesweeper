#compatibility hack so I don't have to put try-catches in the import sections of my actual source files, just to get cross-version compatibility.

try:
    from Tkinter import *
except:
    from tkinter import *

try:
    from tkSimpleDialog import *
except:
    from tkinter.simpledialog import *