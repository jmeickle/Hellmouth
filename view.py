from lifepath import Lifepath
viewrange = 10

# Cycling selector.
class Selector():
    def __init__(self, parent, choices, initial=0):
        self.parent = parent
        self.choices = choices
        self.choice = initial

    def next(self):
        self.choice += 1
        if self.choice > self.choices:
            self.choice = 0

    def prev(self):
        self.choice -= 1
        if self.choice < 0:
            self.choice = self.choices

    def choose(self):
        self.parent.selector = self.choice

class Component():

    def __init__(self, window, x, y, startx, starty):
        self.window = window.subwin(y, x, starty, startx)
        self.x = startx
        self.y = starty

    # Rectangular character function.
    def rd(self, x, y, glyph):
        self.window.addch(y, x, glyph)

    # Rectangular string function.
    def rds(self, x, y, string):
        self.window.addstr(y, x, string)

    # Hex character function.
    def hd(self, x, y, glyph):
        self.window.addch(y, 2*x + y, glyph)

class MainMap(Component):
    def __init__(self, window, x, y, startx, starty):
        Component.__init__(self, window, x, y, startx, starty)
        self.map = None
        self.actors = []
        self.player = None

    def center_x(self):
        return self.player.pos[0]

    def center_y(self):
        return self.player.pos[1]

    # Accepts viewrange offsets to figure out what part of the map is visible.
    def get_glyph(self, x, y):
        # DEBUG:
        # x = min(self.map.height-1, x+self.center_x())
        # y = min(self.map.height-1, y+self.center_y())
        # return chr(48 + x % 10)
        x += self.center_x()
        y += self.center_y()
        return self.map.cells[min(self.map.height-1, y)]\
                             [min(self.map.width-1, x)]

    def add(self, actor):
        self.actors.append(actor)

    def draw(self):
        # The +1 is so that @ = 0, 0 in viewrange.
        for y in range(-viewrange, viewrange+1):
            for x in range(-viewrange, viewrange+1):
                self.hd(viewrange+x, viewrange+y, self.get_glyph(x, y))

        # Draw the actors
        for actor in self.actors:
            self.hd(viewrange+1+actor.pos[0]-self.center_x(),\
                    viewrange+1+actor.pos[1]-self.center_y(),\
                    actor.glyph)

        self.window.refresh()

class Stats(Component):
    def __init__(self, window, x, y, startx, starty):
        Component.__init__(self, window, x, y, startx, starty)

    def draw(self):
        self.rds(0, 1, "HP: 5")
        self.rds(0, 2, "ST: 15")
        self.rds(0, 3, "DX: 15")
        self.rds(0, 4, "IQ: 15")
        self.rds(0, 5, "HT: 15")

class Chargen(Component):
    def __init__(self, window, x, y, startx, starty):
        Component.__init__(self, window, x, y, startx, starty)
        self.selector = Selector(self, 5)
        self.lifepath = Lifepath()

    def draw(self):
#        self.rds(0, 10, lifepath)
        if hasattr(self.selector, 'parent'):
            self.rds(0, 5, "Currently selected: %s" % self.selector.choice)
        else:
            self.rds(0, 5, "Final choice: %s" % self.selector)

#class MiniMap(Component):
#class Health(Component):
