class Component():

    def __init__(self, window, x=0, y=0):
        self.window = window
        self.x = x
        self.y = y

class MainMap(Component):
    def __init__(self, window, x, y):
        Component.__init__(self, window, x, y)
        self.map = None
        self.actors = []

    def add(self, actor):
        self.actors.append(actor)

    def draw(self):
        # Draw the map. We do two tricks to make this hex-y:
        #     * offset every other row by 1.
        #     * multiply the x position by two.
        for y in range(self.map.height):
            for x in range(self.map.height):
                offset = y % 2
                self.window.addch(y, (2*x) + offset, self.map.cells[y][x])

        # Draw the actors
        for actor in self.actors:
            self.window.addch(actor.y, actor.x, actor.glyph)
#class MiniMap(Component):

#class Stats:
#    def 
