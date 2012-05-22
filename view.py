from color import Color
from define import *
from hex import *
from skills import skill_list

import curses
import math
import re

from collections import deque
from random import choice

# TODO: Move these only where needed?
from dialogue import chargen
from lifepath import Lifepath
from lifepath_events import eventdata

# Component is the minimal base class. They participate in keyin and draw
# loops, but do not have access to drawing functions.
class Component():
    def __init__(self):
        self.alive = True
        self.children = []
        self.parent = None

    # CREATION / DELETION

    # Spawn a child and return it.
    def spawn(self, child):
        # Some information is passed down for convenience:
        if hasattr(self, 'cursor'):
            child.cursor = self.cursor
        if hasattr(self, 'map'):
            child.map = self.map
        if hasattr(self, 'player'):
            child.player = self.player

        child.parent = self
        self.children.append(child)
        return child

    # Kills children (recursively) and then itself.
    def suicide(self):
        for child in self.children:
            child.suicide()
        if self.parent is not None:
            self.parent.children.remove(self)
        else:
            self.alive = False

    # DRAWING:

    # Draw yourself, then recurse through your children to draw them.
    def _draw(self):
        self._reset()
        self.before_draw()
        if self.draw() is not False:
            for child in self.children:
                if child._draw() is False:
                    return False
            return True
        else:
            return False

    # Reset yourself to prepare for drawing. Abstract.
    def _reset(self):
        return True

    # Do something before drawing yourself. Abstract.
    def before_draw(self):
        return True

    # Draw self. Abstract.
    def draw(self):
        return True

    # TODO: Actually fix this.
    # Returns true if a screen coordinate cannot be drawn to.
    def undrawable(self, pos):
        x, y = pos
        if x < 0 or y < 0:
            return True
        if x >= TERM_X or y >= TERM_Y:
            return True
        return False

    # Set up curses attributes on a string
    # TODO: Handle anything but color
    def attr(self, col, attr=None):
        color = 0
        if col is not None and col is not 0:
            color += Color.pair[col]
        return curses.color_pair(color)

    # KEYIN

    # Recurse through children trying their keyin functions,
    # until you've done your own.
    def _keyin(self, c):
        for child in self.children:
            if child._keyin(c) is False:
                return False
        return self.keyin(c)

    # Handle keyin. Abstract.
    def keyin(self, c):
        return True

