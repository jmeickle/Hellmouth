import math
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
        # -1 to account for 0,0 start
        self.viewport = (math.floor(y/2)-1, math.floor(y/2)-1)
        self.viewrange = 11

    # Called before the map is rendered, but after it's ready to go.
    def ready(self):
        return

    # Hex character function, for maps only.
    def hd(self, x, y, glyph):
        # X/Y are offsets from the map center
        X = x - self.player.pos[0]
        Y = y - self.player.pos[1]
        self.window.addch(self.viewport[1]+Y, 2*(self.viewport[0]+X)+Y, glyph)

    # Accepts viewrange offsets to figure out what part of the map is visible.
    def get_glyph(self, x, y):
#        x += self.player.pos[0]
#        y += self.player.pos[1]
        return self.map.cells[min(self.map.height-1, y)]\
                             [min(self.map.width-1, x)]

    def add(self, actor):
        self.actors.append(actor)

    def draw(self):
        hexes = []
        hex.iterator(hexes, self.player.pos[0], self.player.pos[1], self.viewrange)

        minX = 0
        maxX = len(self.map.cells[0])
        minY = 0
        maxY = len(self.map.cells)

#        print hexes
#        exit()

        for h in hexes:
            if h[0] < minX or h[0] > maxX or h[1] < minY or h[1] > maxY:
                glyph = 'X'
            else:
                glyph = self.get_glyph(h[0], h[1])

            self.hd(h[0], h[1], glyph)

        # Draw the actors
#        for actor in self.actors:
#            self.hd(self.viewrange+1+actor.pos[0]-self.player.pos[0],\
#                    self.viewrange+1+actor.pos[1]-self.player.pos[1],\
#                    actor.glyph)

        self.window.refresh()

class Stats(View):
    def __init__(self, window, x, y, startx, starty):
        View.__init__(self, window, x, y, startx, starty)
        self.x_acc = 0
        self.y_acc = 0

    def draw(self):
        # Col 1
        self.x_acc = 0
        self.y_acc = 0

        self.line("-"*12)
        for x in range(10):
            self.line("-"+" "*10+"-")
        self.line("-"*12)

        # Col 2
        self.x_acc += 12
        self.y_acc = 0

        self.line("HP: %+3d/%2d" % (-50, 10))
        self.line("FP: %2d/%2d" % (10, 12))
        self.line("MP: 5")
        self.line("")
        self.line("Block: 5")
        self.line("Dodge: 5")
        self.line("Parry: 5")

        # Col 3
        self.x_acc += 12
        self.y_acc = 0

        self.line("ST: 5")
        self.line("DX: 5")
        self.line("IQ: 5")
        self.line("HT: 5")
        self.line("")
        self.line("Will: 5")
        self.line("Per.: 5")
        self.line("")
        self.line("Move: 5")
        self.line("Spd.: 5")

        # Combat Log
        self.x_acc = 0
        self.y_acc += 4

        for x in range(10):
            self.line("Sample combat log text, line %d" % x)

    def line(self, str):
        self.rds(0+self.x_acc, 0+self.y_acc, str)
        self.y_acc += 1

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
