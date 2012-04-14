from define import Color
from define import NW, NE, CE, SE, SW, CW
from dialogue import chargen
import curses
import math
import hex
from lifepath import Lifepath
import re
from collections import deque
from lifepath_events import eventdata

# Cycling selector.
class Selector():
    def __init__(self, parent, choices, initial=0):
        self.parent = parent
        self.choices = choices
        self.choice = initial

    def next(self, amt=1):
        self.choice += amt
        if self.choice >= self.choices:
            self.choice = 0

    def prev(self, amt=1):
        self.choice -= amt
        if self.choice < 0:
            self.choice = self.choices-1

    # TODO: Make this take a function and call it
    def choose(self):
        self.parent.selector = self.choice

class Cursor():
    def __init__(self, parent, pos):
        self.parent = parent
        self.pos = pos
        self.style = ("{","}")

    # Move the cursor (hexagonally).
    def scroll(self, dir):
        self.pos = (self.pos[0] + dir[0], self.pos[1] + dir[1])

    # This is a function so that the cursor color can change in response to
    # the hex that it's targeting.
    def color(self):
        return "magenta-black"

class View():
    def __init__(self, window, x, y, startx=0, starty=0):
        self.screen = window
        self.window = window.subwin(y, x, starty, startx)
        self.x = startx
        self.y = starty
        self.width = x
        self.height = y
        self.x_acc = 0
        self.y_acc = 0
        self.alive = True
        self.children = []

    # Utility functions shared by all views

    # Draw self. Abstract.
    def draw(self):
        return True

    # Draw yourself, then recurse through your children to draw them.
    def _draw(self):
        if self.draw() is not False:
            for child in self.children:
                if child._draw() is False:
                    return False
            return True
        else:
            return False

    # Handle keyin. Abstract.
    def keyin(self, c):
        return True

    # Recurse through children trying their keyin functions,
    # until you've done your own.
    def _keyin(self, c):
        for child in self.children:
            if child._keyin(c) is False:
                return False
        return self.keyin(c)

    # Spawn child and return it.
    def spawn(self, child):
        self.children.append(child)
        child.parent = self
        return child

    # Set up curses attributes on a string
    # TODO: Handle anything but color
    def attr(self, col, attr):
        color = 0
        if col is not None and col is not 0:
            color += Color.pair[col]
        return curses.color_pair(color)

    # Rectangular character function.
    def rd(self, x, y, glyph, col=0, attr=None):
        self.window.addch(y, x, glyph, self.attr(col, attr))

    # Rectangular string function.
    def rds(self, x, y, string, col=0, attr=None):
        self.window.addstr(y, x, string, self.attr(col, attr))

    # Draw a line; only relevant for text-y views.
    # TODO: Handle multi-line strings!
    def line(self, str, col=None, attr=None):
        self.rds(0+self.x_acc, 0+self.y_acc, str, col, attr)
        self.y_acc += 1

    def reset(self):
        self.x_acc = 0
        self.y_acc = 0

    # Print a line with multiple colors
    # TODO: Handle multi-line strings!
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
    def __init__(self, window, x, y, startx=0, starty=0):
        View.__init__(self, window, x, y, startx, starty)
        self.map = None
        self.player = None
        # -1 to account for 0,0 start
        self.viewport = (math.floor(y/2)-1, math.floor(y/2)-1)
        self.cursor = None

    # Called before the map is rendered, but after it's ready to go.
    def ready(self):
        return

    def keyin(self, c):
        # TODO: Fix spacing here.
        # Return true if no keyin was used; otherwise, false.
        if c == ord('I'):
            child = self.spawn(Inventory(self.screen, self.width, self.height))
            child.map = self.map
            child.reset()
            return False

        elif c == ord('v'):
            if self.cursor is None:
                child = self.spawn(Examine(self.screen, self.width, 1, 0, 23))
                self.cursor = Cursor(self, self.player.pos)
                self.cursor.child = child
                return False

        # TODO: Move this elsewhere, it doesn't belong.
        if self.cursor is not None:
            if c == ord(' '):
                self.cursor = None
                self.child = None
            elif c == ord('7'):
                self.cursor.scroll(NW)
            elif c == ord('4'):
                self.cursor.scroll(CW)
            elif c == ord('1'):
                self.cursor.scroll(SW)
            elif c == ord('9'):
                self.cursor.scroll(NE)
            elif c == ord('6'):
                self.cursor.scroll(CE)
            elif c == ord('3'):
                self.cursor.scroll(SE)
            else: return True
            return False

        else:
        # TODO: Move these!
            if c == ord('7'):
                self.map.player.do(NW)
            elif c == ord('4'):
                self.map.player.do(CW)
            elif c == ord('1'):
                self.map.player.do(SW)
            elif c == ord('9'):
                self.map.player.do(NE)
            elif c == ord('6'):
                self.map.player.do(CE)
            elif c == ord('3'):
                self.map.player.do(SE)
            elif c == ord('5'):
                self.map.player.over()
            else: return True
            return False

    # Hex character function, for maps only.
    def hd(self, x, y, glyph, col=0, attr=None):
        # X/Y are offsets from the map center
        X = x - self.player.pos[0]
        Y = y - self.player.pos[1]

        self.window.addch(self.viewport[1]+Y, 2*(self.viewport[0]+X)+Y, glyph, self.attr(col, attr))

    # Offset hexes.
    def offset_hd(self, x, y, glyph, col=0, attr=None, dir=(0,0)):
        # X/Y are offsets from the map center
        X = x - self.player.pos[0]
        Y = y - self.player.pos[1]

        self.window.addch(self.viewport[1]+Y+dir[0], 2*(self.viewport[0]+X)+Y+dir[1], glyph, self.attr(col, attr))

    # Accepts viewrange offsets to figure out what part of the map is visible.
    def get_glyph(self, x, y):
        return self.map.cells[min(self.map.width-1, x)][min(self.map.height-1, y)].draw()

    def draw(self):
        hexes = []
        hex.iterator(hexes, self.player.pos[0], self.player.pos[1], self.map.viewrange)

        minX = 0
        maxX = self.map.width-1
        minY = 0
        maxY = self.map.height-1

        for h in hexes:
            if h[0] < minX or h[0] > maxX or h[1] < minY or h[1] > maxY:
                glyph = 'X'
                col = "red-black"
            else:
                glyph, col = self.get_glyph(h[0], h[1])

            self.hd(h[0], h[1], glyph, col)

        # Draw the map cursor if it's present.
        if self.cursor is not None:
            c = self.cursor
            self.offset_hd(c.pos[0], c.pos[1], c.style[0], c.color(), None, (0,-1))
            self.offset_hd(c.pos[0], c.pos[1], c.style[1], c.color(), None, (0,1))
            return False

        #self.window.refresh()