class View(Component):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        Component.__init__(self)
        self.screen = window
        self.window = window.subwin(y, x, start_y, start_x)
        self.x = x
        self.y = y
        self.start_x = start_x
        self.start_y = start_y

        # Set up drawing variables (redone each draw)
        self._reset()

    # Resets view-drawing-related variables. Run each draw.
    def _reset(self, margin=(0,0), border=(0,0), padding=(0,0)):
        # Box model.
        margin_x, margin_y = margin
        border_x, border_y = border
        padding_x, padding_y = padding

        edge_x = margin_x + border_x + padding_x
        edge_y = margin_y + border_y + padding_y

        # Available width/height.
        self.width = self.x - 2*(edge_x)
        assert self.width > 0, "Width was below 1 after box model: %s" % self.__dict__
        self.height = self.y - 2*(edge_y)
        assert self.height > 0, "Height was below 1 after box model: %s" % self.__dict__

        # Some references based on width/height, to make placing a bit nicer
        self.TOP = edge_y
        self.BOTTOM = self.height - edge_y - 1
        self.LEFT = edge_x
        self.RIGHT = self.width - edge_x - 1

        # Cumulative x/y tracking.
        self.x_acc = 0
        self.y_acc = 0

    # Rectangular character function.
    def rd(self, pos, glyph, col=0, attr=None):
        x, y = pos
        draw_x = x + self.LEFT
        draw_y = y + self.TOP
        assert self.undrawable((draw_x, draw_y)) is False, "rd function tried to draw out of bounds: %s at %s." % (self.__dict__, (draw_x, draw_y))
        self.window.addch(draw_y, draw_x, glyph, self.attr(col, attr))

    # Rectangular string function.
    def rds(self, pos, string, col=0, attr=None):
        # The max string we could actually fit.
        #max = self.width - self.x_acc
        #assert max > len(string), "rds function tried to print a string that was too long: %s, length %s" % (string, len(string))
        x, y = pos
        draw_x = x + self.LEFT
        draw_y = y + self.TOP
        assert self.undrawable((draw_x, draw_y)) is False, "rds function tried to draw %s out of bounds: %s at %s." % (string, self.__dict__, (draw_x, draw_y))
        self.window.addstr(draw_y, draw_x, string, self.attr(col, attr))

    # Draw a line in rectangular coords - requires linebreaking.
    def rdl(self, pos, line, col=None, attr=None, indent=0):
        # Maximum number of chars we'll try to print in a line.
        max = self.width - self.x_acc - 1

        if len(line) > max:
            list = re.split('(\W+)', line)
            string = ""

            for word in list:
                if len(word) + len(string) > max:
                    self.rds(pos, string, col, attr)
                    pos = add(pos, (0,1))
                    self.y_acc += 1
                    string = " "*indent
                if len(string) == 0 and word.isspace() is True:
                    continue
                string += word
        else:
            string = line

        self.rds(pos, string, col, attr)

    # Draw a simple line; only relevant for text-y views.
    def line(self, string, col=None, attr=None, indent=0):
        pos = (self.x_acc, self.y_acc)
        self.rdl(pos, string, col, attr, indent)
        self.y_acc += 1

    # Print a line with multiple colors
    # TODO: Handle multi-line strings!
    # TODO: Handle other attributes.
    def cline(self, string, col=None, attr=None, indent=0):
        position = 0
        curr_col = col
        substrs = re.split('<(/*\w*-?\w*)>',string)
        for substr in substrs:
            if substr == '':
                continue;
            if substr == '/':
                curr_col = col
            elif Color.pair.get(substr, None) is not None:
                curr_col = substr
            else:
                y_acc = self.y_acc
                pos = (self.x_acc + position, self.y_acc)
                self.rdl(pos, substr, curr_col, attr, indent)
                if y_acc == self.y_acc:
                    position += len(substr)
                else:
                    position = 0
        # Only increment y at the end of the line.
        self.y_acc += 1

    # Simple border function (no margin, border 1, padding 1).
    def border(self, glyph):
        #exit(self.__dict__)
        self.rds((0, 0), glyph*(self.x))
        while self.y_acc < self.y-1:
            self.rd((0, self.y_acc), glyph)
            self.rd((self.x-1, self.y_acc), glyph)
            self.y_acc += 1
        self.rds((0,0), glyph*(self.x-1))
        # Margin, border, padding. Re-calling _reset isn't harmful.
        self._reset((0,0), (1,1), (1,1))

# TODO: Make this a subclass of a Map view.
class MainMap(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)
        self.map = None
        self.player = None
        # -1 to account for 0,0 start
        self.viewport = (int(y/2)-1, int(y/2)-1)
        self.cursor = None

    # Called before the map is rendered, but after it's ready to go.
    def ready(self):
        return

    def keyin(self, c):
        # TODO: Allow multiple open children.
        if not self.children:
            if c == ord('I'):
                self.spawn(Inventory(self.screen, self.width, self.height))
                return False

            elif c == ord('v'):
                if self.cursor is None:
                    self.cursor = self.spawn(Cursor(self.player.pos))
                    self.cursor.cursor = self.cursor # Weird, right? But it can't be passed down automatically because it didn't exist.
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
            else: return True
            return False

    # Hex character function, for maps only.
    def hd(self, pos, glyph, col=0, attr=None):
        # Three sets of coords are involved:
        x, y = pos
        c_x, c_y = self.center#self.player.pos
        v_x, v_y = self.viewport

        # Offsets from the viewport center
        off_x = x - c_x
        off_y = y - c_y

        draw_x = off_y + 2*(off_x+v_x)
        draw_y = off_y + v_y

        assert self.undrawable((draw_x, draw_y)) is False, "hd function tried to draw out of bounds: %s at %s." % (self.__dict__, (draw_x, draw_y))
        self.window.addch(draw_y, draw_x, glyph, self.attr(col, attr))

    # Draw to offset hexes, i.e., the 'blank' ones.
    def offset_hd(self, pos, dir, glyph, col=0, attr=None):
        # Four sets of coords are involved:
        x, y = pos
        c_x, c_y = self.center#self.player.pos
        v_x, v_y = self.viewport
        d_x, d_y = dir

        # Offsets from the viewport center
        off_x = x - c_x
        off_y = y - c_y

        draw_x = off_y + 2*(off_x+v_x) + d_x
        draw_y = off_y + v_y + d_y

        assert self.undrawable((draw_x, draw_y)) is False, "offset hd function tried to draw out of bounds: %s at %s." % (self.__dict__, (draw_x, draw_y))
        self.window.addch(draw_y, draw_x, glyph, self.attr(col, attr))

    # Accepts viewrange offsets to figure out what part of the map is visible.
    def get_glyph(self, pos):
        return self.map.cell(pos).draw()

    def draw(self):
        if self.cursor is not None:
            self.center = self.cursor.pos
        else:
            self.center = self.player.pos

        cells = area(self.map.viewrange, self.center)

        for cell in cells:
            if self.map.valid(cell) is not False:
                glyph, col = self.get_glyph(cell)
                self.hd(cell, glyph, col)
            else:
                glyph = 'X'
                col = "magenta-black"
                #self.hd(cell, glyph, col)

