from Tkinter import *
from imageGrid import ImageGrid

def clicked(event, pos, button, state, last_down_pos):
    #print pos, button, state, last_down_pos
    if button == "left":
        if state == "down":
            x.set_image(pos[0], pos[1], "uncovered")
        elif state == "up":
            if pos != last_down_pos:
                #user moved cursor out of cell before unpressing. This means he wants to cancel.
                x.set_image(last_down_pos[0], last_down_pos[1], "covered")
            else:
                print "Permanently uncovering {} {}...".format(*pos)

root = Tk()

names = {"covered": "img.png", "uncovered": "img2.gif"}
x = ImageGrid(root, rows=10, cols=10, names=names, default="covered")
x.pack()
x.bind_cell(clicked)

root.mainloop()