# TODO: Update for FOV
class Examine(View):
    def __init__(self, window, x, y, startx=0, starty=0):
        View.__init__(self, window, x, y, startx, starty)
        self.parent = None

    def draw(self):
        self.reset()
        pos = self.parent.cursor.pos
        map = self.parent.map
        str = map.cell(pos).describe()
        self.line(str)

class Stats(View):
    # TODO: Move this out of here, it really doesn't belong.
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

    def __init__(self, window, x, y, startx=0, starty=0):
        View.__init__(self, window, x, y, startx, starty)
        self.player = None

    def draw(self):
        # Col 1: Skeleton/Paperdoll
        self.reset()
        # Brevity!
        p = self.player

        self.cline('    <%s>[</>%s<%s>]</>   ' % (p.loccol('Head'), p.wound('Head'), p.loccol('Head')))
        self.cline('  <%s>.--</><%s>T</><%s>--.</> ' % (p.loccol('LArm'), p.loccol('Torso'), p.loccol('RArm')))
        self.cline(' %s<%s>|</> <%s>=</>%s<%s>=</> <%s>|</>%s' % (p.wound('LArm'), p.loccol('LArm'), p.loccol('Torso'), p.wound('Torso'), p.loccol('Torso'), p.loccol('RArm'), p.wound('RArm')))
        self.cline(' %s<%s>.</> <%s>-|-</> <%s>.</>%s ' % (p.wound('LHand'), p.loccol('LHand'), p.loccol('Torso'), p.loccol('RHand'), p.wound('RHand')))
        self.cline('   <%s>.-</><%s>|</><%s>-.</>   ' % (p.loccol('LLeg'), p.loccol('Groin'), p.loccol('RLeg')))
        self.cline('  %s<%s>|</>   <%s>|</>%s  ' % (p.wound('LLeg'), p.loccol('LLeg'), p.loccol('RLeg'), p.wound('RLeg')))
        self.cline('   <%s>|</>   <%s>|</>   ' % (p.loccol('LLeg'), p.loccol('RLeg')))
        self.cline(' %s<%s>--</>   <%s>--</>%s ' % (p.wound('LFoot'), p.loccol('LFoot'), p.loccol('RFoot'), p.wound('RFoot')))
#        self.line("-"*12)
#        for x in range(10):
#            self.line("-"+" "*10+"-")
#        self.line("-"*12)

        # Col 2: Combat information
        self.x_acc += 12
        self.y_acc = 0
        self.line("Remaining HP: %s" % p.hp)
#        self.statline('Hit Points')
#        self.statline('Mana Points')
#        self.statline('Fatigue Points')
#        self.line("")
#        self.statline('Block')
#        self.statline('Dodge')
#        self.statline('Parry')

        # Col 3: Stats
        self.x_acc += 12
        self.y_acc = 0

