from imageGrid import ImageGrid

class StateView(ImageGrid):
    def __init__(self, root, state, **kwargs):
        self.state = state
        
        kwargs["names"] = {name: "images/{}.png".format(name) for name in "covered uncovered 1 2 3 4 5 6 7 8 flagged unsure".split()}
        kwargs["rows"] = state.height
        kwargs["cols"] = state.width
        kwargs["default"] = "covered"
        ImageGrid.__init__(self, root, **kwargs)

        self.bind_cell(self.clicked)
    def clicked(self, event, pos, button, state, last_down_pos):
        if state == "up":
            if not (self.in_range(pos) and pos == last_down_pos):
                return
            if self.state.cell_states[pos] == self.state.covered:
                for cell in self.state.get_group(pos):
                    self.state.cell_states[cell] = self.state.uncovered
                    self.set_image(cell, self.state.get_name(cell))