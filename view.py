from define import Color
import curses
import math
import hex
from lifepath import Lifepath
import re

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
        self.x_acc = 0
        self.y_acc = 0

    # Utility functions shared by all views

    # Set up curses attributes on a string
    # TODO: Handle anything but color
    def attr(self, col, attr):
        color = 0
        if col is not None:
            color += Color.pair[col]
        return curses.color_pair(color)

#        exit("%s"%Color.pair)]
        #col="red-black"
#        exit("%s"%col)
#"red-black"]
#        exit("COLOR: %s"%col)
#curses.color_pair(Color.pair[col])
#curses.color_pair(Color.pair[col]))
#self.attr(col, attr))

 #       ret = 0
  #      if col is not None:
#            exit("TEST: %s"%curses.color_pair(Color.pair[col]))
#            exit("TEST: %s" % Color.pair[col])
#            print Color.pair[col]
#            exit()
#            exit("PAIR: %s" % curses.color_pair(Color.pair[col]))
   #     if attr is not None:
    #        ret | 0
#attr
        return curses.color_pair(Color.pair[col])

    # Rectangular character function.
    def rd(self, x, y, glyph, col=0, attr=None):
        self.window.addch(y, x, glyph, self.attr(col, attr))

    # Rectangular string function.
    def rds(self, x, y, string, col=0, attr=None):
        self.window.addstr(y, x, string, self.attr(col, attr))

    # Draw a line; only relevant for text-y views.
    def line(self, str, col=None, attr=None):
        self.rds(0+self.x_acc, 0+self.y_acc, str, col, attr)
        self.y_acc += 1

    def reset(self):
        self.x_acc = 0
        self.y_acc = 0

    # Print a line with multiple colors
    # TODO: Handle other attributes.
    def cline(self, str, col=None, attr=None):
        strlen = 0
        curr_col = col
        substrs = re.split('<(/*\w*-?\w*)>',str)
        for substr in substrs:
            if substr == '':
                continue;
            if substr == '/':
                curr_col = col
            elif Color.pair.get(substr, None) is not None:
                curr_col = substr
            else:
                self.rds(0+self.x_acc+strlen, 0+self.y_acc, substr, curr_col, attr)
                strlen += len(substr)
        # Only increment y at the end of the line.
        self.y_acc += 1

class MainMap(View):
    def __init__(self, window, x, y, startx, starty):
        View.__init__(self, window, x, y, startx, starty)
        self.map = None
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
        # TERRIBLE HACK
        if glyph == '"':
            self.window.addch(self.viewport[1]+Y, 2*(self.viewport[0]+X)+Y, glyph, curses.A_DIM)
        elif glyph == '@':
            self.window.addch(self.viewport[1]+Y, 2*(self.viewport[0]+X)+Y, glyph, curses.A_STANDOUT)
        elif glyph == 'A':
            self.window.addch(self.viewport[1]+Y, 2*(self.viewport[0]+X)+Y, glyph, curses.A_STANDOUT)
        else: 
            self.window.addch(self.viewport[1]+Y, 2*(self.viewport[0]+X)+Y, glyph)

    # Accepts viewrange offsets to figure out what part of the map is visible.
    def get_glyph(self, x, y):
        return self.map.cells[min(self.map.width-1, x)][min(self.map.height-1, y)].draw()

    def draw(self):
        hexes = []
        hex.iterator(hexes, self.player.pos[0], self.player.pos[1], self.viewrange)

        minX = 0
        maxX = self.map.width-1
        minY = 0
        maxY = self.map.height-1

#        print hexes
#        exit()

        for h in hexes:
            if h[0] < minX or h[0] > maxX or h[1] < minY or h[1] > maxY:
                glyph = '"'
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
    short = { "Speed" : "Spd.",
              "Perception" : "Per.",
              "Strength" : "ST",
              "Dexterity" : "DX",
              "Intelligence" : "IQ",
              "Health" : "HT",
              "Hit Points" : "HP",
              "Fatigue Points" : "FP",
              "Mana Points" : "MP",
}

    def __init__(self, window, x, y, startx, starty):
        View.__init__(self, window, x, y, startx, starty)
        self.player = None

    def draw(self):
        # Col 1: Skeleton/Paperdoll
        self.reset()

        self.cline('    <%s>[</>%s<%s>]</>   ' % (self.player.loccol('Head'), self.player.wound('Head'), self.player.loccol('Head')))
        self.cline('  <%s>.--</><%s>T</><%s>--.</> ' % (self.player.loccol('LArm'), self.player.loccol('Torso'), self.player.loccol('RArm')))
        self.cline('  | =%s= | ' % self.player.wound('Torso'))
        self.cline('<magenta-red>%s</>  . -|- .<yellow-green>%s</> ' % (1, 8))
        self.cline('   .-|-.   ')
        self.cline('   |   |<red-cyan>%s</>  ' % 4)
        self.cline('   |   |  ')
        self.cline('  --   --<yellow-blue>%s</> ' % 5)
#        self.line("-"*12)
#        for x in range(10):
#            self.line("-"+" "*10+"-")
#        self.line("-"*12)

        # Col 2: Combat information
        self.x_acc += 12
        self.y_acc = 0

        self.statline('Hit Points')
        self.statline('Mana Points')
        self.statline('Fatigue Points')
        self.line("")
        self.statline('Block')
        self.statline('Dodge')
        self.statline('Parry')

        # Col 3: Stats
        self.x_acc += 12
        self.y_acc = 0

        self.statline("Strength")
        self.statline("Dexterity")
        self.statline("Intelligence")
        self.statline("Health")
        self.line("")
        self.statline("Will")
        self.statline("Perception")
        self.line("")
        self.statline("Move")
        self.statline("Speed")

        # Combat Log
        self.x_acc = 0
        self.y_acc += 1

        #self.line("Wounds:")
        #for loc in sorted(self.player.body.locs.items()):
        #    self.line("%6s: %s" % (loc[0], loc[1].wounds))

        #for x in range(10):
        #    self.line("Sample combat log text, line %d" % x)

    # Retrieve stat
    def stat(self, stat):
        return self.player.stat(stat)

    # Print a line like 'Dodge: 15' using stat()
    def statline(self, stat):
#        self.line("HP: %3d/%2d" % (-50, 10))
#        self.line("FP: %3d/%2d" % (10, 12))
#        self.line("MP: %3d/%2d" % (8, 15))

        short = Stats.short.get(stat, stat)
        # Alternate draw for these stats.
        if short in ["HP", "FP", "MP"]:
            self.line("%s: %3d/%2d" % (short, self.stat(stat), self.stat("Max"+stat)))
        else:
            self.line("%s: %s" % (short, self.stat(stat)))

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

class Status(View):
    def __init__(self, window, x, y, startx, starty):
        View.__init__(self, window, x, y, startx, starty)

    def draw(self):
        self.reset()
        self.line("")
        self.line("")
        self.line("Pain")
        self.line("Shock")
