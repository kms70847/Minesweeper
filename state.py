from matrix import Matrix, neighbors
from broadcaster import Broadcaster
from geometry import Point
import random

class State(Broadcaster):
    covered, uncovered, flagged, unsure = 1,2,3,4
    won, lost, in_progress = 1,2,3
    def __init__(self, width, height, num_mines):
        assert num_mines <= width*height
        Broadcaster.__init__(self)
        self.width, self.height = width, height
        self.num_mines = num_mines
        self.mines = Matrix(width, height)
        candidate_positions = [Point(x,y) for x in range(width) for y in range(height)]
        for location in random.sample(candidate_positions, num_mines):
            self.mines[location] = True
        self.cell_states = Matrix(width, height, State.covered)
        self.game_state = State.in_progress
    #returns the number of mines in adjacent cells
    def count(self, p):
        return sum(1 for cell in self.mines.neighbors_in_range(p) if self.mines[cell])

    def state_count(self, p, state):
        return sum(1 for cell in self.cell_states.neighbors_in_range(p) if self.cell_states[cell] == state)

    #returns a collection of the cells that would be uncovered if `p` was uncovered.
    #cells with a count of 0 uncover their neighbors in a chain reaction.
    def get_group(self, p):
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
            if self.count(cur) == 0:
                for neighbor in self.mines.neighbors_in_range(cur):
                    if neighbor not in seen and self.cell_states[neighbor] == State.covered:
                        to_visit.add(neighbor)
        return seen

    def get_name(self, p):
        if self.cell_states[p] == State.uncovered:
            if self.mines[p]:
                return "mine"
            else:
                if self.count(p) == 0:
                    return "uncovered"
                else:
                    return str(self.count(p))
        else:
            return {State.covered: "covered", State.flagged: "flagged", State.unsure: "unsure"}[self.cell_states[p]]

    def iter_cells(self):
        for i in range(self.width):
            for j in range(self.height):
                yield Point(i,j)

    def uncover(self, p):
        if self.cell_states[p] not in {State.covered, State.unsure}:
            return
        to_uncover = self.get_group(p)
        for cell in to_uncover:
            self.cell_states[cell] = State.uncovered
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
        assert self.cell_states[p] != State.uncovered
        assert state in {State.flagged, State.unsure, State.covered}
        self.cell_states[p] = state
        self.broadcast("marked", p)