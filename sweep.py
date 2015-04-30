from geometry import Point
import random

def neighbors(p):
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0: continue
            yield p + Point(dx, dy)

class Matrix:
    def __init__(self, width, height, default=None):
        self.width = width
        self.height = height
        self.data = [[default for _ in range(width)] for __ in range(height)]
    def in_range(self, p):
        return (0 <= p.x < self.width) and (0 <= p.y < self.height)
    def set(self, p, value):
        assert self.in_range(p)
        self.data[p.y][p.x] = value
    def get(self, p):
        assert self.in_range(p)
        return self.data[p.y][p.x]
    def neighbors_in_range(self, p):
        for neighbor in neighbors(p):
            if self.in_range(neighbor):
                yield neighbor
    def __setitem__(self, p, value):
        assert isinstance(p, Point)
        self.set(p, value)
    def __getitem__(self, p):
        assert isinstance(p, Point)
        return self.get(p)

covered, uncovered, flagged, unsure = 1,2,3,4

class State:
    def __init__(self, width, height, num_mines):
        assert num_mines <= width*height
        self.mines = Matrix(width, height)
        candidate_positions = [Point(x,y) for x in range(width) for y in range(height)]
        for location in random.sample(candidate_positions, num_mines):
            self.mines[location] = True
        self.cell_states = Matrix(width, height, covered)
    #returns the number of mines in adjacent cells
    def count(self, p):
        return sum(1 for cell in self.mines.neighbors_in_range(p) if self.mines[cell])

    #returns a collection of the cells that would be uncovered if `p` was uncovered.
    #cells with a count of 0 uncover their neighbors in a chain reaction.
    def get_group(self, p):
        to_visit = set()
        to_visit.add(p)
        seen = set()
        if self.cell_states[p] in (uncovered, flagged):
            return seen

        while to_visit:
            cur = to_visit.pop()
            seen.add(cur)
            if self.count(cur) == 0:
                for neighbor in self.mines.neighbors_in_range(cur):
                    if neighbor not in seen and self.cell_states[neighbor] == covered:
                        to_visit.add(neighbor)
        return seen
        

def rendered(state):
    def glyph(p):
        def numeral(x):
            return " " if x == 0 else str(x)
        cell_state = state.cell_states[p]
        #cell_state = uncovered
        if cell_state == uncovered:
            if state.mines[p]:
                return "O"
            else:
                return numeral(state.count(p))
        else:
            return {covered: ".", flagged: "X", unsure: "?"}[cell_state]
    ret = []
    for j in range(state.mines.height):
        row = []
        for i in range(state.mines.width):
            row.append(glyph(Point(i,j)))
        ret.append("".join(row))
    return "\n".join(ret)

random.seed(0)
state = State(10, 10, 5)
mode = "U"
while True:
    print rendered(state)
    print "Current mode:", mode
    response = raw_input("Enter coordinates or change mode with (U)ncover / (F)lag / u(N)sure:").upper()
    if response in ("U", "F", "N"):
        mode = response
    else:
        try:
            x,y = map(int, response.split())
            p = Point(x,y)
            print p
        except:
            print "Sorry, did not recognize that input."
            continue
        if not state.mines.in_range(p):
            print "Sorry, that point is not in range"
            continue
        if mode == "F":
            if state.cell_states[p] in (covered, unsure):
                state.cell_states[p] = flagged
            elif state.cell_states[p] == flagged:
                state.cell_states[p] = covered
            else:
                print "Sorry, can't flag uncovered cells"
        elif mode == "N":
            if state.cell_states[p] in (covered, flagged):
                state.cell_states[p] = unsure
            elif state.cell_states[p] == unsure:
                state.cell_states[p] = covered
            else:
                print "Sorry, can't mark uncovered cells as unsure"
        else:
            to_uncover = state.get_group(p)
            for pos in to_uncover:
                state.cell_states[pos] = uncovered