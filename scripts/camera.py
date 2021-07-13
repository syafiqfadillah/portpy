class Camera:
    def __init__(self, border):
        self.border = border
        self.true_scroll = [0, 0]
        self.scroll = self.true_scroll.copy()
    
    def focus(self, position):
        # scroll the screen according to the movement of the given entity position
        self.true_scroll[0] += (position[0] - self.true_scroll[0] - 220) / 20
        self.true_scroll[1] += (position[1] - self.true_scroll[1] - 230) / 20
        self.scroll = self.true_scroll.copy()
        self.scroll[0] = max(self.border[0], int(self.scroll[0]))
        self.scroll[0] = min(self.scroll[0], self.border[1] - 300)
        self.scroll[1] = max(self.border[0], int(self.scroll[1]))
        self.scroll[1] = min(self.scroll[1], self.border[1] - 300)
    
    def get_scroll(self):
        return self.scroll
