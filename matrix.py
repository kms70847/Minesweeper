from geometry import Point

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
