from imageGrid import ImageGrid

class StateView(ImageGrid):
    def __init__(self, root, state, **kwargs):
        self.state = state
        
        kwargs["names"] = {
            "covered": "images/img.png",
            "uncovered": "images/img2.gif"
        }
        kwargs["rows"] = state.height
        kwargs["cols"] = state.width
        kwargs["default"] = "covered"
        ImageGrid.__init__(self, root, **kwargs)

        self.bind_cell(self.clicked)
    def clicked(self, event, pos, button, state, last_down_pos):
        if state == "up":
            if not (self.in_range(pos) and pos == last_down_pos):
                return
            print "clicked at {}".format(pos)