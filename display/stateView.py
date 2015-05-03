from imageGrid import ImageGrid

"""
returns the element in `seq` that appears after `item`.
wraps around to the beginning of the list if necessary.
"""
def after(seq, item):
    idx = seq.index(item)
    idx = (idx + 1) % len(seq)
    return seq[idx]

class StateView(ImageGrid):
    def __init__(self, root, state, **kwargs):
        self.state = state
        
        kwargs["names"] = {name: "images/{}.png".format(name) for name in "covered uncovered 1 2 3 4 5 6 7 8 flagged unsure mine".split()}
        kwargs["rows"] = state.height
        kwargs["cols"] = state.width
        kwargs["default"] = "covered"
        ImageGrid.__init__(self, root, **kwargs)

        self.bind_cell(self.clicked)

        self.state.bind(self.state_changed)

    def state_changed(self, event, *args):
        if event == "uncovered":
            cells = args[0]
            for cell in cells:
                self.set_image(cell, self.state.get_name(cell))
        elif event == "marked":
            cell = args[0]
            self.set_image(cell, self.state.get_name(cell))
        elif event == "game_ended":
            if self.state.game_state == self.state.lost:
                for p in self.state.iter_cells():
                    if self.state.mines[p]:
                        self.set_image(p, "mine")

    def clicked(self, event, pos, button, state, last_down_pos):
        if self.state.game_state != self.state.in_progress:
            return
        if button == "left" and state == "up":
            if not (self.in_range(pos) and pos == last_down_pos):
                return
            self.state.uncover(pos)
        if button == "right" and state == "down":
            if not self.in_range(pos):
                return
            state = self.state.cell_states[pos]
            valid_states = [self.state.covered, self.state.flagged, self.state.unsure]
            if state not in valid_states: 
                return
            new_state = after(valid_states, state)
            self.state.mark(pos, new_state)
        if button == "middle" and state == "up":
            if not (self.in_range(pos) and pos == last_down_pos):
                return
            if self.state.cell_states[pos] == self.state.uncovered:
                flagged_neighbor_count = self.state.state_count(pos, self.state.flagged)
                if self.state.count(pos) <= flagged_neighbor_count:
                    for cell in self.state.cell_states.neighbors_in_range(pos):
                        self.state.uncover(cell)