from imageGrid import ImageGrid


def after(seq, item):
    """
    returns the element in `seq` that appears after `item`.
    wraps around to the beginning of the list if necessary.
    """
    idx = seq.index(item)
    idx = (idx + 1) % len(seq)
    return seq[idx]


class StateView(ImageGrid):
    """Tkinter widget that represents the main field of play for the game."""

    def __init__(self, root, state, **kwargs):
        """Positional arguments:
        root - the parent window of this widget.
        state - the State object representing the game.
        """

        self.state = state

        kwargs["names"] = {name: "images/{}.png".format(name) for name in "covered uncovered 1 2 3 4 5 6 7 8 flagged unsure mine".split()}
        kwargs["rows"] = state.height
        kwargs["cols"] = state.width
        kwargs["default"] = "covered"
        ImageGrid.__init__(self, root, **kwargs)

        """legal values: None, "Normal", "Smart" """
        self.click_mode = None

        """Cells that look uncovered because the user is holding down the mouse button"""
        self.depressed_cells = set()

        self.bind_cell("button", self.clicked)
        self.bind_cell("cursor_moved", self.update_depressed_images)

        self.state.bind(self.state_changed)

    def state_changed(self, event, *args):
        """Callback that fires whenever the game state changes."""

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
        """
        Attempt to toggle the state of the cell at `pos` between covered/flagged/unsure.
        Do nothing if the cell is out of range or uncovered.
        """

        if not self.in_range(pos):
            return
        state = self.state.cell_states[pos]
        valid_states = [self.state.covered, self.state.flagged, self.state.unsure]
        if state not in valid_states:
            return
        new_state = after(valid_states, state)
        self.state.mark(pos, new_state)

    def try_click(self, pos):
        """
        Attempt to uncover the cell at `pos`.
        Do nothing if the cell is out of range.
        """

        if not self.in_range(pos):
            return
        self.state.uncover(pos)

    def try_smart_click(self, pos):
        """Uncover all covered neighboring cells, if it can be trivially deduced that none of them are mines."""

        if self.state.cell_states[pos] == self.state.uncovered:
            flagged_neighbor_count = self.state.neighboring_state_count(pos, self.state.flagged)
            if self.state.neighboring_mine_count(pos) <= flagged_neighbor_count:
                for cell in self.state.cell_states.neighbors_in_range(pos):
                    self.state.uncover(cell)

    def clicked(self, event, pos, button, state, last_down_pos):
        """
        Callback that fires whenever the user clicks on this widget.
        See `ImageGrid.bind_cell` for a description of positional parameters.
        """

        if button == "middle":
            return
        if self.state.game_state not in {self.state.in_progress, self.state.not_started}:
            return

        """Determine current and previous state for our subsequent DFA."""
        cur_state = sorted(b for b, v in self.button_states.items() if b != "middle" and v == "down")
        prev_state = cur_state[:]
        if state == "down":
            prev_state.remove(button)
        else:
            prev_state.append(button)
        prev_state.sort()
        """Collections should contain nothing but left or right."""
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
        """Update the representation of cells that appear depressed because the user is holding down the left mouse button."""

        def restore(cell):
            """Restore the cell to its normal representation."""

            self.set_image(cell, self.state.get_name(cell))

        def iter_3x3(pos):
            """Iterate over the cell and its neighbors."""

            for cell in self.state.mines.neighbors_in_range(pos):
                yield cell
            yield pos

        def may_be_depressed(pos):
            """Return True if the cell is allowed to be depressed."""

            return self.state.get_name(pos) in {"covered", "unsure"}

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
        if self.state.game_state in {self.state.in_progress, self.state.not_started}:
            for cell in to_depress - self.depressed_cells:
                self.set_image(cell, "uncovered")
        self.depressed_cells = to_depress
