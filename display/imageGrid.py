from Tkinter import *
from PIL import Image, ImageTk
from geometry import Point

class ImageGrid(Canvas):
    """
        keyword arguments:
        names - a dictionary whose keys are strings and whose values are filenames.
        rows, cols - positive integers.
        margin - a non-negative integer. default is 5.
        default - a key from names. If none is supplied, the lexicographically first name will be chosen.
    """
    def __init__(self, root, **kwargs):

        #collection of ImageTk.PhotoImages.
        #shouldn't be accessed anywhere; we only need it to prevent premature garbage collection.
        self.photo_refs = []

        names = kwargs.pop("names")
        self.images_by_name = {name: self.load_image(filename) for name, filename in names.iteritems()}
        self.image_height = max(image.height() for image in self.images_by_name.itervalues())
        self.image_width = max(image.width() for image in self.images_by_name.itervalues())

        default_image = kwargs.pop("default", sorted(self.images_by_name.iterkeys())[0])
        
        self.rows = kwargs.pop("rows")
        self.cols = kwargs.pop("cols")
        #tkinter does weird stuff with the edges of a Canvas, so we have to fudge the margins to compensate.
        self.right_margin = kwargs.pop("margin", 5) - 2
        self.left_margin = self.right_margin + 4
        
        kwargs["width"]  = self.cols * self.image_width  + self.left_margin + self.right_margin
        kwargs["height"] = self.rows * self.image_height + self.left_margin + self.right_margin
        Canvas.__init__(self, root, **kwargs)

        self.create_rectangle(-10,-10, 1000, 1000, fill="#AAFFAA")


        self.ids = {}
        self.images = {}
        for i in range(self.cols):
            for j in range(self.rows):
                x = self.left_margin + i * self.image_width
                y = self.left_margin + j * self.image_height
                cell = Point(i,j)
                self.images[cell] = default_image
                self.ids[cell] = self.create_image(x,y, image=self.images_by_name[default_image], anchor="nw")

        self.callbacks = []
        self.button_pressed_position = {key: None for key in ["left", "right"]}
        self.bind("<ButtonPress-1>"  , lambda event: self.button_event(event, "left" , "down"))
        self.bind("<ButtonRelease-1>", lambda event: self.button_event(event, "left" , "up"  ))
        self.bind("<ButtonPress-3>"  , lambda event: self.button_event(event, "right", "down"))
        self.bind("<ButtonRelease-3>", lambda event: self.button_event(event, "right", "up"  ))

    def button_event(self, event, button, state):
        row = (event.y - self.left_margin) / self.image_height
        col = (event.x - self.left_margin) / self.image_width
        cur = Point(col, row)
        if state == "down":
            self.button_pressed_position[button] = Point(col, row)
        
        for callback in self.callbacks:
            callback(event, cur, button, state, self.button_pressed_position[button])

    """
        registers a callback with the class, which triggers on mouse movement.
        callback will be executed with these parameters.
        event - the raw Tkinter event.
        pos - a (col, row) tuple indicating which image was pressed.
        button - "left" or "right"
        state - "up" or "down"
        last_down_pos - a (col, row) tuple indicating which cell the mouse button was pressed down on. equal to `pos` for down clicks.
    """
    def bind_cell(self, callback):
        self.callbacks.append(callback)

    def get_image(self, p):
        return self.images[p]

    def set_image(self, p,name):
        id = self.ids[p]
        self.itemconfig(id, image = self.images_by_name[name])
        self.images[p] = name

    def in_range(self, p):
        return 0 <= p.x < self.cols and 0 <= p.y < self.rows

    def load_image(self, filename):
        if filename.endswith(".gif"):
            return PhotoImage(file=filename)
        else:
            image = Image.open(filename)
            photo = ImageTk.PhotoImage(image)
            self.photo_refs.append(photo)
            return photo