# Main pane class.
class Pane(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)

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
            self.line(string)
        else:
            self.line("There's... nothing there. Nothing at all.")

class Stats(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)

    def draw(self):
        # Col 1: Skeleton/Paperdoll
        # Brevity!
        p = self.player

        self.cline('    <%s>[</>%s<%s>]</>   ' % (p.loccol('Head'), p.wound('Head'), p.loccol('Head')))
        self.cline('  <%s>.--</><%s>+</><%s>--.</> ' % (p.loccol('LArm'), p.loccol('Torso'), p.loccol('RArm')))
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

    # Retrieve stat
    def stat(self, stat):
        return self.player.stat(stat)

    # Print a line like 'Dodge: 15' using stat()
    def statline(self, stat):
#        self.line("HP: %3d/%2d" % (-50, 10))
#        self.line("FP: %3d/%2d" % (10, 12))
#        self.line("MP: %3d/%2d" % (8, 15))

        # Always use the shortest label here.
        short = labels.get(stat)
        if short is not None:
            short = short[0]

        # Alternate draw for these stats.
        if short in ["HP", "FP", "MP"]:
            self.line("%s: %3d/%2d" % (short, self.stat(stat), self.stat("Max"+stat)))
        else:
            self.line("%s: %s" % (short, self.stat(stat)))

