import curses

from views.view import View
from views.screens import Screen
from views.input import *

from define import *
from hex import *
from data.skills import skill_list

from collections import deque
from random import choice

# Main tactical window class.
class Window(View):
    def __init__(self, window):
        View.__init__(self, window, TERM_X, TERM_Y)

    def ready(self):
        self.spawn(MainPane(self.screen))
        self.spawn(SidePane(self.screen))

# Larger, left-hand pane
class MainPane(View):
    def __init__(self, window):
        View.__init__(self, window, MAP_X, MAP_Y, MAP_START_X, MAP_START_Y)

    def ready(self):
        self.spawn(Status(self.screen, STATUS_X, STATUS_Y, STATUS_START_X, PANE_START_Y))
        self.spawn(MainMap(self.screen, MAP_X, MAP_Y, MAP_START_X, MAP_START_Y))

# Smaller, right-hand pane
class SidePane(View):
    def __init__(self, window):
        View.__init__(self, window, PANE_X, PANE_Y, PANE_START_X, PANE_START_Y)

    def ready(self):
        self.spawn(Stats(self.screen, PANE_X, STATS_Y, PANE_START_X, PANE_START_Y))
        self.spawn(Log(self.screen, PANE_X, LOG_Y, PANE_START_X, LOG_START_Y))

# TODO: Make this a subclass of a Map view, to account for tactical/strategic/etc.
class MainMap(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)
        # -1 to account for 0,0 start
        self.viewport = (int(y/2)-1, int(y/2)-1)
        self.viewrange = 10
        self.cursor = None

    def keyin(self, c):
        # TODO: Allow multiple open children.
        if not self.children:
            if c == ord('I'):
                self.spawn(Inventory(self.screen, self.width, self.height))
                return False

            elif c == ord('v'):
                if self.cursor is None:
                    self.cursor = self.spawn(Cursor(self.player.pos))
                    self.cursor.spawn(Examine(self.screen, self.width, 1, self.LEFT, self.BOTTOM))
                    return False

        if True is True:#else:
        # This is generally the last step before keys fall into oblivion.
        # TODO: Feed the keyin into a player function.
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
            elif c == ord('>') or c == ord('<'):
                self.map.player.stairs()
            else: return True
            return False

    # Hex character function, for maps only.
    def hd(self, pos, glyph, col=None, attr=None):
        # Three sets of coords are involved:
        x, y = pos
        c_x, c_y = self.center
        v_x, v_y = self.viewport

        # Offsets from the viewport center
        off_x = x - c_x
        off_y = y - c_y

        draw_x = off_y + 2*(off_x+v_x)
        draw_y = off_y + v_y

        assert self.undrawable((draw_x, draw_y)) is False, "hd function tried to draw out of bounds: %s at %s." % (self.__dict__, (draw_x, draw_y))
        try: self.window.addch(draw_y, draw_x, glyph, self.attr(col, attr))
        except curses.error: pass

    # Draw to offset hexes, i.e., the 'blank' ones.
    def offset_hd(self, pos, dir, glyph, col=None, attr=None):
        # Four sets of coords are involved:
        x, y = pos
        c_x, c_y = self.center
        v_x, v_y = self.viewport
        d_x, d_y = dir

        # Offsets from the viewport center
        off_x = x - c_x
        off_y = y - c_y

        draw_x = off_y + 2*(off_x+v_x) + d_x
        draw_y = off_y + v_y + d_y

        assert self.undrawable((draw_x, draw_y)) is False, "offset hd function tried to draw out of bounds: %s at %s." % (self.__dict__, (draw_x, draw_y))
        try: self.window.addch(draw_y, draw_x, glyph, self.attr(col, attr))
        except curses.error: pass

    # Accepts viewrange offsets to figure out what part of the map is visible.
    def get_glyph(self, pos):
        return self.map.cell(pos).draw()

    def draw(self):
        if self.cursor is not None:
            self.center = self.cursor.pos
        else:
            self.center = self.player.pos

        cells = area(self.viewrange, self.center)

        for cell in cells:
            if self.map.valid(cell) is not False:
                glyph, col = self.get_glyph(cell)
                self.hd(cell, glyph, col)
            else:
                glyph = 'X'
                col = "magenta-black"
                # If we ever want to print something for missing cells.
                #self.hd(cell, glyph, col)


