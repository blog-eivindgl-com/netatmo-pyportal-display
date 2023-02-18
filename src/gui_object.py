class Gui_Object():
    def __init__(self, type, points) -> None:
        self.type = type
        self.points = points
        (x, y) = zip(*points)
        self.min_x = min(x)
        self.min_y = min(y)
        self.max_x = max(x)
        self.max_y = max(y)