class Component():

    def __init__(self, window, x=0, y=0):
        self.window = window
        self.x = x
        self.y = y

    # Rectangular drawing function.
    def rd(self, x, y, glyph):
        self.window.addch(y, x, glyph)

    # Rectangular string function.
    def rds(self, x, y, string):
        self.window.addstr(y, x, string)

    # Hex drawing function.
    def hd(self, x, y, glyph):
        self.window.addch(y, 2*x + y, glyph)

class MainMap(Component):
    def __init__(self, window, x, y):
        Component.__init__(self, window, x, y)
        self.map = None
        self.actors = []

    def add(self, actor):
        self.actors.append(actor)

    def draw(self):
        # Draw the map.
        for y in range(self.map.height):
            for x in range(self.map.height):
# DEBUG:
#                self.hd(x+1, y+1, chr(48+x))
                self.hd(x, y, self.map.cells[y][x])

        # Draw the actors
        for actor in self.actors:
            self.hd(actor.pos[0], actor.pos[1], actor.glyph)

class Stats(Component):
    def __init__(self, window, x, y):
        Component.__init__(self, window, x, y)

    def draw(self):
        self.rds(self.x, self.y, "HP: 5")
        self.rds(self.x, self.y+2, "ST: 15")
        self.rds(self.x, self.y+3, "DX: 15")
        self.rds(self.x, self.y+4, "IQ: 15")
        self.rds(self.x, self.y+5, "HT: 15")

#class MiniMap(Component):

#class Stats:
#    def
