import hex
from lifepath import Lifepath

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

class View():
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

class MainMap(View):
    def __init__(self, window, x, y, startx, starty):
        View.__init__(self, window, x, y, startx, starty)
        self.map = None
        self.actors = []
        self.player = None
        self.viewport = (11, 11)
        self.viewrange = 7

    # Called before the map is rendered, but after it's ready to go.
    def ready(self):
        self.center = self.player.pos

    # Hex character function, for maps only.
    def hd(self, x, y, glyph):
        # X/Y are offsets from the map center
        X = x - self.center[0]
        Y = y - self.center[1]
        print X, Y, glyph
        self.window.addch(self.viewport[1]+Y, 2*(self.viewport[0]+X)+Y, glyph)

    # Accepts viewrange offsets to figure out what part of the map is visible.
    def get_glyph(self, x, y):
        # DEBUG:
        # x = min(self.map.height-1, x+self.center[0])
        # y = min(self.map.height-1, y+self.center[1])
        # return chr(48 + x % 10)
        x += self.center[0]
        y += self.center[1]
        return self.map.cells[min(self.map.height-1, y)]\
                             [min(self.map.width-1, x)]

    def add(self, actor):
        self.actors.append(actor)

    def draw(self):
        hexes = []
        hex.iterator(hexes, self.center[0], self.center[1], self.viewrange)

        for h in hexes:
            self.hd(h[0], h[1], self.get_glyph(h[0], h[1]))

        # Draw the actors
#        for actor in self.actors:
#            self.hd(self.viewrange+1+actor.pos[0]-self.center[0],\
#                    self.viewrange+1+actor.pos[1]-self.center[1],\
#                    actor.glyph)

        self.window.refresh()

class Stats(View):
    def __init__(self, window, x, y, startx, starty):
        View.__init__(self, window, x, y, startx, starty)

    def draw(self):
        self.rds(0, 0, "HP: 5")
        self.rds(0, 2, "ST: 15")
        self.rds(0, 3, "DX: 15")
        self.rds(0, 4, "IQ: 15")
        self.rds(0, 5, "HT: 15")

class Chargen(View):
    def __init__(self, window, x, y, startx, starty):
        View.__init__(self, window, x, y, startx, starty)
        self.selector = Selector(self, 5)
        self.lifepath = Lifepath()

    def draw(self):
#        self.rds(0, 10, lifepath)
        if hasattr(self.selector, 'parent'):
            self.rds(0, 23, "Currently selected option: %s" % self.selector.choice)
        else:
            self.rds(0, 23, "Final option was: %s" % self.selector)

#class MiniMap(View):
#class Health(View):
