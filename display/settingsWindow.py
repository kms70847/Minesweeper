from Tkinter import *

"""Abstract base class for an extended Entry widget that performs per-keystroke validation.
subclasses should override `is_valid` with their own custom behavior.
"""
class StrictEntry(Entry):
    def __init__(self, root, *args, **kwargs):
        valid_command = root.register(self.is_valid)
        Entry.__init__(self, root, validate="all", validatecommand=(valid_command, '%P'), *args, **kwargs)
    def is_valid(self, text):
        return True

"""Entry that accepts only integers, and only as many digits as its width"""
class DigitEntry(StrictEntry):
    def __init__(self, *args, **kwargs):
        self.var = StringVar()
        self.var.set(kwargs.pop("value", 0))
        StrictEntry.__init__(self, textvariable=self.var, *args, **kwargs)
    def is_valid(self, text):
        return text == "" or (text.isdigit() and len(text) <= self.cget("width"))
    def get(self):
        text = self.var.get()
        if not text: return None
        else: return int(text)

class SettingsWindow(Toplevel):
    def __init__(self, root, cur_setting, *args, **kwargs):
        Toplevel.__init__(self, root, *args, **kwargs)
        self.resizable(0,0)
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
        Radiobutton(custom_frame, text="Custom - width: ", variable=self.v, value=len(self.settings)+1).pack(side=LEFT)
        self.custom_width = DigitEntry(custom_frame, width=3, value=cur_setting[1])
        self.custom_width.pack(side=LEFT)
        Label(custom_frame, text=" height: ").pack(side=LEFT)
        self.custom_height = DigitEntry(custom_frame, width=3, value=cur_setting[2])
        self.custom_height.pack(side=LEFT)
        Label(custom_frame, text=" mines: ").pack(side=LEFT)
        self.custom_mines = DigitEntry(custom_frame, width=3, value=cur_setting[3])
        self.custom_mines.pack(side=LEFT)

        custom_frame.pack(padx=(0,10))

        button_row = Frame(self)
        Button(button_row, text="OK", width=10, command=self.ok_clicked).pack(side=LEFT, padx=10, pady=10)
        Button(button_row, text="Cancel", width=10, command=self.cancel_clicked).pack(side=RIGHT, padx=10, pady=10)
        button_row.pack()

        self.setting_chosen = None

    def ok_clicked(self):
        if self.v.get() < len(self.settings):
            self.setting_chosen = self.settings[self.v.get()]
        else:
            self.setting_chosen = ("Custom", self.custom_width.get(), self.custom_height.get(), self.custom_mines.get())
        self.destroy()

    def cancel_clicked(self):
        self.destroy()
