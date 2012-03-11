class Actor:
    def __init__(self):
        self.glyph = 'x'

    def move(self, dir):
        pos = (self.pos[0]+dir[0], self.pos[1]+dir[1])
        if pos[0] >= 0 and pos[0] < self.map.width:
            if pos[1] >= 0 and pos[1] < self.map.height:
                self.pos = pos

