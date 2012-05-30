import curses

from views.view import View
from views.screens import Screen
from views.input import *

from define import *
from hex import *
from data.skills import skill_list

from collections import deque
from random import choice

from text import *

import log

# Main tactical window class.
class Window(View):
    def __init__(self, window):
        View.__init__(self, window, TERM_X, TERM_Y)

    def ready(self):
        self.spawn(SidePane(self.screen))
        self.spawn(MainPane(self.screen))

# Larger, left-hand pane
class MainPane(View):
    def __init__(self, window):
        View.__init__(self, window, MAP_X, MAP_Y, MAP_START_X, MAP_START_Y)

    def ready(self):
        self.spawn(MainMap(self.screen, MAP_X, MAP_Y, MAP_START_X, MAP_START_Y))
        self.spawn(Status(self.screen, STATUS_X, STATUS_Y, STATUS_START_X, PANE_START_Y))

# Smaller, right-hand pane
class SidePane(View):
    def __init__(self, window):
        View.__init__(self, window, PANE_X, PANE_Y, PANE_START_X, PANE_START_Y)

    def ready(self):
        self.spawn(Stats(self.screen, PANE_X, STATS_Y, PANE_START_X, PANE_START_Y))
        self.spawn(LogViewer(self.screen, PANE_X, LOG_Y, PANE_START_X, LOG_START_Y))

# TODO: Make this a subclass of a Map view, to account for tactical/strategic/etc.
class MainMap(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)
        # -1 to account for 0,0 start
        self.viewport = (int(y/2)-1, int(y/2)-1)
        self.viewrange = 10
        self.cursor = None

    def keyin(self, c):
        if c == ord('G') or c == ord('g'):
            self.player.get_all()
            return False

#        if c == ord('g'):
#            if len(self.map.player.cell().items) > 1:
#                self.spawn(ItemPrompt(self.screen, self.width, self.height))
#            else:
#                self.map.player.get_all()
#            return False

        # TODO: Allow multiple open children.
        if not self.children:
            if c == ord('I'):
                self.spawn(Inventory(self.screen, self.width, self.height))
                return False

            elif c == ord('v'):
                if self.cursor is None:
                    self.cursor = self.spawn(Cursor(self.player.pos))
                    self.cursor.spawn(Examine(self.screen, self.width, 1, 0, self.BOTTOM))
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

        if len(self.player.highlights) > 0:
            for highlight, pos in self.player.highlights.items():
                if dist(self.center, pos) > self.viewrange:
                    cells = line(self.center, pos, self.viewrange+1)
                    cell = cells.pop()
                    glyph, col = "*", "red-black"
                    self.hd(cell, glyph, col)

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
            self.line("Cursor: %s" % string)
        else:
            self.line("Cursor: There's... nothing. Nothing at all.")

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
class LogViewer(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)
        self.autoscroll = True
        self.events = 0

    # Spawn a scroller and add the log to the map.
    def ready(self):
        for x in range(50):
            log.add("Test Message %s" % x)
        self.scroller = self.spawn(Scroller(log.length() - self.height))

    def before_draw(self):
        if log.length() > self.events:
            max_scroll = max(0, log.length() - self.height)
            self.scroller.resize(max_scroll)
            if self.autoscroll is True:
                self.scroller.scroll(log.length() - self.events)
            self.events = log.length()

    def draw(self):
        # Start from the bottom:
        self.y_acc = self.height
        index = self.scroller.max

        if self.scroller.index != self.scroller.max:
            self.y_acc -=1
            self.line("[...]")
            self.y_acc -=1
            index += 1

        for event in reversed(log.events()):
            index -= 1
            if index >= self.scroller.index:
                continue
            if self.logline(event) is False:
                self.y_acc = 0
                self.line("[...]")
                break;

    def logline(self, event):
        lines = wrap_string([event], self.width)

        # Move up by that much to offset what the line function would do.
        self.y_acc -= len(lines)

        # Couldn't fit it all.
        if self.y_acc < 1 and self.scroller.index != self.scroller.min:
            return False;

        # Otherwise, display the line(s):
        for line in lines:
            self.line(line)

        # Since we're moving in reverse.
        self.y_acc -= len(lines)