# A single line of text at the bottom of the screen describing what your
# cursor is currently over.
# TODO: Update for FOV
class Examine(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)

    def keyin(self, c):
        if c == curses.KEY_ENTER or c == ord('\n'):
            if self.children:
                return True
            child = self.spawn(CharacterSheet(self.screen, PANE_X, PANE_Y, PANE_START_X, PANE_START_Y))
        else:
            return True
        return False

    def draw(self):
        pos = self.parent.pos
        cell = self.map.cell(pos)
        if cell is not None:
            string = cell.contents()
            self.line("Selected: %s" % string)
        else:
            self.line("There's... nothing there. Nothing at all.")

class Stats(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)

    def draw(self):
        # Col 1: Skeleton/Paperdoll
        for line in self.player.paperdoll():
            self.cline(line)

        # Col 2: Combat information
        self.x_acc += 12
        self.y_acc = 0
        self.statline('HP')
        self.statline('MP')
        self.statline('FP')
        self.line("")
        self.statline('Block')
        self.statline('Dodge')
        self.statline('Parry')

        # Col 3: Stats
        self.x_acc += 12
        self.y_acc = 0

        self.statline("ST")
        self.statline("DX")
        self.statline("IQ")
        self.statline("HT")
        self.line("")
        self.statline("Will")
        self.statline("Perception")
        self.line("")
        self.statline("Move")
        self.statline("Speed")

        # Combat Log
        self.x_acc = 0
        self.y_acc += 1

        # Don't delete! Probably will reuse this for a 'health' screen.
        #self.line("Wounds:")
        #for loc in sorted(self.player.body.locs.items()):
        #    self.line("%6s: %s" % (loc[0], loc[1].wounds))

        #for x in range(10):
        #    self.line("Sample combat log text, line %d" % x)

    # Print a line like 'Dodge: 15' using stat()
    # TODO: Print colors, *s, etc. for more info.
    def statline(self, stat):
        # Always use the shortest label here.
        label = labels.get(stat)[0]
        value = self.player.stat(stat)
        if value is None:
            value = "n/a"

        # These particular stats actually have two stats to display.
        if stat in ["HP", "FP", "MP"]:
            self.line("%s: %3d/%2d" % (label, value, self.player.stat("Max"+stat)))
        else:
            self.line("%s: %s" % (label, value))

# TODO: Implement this
class Status(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)

    def draw(self):
         self.line(self.map.name, "red-black")
         self.line("Level %s" % self.map.level.current_depth())
#        self.line("Pain", "red-black")
#        self.line("Shock", "magenta-black")

# Very hackish right now: events added through map...
class Log(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)
        self.events = deque()

    # Spawn a scroller and add the log to the map.
    def ready(self):
        self.scroller = self.spawn(Scroller(len(self.events) - self.height))
        self.map.log = self

    # Add an event to the history. Autoscrolls unless this has been turned off.
    def add(self, event, scroll=True):
        self.events.append(event)
        self.scroller.resize(max(0, len(self.events) - self.height))
        if scroll is True:
            self.scroller.scroll(1)

    def draw(self):
        # Start from the bottom:
        self.y_acc = self.height
        index = 0
        for event in reversed(self.events):
            index += 1
            if index < self.scroller.index:
                continue
            if self.logline(event) is False:
                break;

    def logline(self, event):
        # HACK: What about colors and such? This will fail.
        lines = 1 + (len(event) / self.width) # Number of lines the string will take up
        self.y_acc -= lines # Move up by that much to offset what the function will do.
        # Couldn't fit a whole line.
        if self.y_acc < 0:
            self.y_acc = 0
            self.line("[...]")
            return False;
        self.line(event, None, None, 1) # color, attr, indent
        self.y_acc -= lines # Move to where we started.

    # Accepts keyin to scroll - that's it for now.
    # TODO: Logline highlight stuff.
