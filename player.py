class Player:
    def __init__(self):
        self.hp = 1
        self.x = 3
        self.y = 3
        self.glyph = '@'

    def draw(self, window):
        window.addch(self.y, self.x, self.glyph)
