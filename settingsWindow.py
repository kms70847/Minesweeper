from tkinter_ex import *


class StrictEntry(Entry):
    """
    Abstract base class for an extended Entry widget that performs per-keystroke validation.
    Subclasses should override `is_valid` with their own custom behavior.
    """

    def __init__(self, root, *args, **kwargs):
        valid_command = root.register(self.is_valid)
        Entry.__init__(self, root, validate="all", validatecommand=(valid_command, '%P'), *args, **kwargs)

    def is_valid(self, text):
        return True


class DigitEntry(StrictEntry):
    """Entry that accepts only integers, and only as many digits as its width"""
    def __init__(self, *args, **kwargs):
        """
        Arguments are anything you would pass to an Entry, plus...
        Keyword arguments:
        value: the value that will appear in the text field. Default 0.
        """

        self.var = StringVar()
        self.var.set(kwargs.pop("value", 0))
        StrictEntry.__init__(self, textvariable=self.var, *args, **kwargs)

    def is_valid(self, text):
        return text == "" or (text.isdigit() and len(text) <= self.cget("width"))

    def get(self):
        """Return the contents of the Entry. Value will be an integer, or None if there are no contents."""

        text = self.var.get()
        if not text:
            return None
        else:
            return int(text)


class SettingsWindow(Toplevel):
    """Pop-up window that lets the user configure settings for the game. I.e., the difficulty level."""

    def __init__(self, root, cur_setting, *args, **kwargs):
        Toplevel.__init__(self, root, *args, **kwargs)
        self.resizable(0, 0)
        self.title("Settings")

        self.settings = (
            ("Beginner", 9, 9, 10),
            ("Intermediate", 16, 16, 40),
            ("Advanced", 30, 16, 99)
        )

        self.v = IntVar()
        for idx, setting in enumerate(self.settings):
            text = "{} - {}x{}, {} mines".format(*setting)
            Radiobutton(self, text=text, variable=self.v, value=idx).pack(anchor="w")
            if cur_setting[0] == setting[0]:
                self.v.set(idx)

        custom_frame = Frame(self)
        Radiobutton(custom_frame, text="Custom - width: ", variable=self.v, value=len(self.settings) + 1).pack(side=LEFT)
        self.custom_width = DigitEntry(custom_frame, width=3, value=cur_setting[1])
        self.custom_width.pack(side=LEFT)
        Label(custom_frame, text=" height: ").pack(side=LEFT)
        self.custom_height = DigitEntry(custom_frame, width=3, value=cur_setting[2])
        self.custom_height.pack(side=LEFT)
        Label(custom_frame, text=" mines: ").pack(side=LEFT)
        self.custom_mines = DigitEntry(custom_frame, width=3, value=cur_setting[3])
        self.custom_mines.pack(side=LEFT)

        custom_frame.pack(padx=(0, 10))

        if cur_setting[0] == "Custom":
            self.v.set(len(self.settings) + 1)

        button_row = Frame(self)
        Button(button_row, text="OK", width=10, command=self.ok_clicked).pack(side=LEFT, padx=10, pady=10)
        Button(button_row, text="Cancel", width=10, command=self.destroy).pack(side=RIGHT, padx=10, pady=10)
        button_row.pack()

        self.setting_chosen = None

    def ok_clicked(self):
        """
        Callback that triggers when the OK button is clicked.
        If user input is valid, update `setting_chosen` with the chosen setting and destroy this window.
        """

        if self.v.get() < len(self.settings):
            self.setting_chosen = self.settings[self.v.get()]
        else:
            width, height, mines = self.custom_width.get(), self.custom_height.get(), self.custom_mines.get()
            if width < 1 or height < 1 or width > 40 or height > 40 or mines > width * height:
                return
            self.setting_chosen = ("Custom", width, height, mines)
        self.destroy()