class Inventory(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)

    def ready(self):
        self.scroller = self.spawn(Scroller())
        self.sidescroller = self.spawn(SideScroller(1))

    # Stored here for convenience.
    def before_draw(self):
        self.items = self.player.list_carried()
        self.slots = self.player.body.locs.items()

        # Tabbing! (Very hackish/simple.)
        if self.sidescroller.index == 0:
            self.scroller.resize(len(self.items)-1)
        else:
            self.scroller.resize(len(self.slots)-1)

    def draw(self):
        self.window.clear()
        self.border(" ")
        self.cline("Inventory")
        self.y_acc += 1
        if len(self.items) > 0:
            for x in range(len(self.items)):
                appearance, items = self.items[x]
                if len(items) > 1:
                    string = "%d %ss" % (len(items), appearance)
                else:
                    string = appearance

                # Highlight tab, if present.
                if self.sidescroller.index == 0 and x == self.scroller.index:
                    self.cline("<green-black>%s</>" % string)
                else:
                    self.cline(string)
        else:
            self.cline("No items")

        self.y_acc += 1

        # Print what's on the ground, too.
        ground = self.map.player.cell().items
        if len(ground) > 0:
            self.cline("Ground:")
            self.y_acc += 1
            for appearance, items in ground.items():
                if len(items) > 1:
                    self.line("%d %ss" % (len(items), appearance))
                else:
                    self.line(appearance)

        self.y_acc = 0
        self.x_acc += 20

        # TODO: Fix this messaging.
        self.cline("Equipped")
        self.y_acc += 1
        for x in range(len(self.slots)):
            locname, loc = self.slots[x]
            equipped = ""
            for appearance, items in loc.readied.items():
                for item in items: # Ick. Definitely need to move this printing!
                    if item.is_wielded():
                        equipped += "%s (wielded)" % appearance
                    else:
                        equipped += "%s (readied)" % appearance
            for appearance, items in loc.held.items():
                for item in items:
                    if not item.is_wielded():
                        equipped += "%s (held)" % appearance
            for appearance, items in loc.worn.items():
                for item in items:
                    equipped += "%s (worn)" % appearance

            # If we don't have a string yet:
            if len(equipped) == 0:
                    equipped = "Nothing"

            # Highlights.
            if self.sidescroller.index == 1 and x == self.scroller.index:
                self.cline("%6s: <green-black>%s</a>" % (locname, equipped))
            else:
                self.cline("%6s: %s" % (locname, equipped))

        self.x_acc = 0
        self.y_acc = self.BOTTOM - 2

        self.cline("Available actions:")
        actions = []
        # These actions depend on having a carried item.
        if self.sidescroller.index == 0 and len(self.items) > 0:
            appearance, items = self.items[self.scroller.index]
            if self.map.player.can_equip_item(appearance, self.player.body.locs.get(self.player.body.primary_slot)):
                actions.append("(<green-black>e</>)quip")

        elif self.sidescroller.index == 1:
            locname, loc = self.slots[self.scroller.index]
            #for item in loc.items():
            # Hackish! Pop a random element from the set.
            items = loc.items()
            if len(items) > 0:
                item = loc.items().pop()
                if self.player._can_unequip_item(item):
                    actions.append("(<green-black>u</>)nequip")

        item = self.selected()
        if item is not None:
            if self.sidescroller.index == 0:
                if self.player.can_drop_item(item):
                    actions.append("(<green-black>d</>)rop")
            elif self.sidescroller.index == 1:
                if self.player._can_drop_item(item):
                    actions.append("(<green-black>d</>)rop")

        # Always visible, if there are items to get.
        if self.player.can_get_items():
            actions.append("(<green-black>G</>)et all")

        self.cline("  %s" % commas(actions))

    # Returns the seletected item (or appearance).
    def selected(self):
        if self.sidescroller.index == 0 and len(self.items) > 0:
            appearance, items = self.items[self.scroller.index]
            return appearance
        elif self.sidescroller.index == 1:
            locname, loc = self.slots[self.scroller.index]
            #for item in loc.items():
            # Hackish! Pop a random element from the set.
            items = loc.items()
            if len(items) > 0:
                return items.pop()

    def keyin(self, c):
        if c == ord(' '):
            self.suicide()
        # Hack.
        elif c == ord('d'):
            if self.scroller.index == 0:
                self.player.drop(self.selected())
            else:
                self.player._drop(self.selected())
        elif c == ord('e'):
            self.player.equip(self.selected())#, self.player.body.locs.get(self.player.body.primary_slot))
        elif c == ord('u'):
            # This is also a hack.
            self.player._unequip(self.selected())
#        else: return True
        elif c == ord('G') or c == ord('g'):
            self.player.get_all()
            return False
        return False

class CharacterSheet(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)
        self.actor = None
        self.text = []

    def ready(self):
        self.scroller = self.spawn(Scroller(0))

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

        # Abort early if no actor.
        if actor is None:
            self.cline("There's nothing interesting here.")
            return False

        self.cline('You can see: %s' % actor.name)
        self.cline("-"*self.width)

        if actor != self.actor:
            self.actor = actor
            self.text = wrap_string(self.actor.character_sheet(), self.width)
            self.scroller.resize(len(self.text)-self.height + 2) # To account for the possibility of hidden lines

        offset = 0

        if self.scroller.index > 0:
            self.cline('[...]')
            offset += 1

        maxlines = self.height - self.y_acc
# TODO: Generalize this.
        for x in range(maxlines):
            if self.y_acc+1 == self.height and self.scroller.index < self.scroller.max:
                self.cline('[...]')
                break;

            index = self.scroller.index + x + offset
            line = self.text[index]
            self.cline(line)
        return False # Block further drawing if we drew.

# TODO: Add a minimap and a health screen.
#class MiniMap(View):
#class Health(View):
