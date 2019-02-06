class MouseDrag:
    def __init__(self):
        self.dragging = 0
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0

    def begin(self, x, y):
        self.dragging = True
        self.x = x
        self.y = y
        self.dx = x
        self.dy = y

    def end(self, x, y):
        self.dragging = False

    def update(self, x, y):
        if self.dragging:
            self.dx = x - self.x
            self.dy = y - self.y
            self.x = x
            self.y = y

    def is_dragging(self):
        return self.dragging

    def get_delta(self):
        return self.dx, self.dy