# TODO: Chargen actually affects stats.
class Chargen(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)
        self.player = None
        self.lifepath = Lifepath()
        self.current = None
        self.toggle_events = False
        self.selected = 0
        self.selections = []
        self.max = len(self.lifepath.first)-1

    def scroll(self, amt):
        self.selected += amt

        if self.selected < 0:
            self.selected = 0

        if self.selected >= self.max:
            self.selected = self.max

    def next(self, choice=None):
        if choice is None:
            choice = self.current.choices[self.selected]

        if self.current is not None:
            self.current.choose(choice)
            self.current = self.current.child
            self.lifepath.events.append(self.current)
        else:
            self.lifepath.start(choice)
            self.current = self.lifepath.first
        # TODO: Handle appending inside of choose()
        self.reset_choices()


    def prev(self):
        if self.current.parent is not None:
            self.current.undo()
            self.current = self.current.parent
            self.lifepath.events.pop()
            self.reset_choices(True)
        else:
            self.current.undo()
            self.current = None
            self.lifepath.events.pop()
            self.lifepath.first = self.lifepath.skip
            self.reset_choices(True)

    def reset_choices(self, restore=False):
        # Reset selection:
        if restore is False:
            self.selections.append(self.selected)
            self.selected = 0
        else:
            self.selected = self.selections.pop()

        # Reset number of choices:
        if self.current is not None:
            if self.current.choices is not None:
                self.max = len(self.current.choices)-1
        else:
            self.max = len(self.lifepath.skip)-1

    def draw(self):
        # Character pane:
        self.x_acc = 60
        self.y_acc = 4
        # TODO: Don't calculate this each time, jeez!
        self.cline("Your character:")
        if self.current is not None:
            self.player.character = self.lifepath.effects()
            for key, value in self.player.character.items():
                self.cline("%s: %s" % (key, value))#: %s" % (stat, value))

        # Top part of the screen:
        self.x_acc = 0
        self.y_acc = 0

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
            # TODO: Duplicated code.
            for event in self.lifepath.events:
                # We only want events with short descriptions. If they take a certain number of years, list that.
                if event.short is not None:
                    string = "You %s" % event.short
                    if event.years is not None:
                        string += " "
                        if event.years == 1:
                            string += "(%s year)" % event.years
                        else:
                            string += "(%s years)" % event.years
                    self.cline(string+".")
            old = self.y_acc
            self.y_acc = level


        # Bottom part of the screen:
        self.y_acc = self.height - 8
        y_save = self.y_acc

        # Print a list of choices for the initial skip.
        if self.current is None:
            # Start with just enough room to list everything and save where we started.
            for x in range(len(self.lifepath.skip)):
                if x == self.selected:
                    self.cline("<green-black>* %s</>" % self.lifepath.skip[x][0])
                else:
                    self.line("* %s" % self.lifepath.skip[x][0])
        # Prints a list of choices for the current event.
        elif self.current.choices is not None:
            for choice in self.current.choices:
                if self.current.choices[self.selected] == choice:
                    self.cline("<green-black>* %s</>" % choice)
                else:
                    self.line("* %s" % choice)
        # Prints the final choice: whether to start.
        else:
            self.y_acc = self.height-1
            self.cline("<red-black>Really use this lifepath? You can't change it once you've started the game.</>")

        # Go back up to where we started, but this time, to the right.
        self.y_acc = y_save
        self.x_acc = 25

        # Print the text from the currently highlighted event.
        if self.current is None:
            self.line(self.lifepath.first[self.selected][1])
        else:
            if self.current.choices is not None:
               self.cline(eventdata.get(self.current.choices[self.selected], {'text': '<DEBUG: NO TEXT>'})['text'])

        if self.toggle_events is True:
            self.x_acc = 0
            self.y_acc = self.height / 3
            self.cline("%s" % "-"*self.width)
            self.cline("Your life so far:")
            self.cline("")
            line = ""
            for event in self.lifepath.events:
                # We only want events with short descriptions. If they take a certain number of years, list that.
                if event.short is not None:
                    string = "%s" % event.short
                    if event.years is not None:
                        string += " "
                        if event.years == 1:
                            string += "(%s year)" % event.years
                        else:
                            string += "(%s years)" % event.years
                    line += string+" -> "
            line += "?\n"
            self.cline(line)
            self.y_acc += 4
            self.cline("%s" % "-"*self.width)

        # Don't draw anything else.
        return False

    # TODO: Duplicated code.
    def keyin(self, c):
        # Show a list of events so far.
        if c == ord('?'):
            if self.toggle_events is True:
                self.toggle_events = False
            else:
                self.toggle_events = True
            return False
        # Make the first choice, which uses a different system to
        # skip ahead several steps in the chargen system.
        if self.current is None:
            if c == curses.KEY_ENTER or c == ord('\n'):
                # TODO: Move this into lifepath code!
                # Each particular skip choice comes with a predetermined list of choices to make.
                choices = self.lifepath.skip[self.selected][2]
                # Everyone starts at Start.
                self.next('Start')
                # After that, follow the choices.
                for choice in choices:
                    self.next(choice)
            elif c == curses.KEY_UP:
                self.scroll(-1)
            elif c == curses.KEY_DOWN:
                self.scroll(1)
            else: return True
            return False
        # Choicely choosing the next choice from choices
        elif self.current.choices is not None:
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
                self.suicide()
            elif c == ord(' '):
                self.prev()
            else: return True
            return False

# TODO: Add a minimap and a health screen.
#class MiniMap(View):
#class Health(View):

# TODO: Implement this
class Status(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)

    def draw(self):
        self.line("")
#        self.line("")
#        self.line("Pain", "red-black")
#        self.line("Shock", "magenta-black")

