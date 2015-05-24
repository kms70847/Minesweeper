from matrix import Matrix, neighbors
from broadcaster import Broadcaster
from geometry import Point
import random

class State(Broadcaster):
    """Representation of the game state of Minesweeper."""

    covered, uncovered, flagged, unsure = 1,2,3,4
    won, lost, not_started, in_progress = 1,2,3,4

    def __init__(self, width, height, num_mines):
        """
        Positional arguments:
        width: the width of the game field.
        height: the height of the game field.
        num_mines: the number of mines in the game field.
        """

        assert num_mines <= width*height
        Broadcaster.__init__(self)
        self.width, self.height = width, height
        self.num_mines = num_mines
        self.mines = Matrix(width, height)
        candidate_positions = [Point(x,y) for x in range(width) for y in range(height)]
        for location in random.sample(candidate_positions, num_mines):
            self.mines[location] = True
        self.cell_states = Matrix(width, height, State.covered)
        self.cell_state_counts = {State.covered: width*height, State.uncovered: 0, State.flagged: 0, State.unsure: 0}
        self.game_state = State.not_started

    def neighboring_mine_count(self, p):
        """Return the number of mines in adjacent cells."""

        return sum(1 for cell in self.mines.neighbors_in_range(p) if self.mines[cell])

    def neighboring_state_count(self, p, state):
        """Return the number of adjacent cells that have a particular state."""

        return sum(1 for cell in self.cell_states.neighbors_in_range(p) if self.cell_states[cell] == state)

    def state_count(self, state):
        """Return the number of cells in the whole field that have a particular state."""

        return self.cell_state_counts[state]

    def get_group(self, p):
        """
        Return a collection of the cells that would be uncovered if `p` was uncovered.
        Cells with a count of 0 uncover their neighbors in a chain reaction.
        """

        to_visit = set()
        to_visit.add(p)
        seen = set()
        if self.cell_states[p] in (State.uncovered, State.flagged):
            return seen

        if self.mines[p]:
            seen.add(p)
            return seen

        while to_visit:
            cur = to_visit.pop()
            seen.add(cur)
            if self.neighboring_mine_count(cur) == 0:
                for neighbor in self.mines.neighbors_in_range(cur):
                    if neighbor not in seen and self.cell_states[neighbor] == State.covered:
                        to_visit.add(neighbor)
        return seen

    def get_name(self, p):
        """
        Return a string representative of the state of the cell.
        Possible values are mine, uncovered, covered, flagged, unsure, or a number between 1 and 8 inclusive.
        """

        if self.cell_states[p] == State.uncovered:
            if self.mines[p]:
                return "mine"
            else:
                if self.neighboring_mine_count(p) == 0:
                    return "uncovered"
                else:
                    return str(self.neighboring_mine_count(p))
        else:
            return {State.covered: "covered", State.flagged: "flagged", State.unsure: "unsure"}[self.cell_states[p]]

    def iter_cells(self):
        """Yield each Point corresponding to a cell on the field."""

        for i in range(self.width):
            for j in range(self.height):
                yield Point(i,j)

    def set_state(self, p, state):
        """
        Set the state of the cell.
        (Whether a cell has a mine can't be set with this method; modify State.mines for that.)
        """

        old_state = self.cell_states[p]
        self.cell_state_counts[old_state] -= 1
        self.cell_state_counts[state] += 1
        self.cell_states[p] = state

    def uncover(self, p):
        """
        Uncover the cell, if possible (i.e. it's in range and not flagged.
        This can trigger game loss/win events, and uncover multiple cells in a chain reaction.
        """

        #don't let user die on his first move
        if self.mines[p] and self.game_state == State.not_started:
            #move mine to first open spot you can find
            for candidate_p in self.iter_cells():
                if p != candidate_p and not self.mines[candidate_p]:
                    self.mines[p] = False
                    self.mines[candidate_p] = True
                    break

        #can't click on flags or question marks
        if self.cell_states[p] not in {State.covered, State.unsure}:
            return

        to_uncover = self.get_group(p)
        for cell in to_uncover:
            self.set_state(cell, State.uncovered)

        #broadcast events
        if self.game_state == State.not_started:
            self.game_state = State.in_progress
            self.broadcast("started")
        self.broadcast("uncovered", to_uncover)
        if self.mines[p]:
            self.game_state = State.lost
            self.broadcast("game_ended")
        else:
            num_uncovered = sum(1 for cell in self.iter_cells() if self.cell_states[cell] != State.uncovered)
            if num_uncovered == self.num_mines:
                self.game_state = State.won
                self.broadcast("game_ended")

    def mark(self, p, state):
        """Like `set_state`, but triggers a "marked" event."""

        assert self.cell_states[p] != State.uncovered
        assert state in {State.flagged, State.unsure, State.covered}
        self.set_state(p, state)
        self.broadcast("marked", p)