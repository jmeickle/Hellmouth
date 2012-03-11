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
                self.hd(x, y, self.map.cells[y][x])

        # Draw the actors
        for actor in self.actors:
            self.hd(actor.x, actor.y, actor.glyph)
#class MiniMap(Component):

#class Stats:
#    def 
