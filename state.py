from matrix import Matrix, neighbors
from geometry import Point
import random

class State:
    covered, uncovered, flagged, unsure = 1,2,3,4
    def __init__(self, width, height, num_mines):
        assert num_mines <= width*height
        self.mines = Matrix(width, height)
        candidate_positions = [Point(x,y) for x in range(width) for y in range(height)]
        for location in random.sample(candidate_positions, num_mines):
            self.mines[location] = True
        self.cell_states = Matrix(width, height, State.covered)
    #returns the number of mines in adjacent cells
    def count(self, p):
        return sum(1 for cell in self.mines.neighbors_in_range(p) if self.mines[cell])

    #returns a collection of the cells that would be uncovered if `p` was uncovered.
    #cells with a count of 0 uncover their neighbors in a chain reaction.
    def get_group(self, p):
        to_visit = set()
        to_visit.add(p)
        seen = set()
        if self.cell_states[p] in (State.uncovered, State.flagged):
            return seen

        while to_visit:
            cur = to_visit.pop()
            seen.add(cur)
            if self.count(cur) == 0:
                for neighbor in self.mines.neighbors_in_range(cur):
                    if neighbor not in seen and self.cell_states[neighbor] == State.covered:
                        to_visit.add(neighbor)
        return seen