# Very hackish right now: events added through map...
class Log(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)
        self.events = deque()
        self.index = 0

    # Add an event to the history. Autoscrolls unless this has been turned off.
    def add(self, event, scroll=True):
        self.events.append(event)
        if scroll is True:
            self.scroll(1)

    def draw(self):
        # Start from the bottom:
        self.y_acc = self.height
        for event in reversed(self.events):
            if self.logline(event) is False:
                break;

    def logline(self, event):
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
    def keyin(self, c):
        if c == curses.KEY_UP: self.scroll(-1)
        elif c == curses.KEY_DOWN: self.scroll(1)
        else: return True
        return False

    # Scrolling the log up and down.
    def scroll(self, amt):
        self.index += amt
        # Prevent an index below zero.
        if self.index < 0:
            self.index = 0

        # Prevent scrolling if there's no more entries to see.
        max = len(self.events) - self.height
        if self.index >= max:
            self.index = max


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
                    self.cline("<green-black>%s - %s (%s)</>" % (index, appearance, len(itemlist)))
                else:
                    self.cline("%s - %s (%s)" % (index, appearance, len(itemlist)))
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

        if self.selector.text is not None:
            self.cline(self.selector.text)
        else:
            self.cline("d/e/u")

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

# Cycling selector.
class Selector():
    def __init__(self, parent, choices, initial=0):
        self.parent = parent
        self.choices = choices
        self.choice = initial
        self.action = None
        self.text = None

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

    def fire(self, arg):
        if self.action is not None:
            self.action(arg)

    def toggle(self, action, text):
        if self.action == action:
            self.action = None
            self.text = None
        else:
            self.action = action
            self.text = text

class Cursor(Component):
    styles = {
        "braces" : [("{", WW), ("}", EE)],
    }

    def __init__(self, pos):
        Component.__init__(self)
        self.pos = pos
        self.style = "braces"

    def keyin(self, c):
        if c == ord(' '):
            self.parent.cursor = None
            self.suicide()
        elif c == ord('7'):
            self.scroll(NW)
        elif c == ord('4'):
            self.scroll(CW)
        elif c == ord('1'):
            self.scroll(SW)
        elif c == ord('9'):
            self.scroll(NE)
        elif c == ord('6'):
            self.scroll(CE)
        elif c == ord('3'):
            self.scroll(SE)
        else: return True
        return False

    # Move the cursor (hexagonally).
    def scroll(self, dir):
        self.pos = add(self.pos, dir)

    def draw(self):
        color = self.color()
        for glyph, dir in Cursor.styles[self.style]:
            self.parent.offset_hd(self.pos, dir, glyph, color)

    # This is a function so that the cursor color can change in response to
    # the hex that it's targeting.

    # TODO: ask the cells how they want to be drawn, instead.
    def color(self):
        cell = self.map.cell(self.pos)
        if cell is not None:
            if cell.actor is not None:
                if cell.actor.controlled is True:
                    return "green-black"
                else:
                    return "red-black"
            else:
                if cell.terrain or cell.items:
                    return "yellow-black"
                else:
                    return "magenta-black"

class CharacterSheet(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)

    def keyin(self, c):
        if c == ord(' '):
            self.suicide()
        else:
            return True
        return False

    def draw(self):
        self.border("~")
        #self.window.bkgd("_", self.attr("white-black"))
        pos = self.cursor.pos
        actor = self.map.actor(pos)
        if actor is None:
            return True

        # TODO: Make this a describe method of the actor.
        # Print out a character sheet:
        self.cline("Viewing %s" % actor.name)
        self.cline("")
        self.cline("--Attributes--")
        for stat, points in actor.attributes.items():
            self.cline("%s: %s" % (stat, points))
        self.cline("")
        self.cline("--Points--")
        for skill, points in actor.points["skills"].items():
            self.cline("%s: %s points" % (skill, points))
        #self.cline("")
        #self.cline("--Skill Ranks--")
        #for skill, info in actor.skills.items():
        #    self.cline("%s (%s/%s): %s%+d" % (skill, labels[skill_list[skill]["attribute"]], labels[skill_list[skill]["difficulty"]], labels[info[0]], info[1]))
        #self.cline("")
        #self.cline("--Skill Levels--")
        #for skill, level in actor.base_skills.items():
        #    str = "%s (%s/%s) - %s" % (skill, labels[skill_list[skill]["attribute"]], labels[skill_list[skill]["difficulty"]], level[0])
        #    if level[1] is not False:
        #        str += " " + "(default: %s%d)" % (level[1][0], level[1][1])
        #    self.cline(str)