#        self.statline("Strength")
#        self.statline("Dexterity")
#        self.statline("Intelligence")
#        self.statline("Health")
#        self.line("")
#        self.statline("Will")
#        self.statline("Perception")
#        self.line("")
#        self.statline("Move")
#        self.statline("Speed")

        # Combat Log
        self.x_acc = 0
        self.y_acc += 1

        # Don't delete! Probably will reuse this for a 'health' screen.
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

# TODO: Chargen actually affects stats.
class Chargen(View):
    def __init__(self, window, x, y, startx=0, starty=0):
        View.__init__(self, window, x, y, startx, starty)
        self.player = None
        self.lifepath = Lifepath()
        self.current = None
        self.selected = 0
        self.max = len(self.lifepath.initial)-1

    def scroll(self, amt):
        self.selected += amt

        if self.selected < 0:
            self.selected = 0

        if self.selected >= self.max:
            self.selected = self.max

    def next(self):
        self.current.choose(self.current.choices[self.selected])
        self.current = self.current.child
        # TODO: Handle appending inside of choose()
        self.lifepath.events.append(self.current)

        # Reset choice:
        self.selected = 0
        if self.current.choices is not None:
            self.max = len(self.current.choices)-1
        else:
            self.max = 0 # Irrelevant, but whatever.

    def prev(self):
        # TODO: Fix this, it's buggy.
        if self.current.parent is not None:
            # Get previous selection.
#            prev_sel = 0
#            for x in range(len(self.current.parent.choices)):
#                if self.current.parent.choices[x] == self.current.name:
#                    prev_sel = x

            # Set self to the old one.
            self.current.undo()
            self.current = self.current.parent
            self.lifepath.events.pop()
            self.selected = 0 #prev_sel
            self.max = len(self.current.choices)-1
            return False

    def draw(self):
        self.reset()

        # Top half of the screen:

        # Triggers if we haven't started down a lifepath yet.
        # Prints initial text.
        if self.current is None:
            self.cline(chargen["initial"])
        # STUB: Triggers if an event brings a prompt with it.
        # Prints the prompt text.
        #elif self.current.prompt is not None:
        # Triggers if we're at a certain age in the lifepath.
        # Prints the text asking about the NEXT age category.
        elif self.current.age is not None:
            self.cline(chargen["age-%s" % (self.current.age+1)])
        # Triggers if we have a choice without an associated age (i.e., a final one.)
        # Prints a list of events in your lifepath.
        else:
            self.cline(chargen["final"])
            self.y_acc += 2
            level = self.y_acc
            self.cline("What you've told the stranger:")
            self.y_acc += 1
            for event in self.lifepath.events:
                # We only want events with short descriptions. If they take a certain number of years, list that.
                if event.short is not None:
                    str = "You had %s" % event.short
                    if event.years is not None:
                        str += " "
                        str += "(for %s years)" % event.years
                    self.cline(str)
            old = self.y_acc
            self.y_acc = level
            self.x_acc = 60
            # TODO: Don't calculate this each time, jeez!
            self.player.stats = self.lifepath.effects()
            self.cline("Your character:")
            for stat, value in self.player.stats.iteritems():
                self.cline("%s: %s" % (stat, value))#: %s" % (stat, value))
            self.y_acc = old
            self.x_acc = 0

        # Bottom half of the screen:
        self.y_acc += 5

        # Print the text from the currently highlighted event.
        if self.current is None:
            self.line(self.lifepath.initial[self.selected][1])
        else:
            if self.current.choices is not None:
               self.cline(eventdata.get(self.current.choices[self.selected], {'text': '<DEBUG: NO TEXT>'})['text'])

        self.y_acc += 1
 
        # Print a list of choices for the initial skip.
        if self.current is None:
            for x in range(len(self.lifepath.initial)):
                if x == self.selected:
                    self.cline("<green-black>* %s</>" % self.lifepath.initial[x][0])
                else:
                    self.line("* %s" % self.lifepath.initial[x][0])
        # Prints a list of choices for the current event.
        elif self.current.choices is not None:
            for choice in self.current.choices:
                if self.current.choices[self.selected] == choice:
                    self.cline("<green-black>* %s</>" % choice)
                else:
                    self.line("* %s" % choice)
        # Confirms whether to start.
        else:
            self.cline("<red-black>Really use this lifepath? You can't change it once you've started the game.</>")

        # Don't draw anything else.
        return False

    def keyin(self, c):
        # Make the first choice, which uses a different system to
        # skip ahead several steps in the chargen system.
        if self.current is None:
            if c == curses.KEY_ENTER or c == ord('\n'):
                skip = self.lifepath.initial
                self.lifepath.start('Start')
                self.current = self.lifepath.initial
                for x in range(self.selected):
                    self.current.choose(skip[x+1][2])
                    self.current = self.current.child
                self.selected = 0
            elif c == curses.KEY_UP:
                self.scroll(-1)
            elif c == curses.KEY_DOWN:
                self.scroll(1)
            else: return True
            return False
        # Choicely choosing the next choice from choices
        if self.current.choices is not None:
            if c == curses.KEY_ENTER or c == ord('\n'):
                self.next()
            elif c == ord(' '):
                self.prev()
            elif c == curses.KEY_UP:
                self.scroll(-1)
            elif c == curses.KEY_DOWN:
                self.scroll(1)
            else: return True
            return False
        # Last stage: choosing whether to start the game or not.
        else:
            if c == curses.KEY_ENTER or c == ord('\n'):
                self.alive = False
            elif c == ord(' '):
                self.prev()
            else: return True
            return False

