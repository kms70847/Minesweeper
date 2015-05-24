from tkinter_ex import *
from PIL import Image, ImageTk
from geometry import Point


class ImageGrid(Canvas):
    """Tkinter widget that displays images in a grid."""

    def __init__(self, root, **kwargs):
        """
        keyword arguments:
        names - a {string: filename} dictionary.
        rows, cols - positive integers.
        margin - a non-negative integer. default is 0.
        default - a key from names. If none is supplied,
            the lexicographically first name will be chosen.
        """

        """
        collection of ImageTk.PhotoImages.
        shouldn't be accessed anywhere;
        we only need it to prevent premature garbage collection.
        """
        self.photo_refs = []

        names = kwargs.pop("names")
        self.images_by_name = {name: self.load_image(filename) for name, filename in names.items()}
        self.image_height = max(image.height() for image in self.images_by_name.values())
        self.image_width = max(image.width() for image in self.images_by_name.values())

        default_image = kwargs.pop("default", sorted(self.images_by_name.keys())[0])

        self.rows = kwargs.pop("rows")
        self.cols = kwargs.pop("cols")

        """tkinter does weird stuff with the edges of a Canvas, so we have to fudge the margins to compensate."""
        self.right_margin = kwargs.pop("margin", 0) - 2
        self.left_margin = self.right_margin + 4

        kwargs["width"] = self.cols * self.image_width + self.left_margin + self.right_margin
        kwargs["height"] = self.rows * self.image_height + self.left_margin + self.right_margin
        Canvas.__init__(self, root, **kwargs)

        self.ids = {}
        self.images = {}
        for i in range(self.cols):
            for j in range(self.rows):
                x = self.left_margin + i * self.image_width
                y = self.left_margin + j * self.image_height
                cell = Point(i, j)
                self.images[cell] = default_image
                self.ids[cell] = self.create_image(x, y, image=self.images_by_name[default_image], anchor="nw")

        self.callbacks = {"button": [], "cursor_moved": []}
        self.button_pressed_position = {key: None for key in ["left", "right", "middle"]}
        self.button_states = {key: "up" for key in ["left", "right", "middle"]}
        self.bind("<ButtonPress-1>", lambda event: self.button_event(event, "left", "down"))
        self.bind("<ButtonRelease-1>", lambda event: self.button_event(event, "left", "up"))
        self.bind("<ButtonPress-2>", lambda event: self.button_event(event, "middle", "down"))
        self.bind("<ButtonRelease-2>", lambda event: self.button_event(event, "middle", "up"))
        self.bind("<ButtonPress-3>", lambda event: self.button_event(event, "right", "down"))
        self.bind("<ButtonRelease-3>", lambda event: self.button_event(event, "right", "up"))

        self.cursor_position = None
        self.bind("<Motion>", self.cursor_moved_event)

    def button_event(self, event, button, state):
        """
        Callback that triggers when the user clicks or un-clicks.
        Alert listeners that registered using `bind_cell`.
        """

        row = (event.y - self.left_margin) / self.image_height
        col = (event.x - self.left_margin) / self.image_width
        cur = Point(col, row).map(int)
        if state == "down":
            self.button_pressed_position[button] = Point(col, row)
            self.button_states[button] = "down"
        else:
            self.button_states[button] = "up"

        for callback in self.callbacks["button"]:
            callback(event, cur, button, state, self.button_pressed_position[button])

    def cursor_moved_event(self, event):
        """
        Callback that triggers when the user moves the mouse.
        Alert listeners that registered using `bind_cell`.
        """

        row = (event.y - self.left_margin) / self.image_height
        col = (event.x - self.left_margin) / self.image_width
        cur = Point(col, row).map(int)
        if self.cursor_position != cur:
            old_position = self.cursor_position
            self.cursor_position = cur
            for callback in self.callbacks["cursor_moved"]:
                callback(self.cursor_position, old_position)

    def bind_cell(self, event_name, callback):
        """
        Register a callback with the class, which triggers on mouse activity.

        If event_name is "button", event triggers when a mouse button is pressed or released.
        Callback will be executed with these parameters.
        event - the raw Tkinter event.
        pos - a (col, row) tuple indicating which image was pressed.
        button - "left" or "right"
        state - "up" or "down"
        last_down_pos - a (col, row) tuple indicating which cell the mouse button was pressed down on. equal to `pos` for down clicks.

        If event_name is "cursor_moved", event triggers when the cursor moves into a new cell of the grid, including out-of-bounds ones.
        Callback will be executed with these parameters.
        position - the cell the cursor is in now.
        old_position - the cell the cursor used to be in.
        """

        assert event_name in {"button", "cursor_moved"}
        self.callbacks.setdefault(event_name, []).append(callback)

    def get_image(self, p):
        """Return the name of the image currently displayed at cell `p`."""

        return self.images[p]

    def set_image(self, p, name):
        """Update the cell at `p` to display the image associated to `name`."""

        id = self.ids[p]
        self.itemconfig(id, image=self.images_by_name[name])
        self.images[p] = name

    def in_range(self, p):
        """Return True if `p` lies within the bounds of the grid."""

        return 0 <= p.x < self.cols and 0 <= p.y < self.rows

    def load_image(self, filename):
        """
        Return a PhotoImage instance for the given filename.
        A reference will be kept indefinitely to prevent premature garbage collection.
        """

        if filename.endswith(".gif"):
            return PhotoImage(file=filename)
        else:
            image = Image.open(filename)
            photo = ImageTk.PhotoImage(image)
            self.photo_refs.append(photo)
            return photo