#    def keyin(self, c):
#        if c == curses.KEY_UP: self.scroll(-1)
#        elif c == curses.KEY_DOWN: self.scroll(1)
#        else: return True
#        return False

 #   # Scrolling the log up and down.
 #   def scroll(self, amt):
 #       self.index += amt
 #       # Prevent an index below zero.
 #       if self.index < 0:
 #           self.index = 0

        # Prevent scrolling if there's no more entries to see.
#        max = len(self.events) - self.height
#        if self.index >= max:
#            self.index = max

class Inventory(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)
        self.items = None
        self.selector = None

    # Just so this doesn't have to be passed in.
    def before_draw(self):
        self.items = self.player.items()

        if self.selector is None:
            self.selector = Selector(self, len(self.items))
        else:
            self.selector.choices = len(self.items)
            self.selector.choice = min(self.selector.choice, self.selector.choices-1)

    def draw(self):
        self.x_acc += 10
        self.cline("Inventory")
        self.y_acc += 3
        if len(self.items) > 0:
            for index, appearance, itemlist in self.items:
                if self.selector.choice == index:
                    self.cline("<green-black>%s (%s)</>" % (appearance, len(itemlist)))
                else:
                    self.cline("%s (%s)" % (appearance, len(itemlist)))
        else:
            self.cline("No items")

        self.y_acc = 0
        self.x_acc += 20

        # TODO: Fix this messaging.
        self.cline("Equipped")
        for loc in sorted(self.player.body.locs.items()):
            equipped = ""
            for held in loc[1].held:
                equipped += "%s (held)" % held.appearance()
            for ready in loc[1].readied:
                equipped += "%s (readied)" % ready.appearance()
            for worn in loc[1].worn:
                equipped += "%s (worn)" % worn.appearance()
            if len(equipped) == 0:
                equipped = "Nothing"
            self.cline("%6s: %s" % (loc[0], equipped))

#        if self.selector.text is not None:
#            self.cline(self.selector.text)
#        else:
#            self.cline("d/e/u")

    def keyin(self, c):
        if c == ord(' '):
            self.parent.children.remove(self)
        elif c == ord('+'):
            self.selector.next()
        elif c == ord('-'):
            self.selector.prev()
        elif c == ord('d'):
            self.selector.toggle(self.player.drop, "Drop item")
        elif c == ord('e'):
            self.selector.toggle(self.player.equip, "Equip item")
        elif c == ord('u'):
            self.selector.toggle(self.player.unequip, "Unequip item")
        elif c == curses.KEY_ENTER or c == ord('\n'):
            if len(self.items) > 0:
                index, appearance, itemlist = self.items[self.selector.choice]
                self.selector.fire(appearance)
        else: return True
        return False

class CharacterSheet(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)
        self.actor = None
        self.text = []
        self.scroller = self.spawn(Scroller())

    def keyin(self, c):
        if c == ord(' '):
            self.suicide()
        else:
            return True
        return False

    def draw(self):
        self.border(" ")
        pos = self.cursor.pos
        actor = self.map.actor(pos)
        self.cline('You can see:')
        self.cline('')
        # Abort early if no actor.
        if actor is None:
            self.cline('Nothing.')
            return True
        if actor != self.actor:
            self.actor = actor
            self.text = self.actor.character_sheet()
            self.scroller.resize(max(0,len(self.text)-self.height))
        for x in range(self.scroller.index, len(self.text)):
            if x > 1 and x == self.scroller.index:
                self.cline('[...]')
                continue
            line = self.text[x]
      #      if len(line) > self.width:
      #          line = line[:self.width]
            self.cline(line)
            if self.y_acc+1 >= self.height and x+2 < len(self.text):
                self.cline('[...]')
                break
        return False # Block further drawing if we drew.

# TODO: Add a minimap and a health screen.
#class MiniMap(View):
#class Health(View):