# TODO: Add a minimap and a health screen.
#class MiniMap(View):
#class Health(View):

# TODO: Implement this
class Status(View):
    def __init__(self, window, x, y, startx=0, starty=0):
        View.__init__(self, window, x, y, startx, starty)

    def draw(self):
        self.reset()
#        self.line("")
#        self.line("")
#        self.line("Pain", "red-black")
#        self.line("Shock", "magenta-black")

# Very hackish right now: events added through map...
class Log(View):
    def __init__(self, window, x, y, startx=0, starty=0):
        View.__init__(self, window, x, y, startx, starty)
        self.events = deque()
        self.index = 0

    # Scrolling the log up and down.
    def keyin(self, c):
        if c == curses.KEY_UP: self.scroll(-1)
        elif c == curses.KEY_DOWN: self.scroll(1)
        else: return True
        return False

    # Add an event to the history. Autoscrolls unless this has been turned off.
    def add(self, event, scroll=True):
        self.events.append(event)
        if scroll is True:
            self.scroll(1)

    def scroll(self, amt):
        self.index += amt
        # Prevent an index below zero.
        if self.index < 0:
            self.index = 0

        # Prevent scrolling if there's no more entries to see.
        max = len(self.events) - self.height
        if self.index >= max:
            self.index = max

    def draw(self):
        self.reset()

        count = 0
        lines = 0
        for x in self.events:
            count += 1
            if count <= self.index:
                continue
            # TODO: Fix multiline and get rid of that -1.
            if lines >= self.height-1:
                break
            self.line(x)
            lines += 1
            continue

    # TODO: Multi-line log entries
            if len(x) > self.width:
                substrs = self.logline(x)
                for substr in substrs:
                    self.line(substr)
                    lines += 1

    def logline(self, str, x=None):
        if x is None:
            x = self.width

        ret = []
        line = ""
        count = 0
        lines = 0

        for char in str:
            count += 1
            line += char
            if count >= x:
                count = 0
                if lines > 0:
                    line = "  %s" % line
                ret.append(line)
                lines += 1

        return ret

class Inventory(View):
    def __init__(self, window, x, y, startx=0, starty=0):
        View.__init__(self, window, x, y, startx, starty)
        self.map = None # So it can access, e.g., items on the ground
        self.player = None
        self.items = None
        self.selector = None

    # Just so this doesn't have to be passed in.
    def reset(self):
        self.x_acc = 0
        self.y_acc = 0
        self.player = self.map.player
        self.items = self.player.items()
        if self.selector is None:
            self.selector = Selector(self, len(self.items))
        else:
            self.selector.choices = len(self.items)
            self.selector.choice = min(self.selector.choice, self.selector.choices-1)

    def draw(self):
        self.reset()
        self.x_acc += 10
        self.cline("Inventory")
        self.y_acc += 3
        if len(self.items) > 0:
            for index, appearance, item in self.items:
                if self.selector.choice == index:
                    self.cline("<green-black>%s - %s (%s)</>" % (index, appearance, len(item)))
                else:
                    self.cline("%s - %s (%s)" % (index, appearance, len(item)))
        else:
            self.cline("No items")

        self.y_acc = 0
        self.x_acc += 20

        self.cline("Equipped")
        for loc in sorted(self.player.body.locs.items()):
            equipped = ""
            for held in loc[1].held:
                equipped += "%s (held)" % held.appearance()
            for worn in loc[1].worn:
                equipped += "%s (worn)" % worn.appearance()
            if len(equipped) == 0:
                equipped = "Nothing"
            self.cline("%6s: %s" % (loc[0], equipped))

    def keyin(self, c):
        if c == ord(' '):
            self.parent.children.remove(self)
        elif c == ord('+'):
            self.selector.next()
        elif c == ord('-'):
            self.selector.prev()
        elif c == curses.KEY_ENTER or c == ord('\n'):
            if len(self.items) > 0:
                index, appearance, item = self.items[self.selector.choice]
                self.player.drop(appearance)
        else: return True
        return False
