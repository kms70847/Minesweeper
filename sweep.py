from geometry import Point
import random
from state import State        

def rendered(state):
    def glyph(p):
        def numeral(x):
            return " " if x == 0 else str(x)
        cell_state = state.cell_states[p]
        #cell_state = uncovered
        if cell_state == State.uncovered:
            if state.mines[p]:
                return "O"
            else:
                return numeral(state.count(p))
        else:
            return {State.covered: ".", State.flagged: "X", State.unsure: "?"}[cell_state]
    ret = []
    for j in range(state.mines.height):
        row = []
        for i in range(state.mines.width):
            row.append(glyph(Point(i,j)))
        ret.append("".join(row))
    return "\n".join(ret)

def state_from_name(name):
    return {"U": State.uncovered, "F": State.flagged, "N": State.unsure}[name]

def name_from_state(state):
    return {State.uncovered: "U", State.flagged: "F", State.unsure: "N"}[state]

random.seed(0)
state = State(10, 10, 5)
mode = State.uncovered
while True:
    print rendered(state)
    print "Current mode:", name_from_state(mode)
    response = raw_input("Enter coordinates or change mode with (U)ncover / (F)lag / u(N)sure:").upper()
    if response in ("U", "F", "N"):
        mode = state_from_name(response)
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
        if mode in (State.flagged, State.unsure):
            if state.cell_states[p] == State.uncovered:
                print "Sorry, can't mark uncovered cells"
            elif state.cell_states[p] == mode:
                state.cell_states[p] = State.covered
            else:
                state.cell_states[p] = mode
        elif mode == State.uncovered:
            to_uncover = state.get_group(p)
            for pos in to_uncover:
                state.cell_states[pos] = State.uncovered
        else:
            raise Exception("unknown mode {}".format(mode))