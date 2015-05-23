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

        #legal values: None, "Normal", "Smart"
        self.click_mode = None

        #cells that look uncovered because the user is holding down the mouse button
        self.depressed_cells = set()

        self.bind_cell("button", self.clicked)
        self.bind_cell("cursor_moved", self.update_depressed_images)

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

    def try_mark(self, pos):
        if not self.in_range(pos):
            return
        state = self.state.cell_states[pos]
        valid_states = [self.state.covered, self.state.flagged, self.state.unsure]
        if state not in valid_states: 
            return
        new_state = after(valid_states, state)
        self.state.mark(pos, new_state)

    def try_click(self, pos):
        if not self.in_range(pos):
            return
        self.state.uncover(pos)

    def try_smart_click(self, pos):
        if self.state.cell_states[pos] == self.state.uncovered:
            flagged_neighbor_count = self.state.neighboring_state_count(pos, self.state.flagged)
            if self.state.neighboring_mine_count(pos) <= flagged_neighbor_count:
                for cell in self.state.cell_states.neighbors_in_range(pos):
                    self.state.uncover(cell)

    def clicked(self, event, pos, button, state, last_down_pos):
        if button == "middle": return

        #determine current and previous state for our subsequent DFA
        cur_state = sorted(b for b,v in self.button_states.iteritems() if b != "middle" and v == "down")
        prev_state = cur_state[:]
        if state == "down":
            prev_state.remove(button)
        else:
            prev_state.append(button)
        prev_state.sort()
        #collections should contain nothing but left or right
        assert all(x in ["left", "right"] for seq in [cur_state, prev_state] for x in seq)

        if prev_state == [] and cur_state == ['left']:
            self.click_mode = "Normal"
            self.update_depressed_images(pos, pos)
        elif prev_state == [] and cur_state == ['right']:
            self.try_mark(pos)
        elif prev_state == ['left'] and cur_state == []:
            if self.click_mode == "Normal":
                self.try_click(pos)
            elif self.click_mode == "Smart":
                self.try_smart_click(pos)
            else:
                raise Exception("Unexpected click mode {}".format(self.click_mode))
            self.click_mode = None
            self.update_depressed_images(pos, pos)
        elif cur_state == ['left', 'right']:
            self.click_mode = "Smart"
            self.update_depressed_images(pos, pos)
        elif prev_state == ['left', 'right'] and cur_state == ['left']:
            self.try_smart_click(pos)
        elif prev_state == ['left', 'right'] and cur_state == ['right']:
            self.try_smart_click(pos)
            self.click_mode = None
            self.update_depressed_images(pos, pos)
        elif prev_state == ['right'] and cur_state == []:
            pass
        else:
            raise Exception("Unexpected state change from {} to {}".format(prev_state, cur_state))

    def update_depressed_images(self, pos, old_pos):
        def restore(cell):
            self.set_image(cell, self.state.get_name(cell))
        def iter_3x3(pos):
            for cell in self.state.mines.neighbors_in_range(pos):
                yield cell
            yield pos

        may_be_depressed = lambda pos: self.state.get_name(pos) in {"covered", "unsure"}

        to_depress = set()
        if self.click_mode == "Normal":
            if self.in_range(pos) and may_be_depressed(pos):
                to_depress.add(pos)
        elif self.click_mode == "Smart":
            for cell in iter_3x3(pos):
                if may_be_depressed(cell):
                    to_depress.add(cell)

        to_unpress = self.depressed_cells - to_depress
        for cell in to_unpress:
            restore(cell)
        for cell in to_depress - self.depressed_cells:
            self.set_image(cell, "uncovered")
        self.depressed_cells = to_depress