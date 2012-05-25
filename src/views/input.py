import curses

from component import Component
from define import *
from hex import *

class Scroller(Component):
    def __init__(self, max=0, min=0, initial=0):
        Component.__init__(self)
        self.min = min
        self.max = max
        self.index = initial

    def resize(self, max, min=0):
        self.min = min
        self.max = max
        self.scroll(0)

    def scroll(self, amt):
        self.index += amt
        if self.min is not None:
            if self.index < self.min:
                self.index = self.min
        if self.max is not None:
            if self.index >= self.max:
                self.index = self.max

    def keyin(self, c):
        if c == curses.KEY_UP or c == ord('-'): self.scroll(-1)
        elif c == curses.KEY_DOWN or c == ord('+'): self.scroll(1)
        else:
            return True
        return False

# Cycling selector.
class Selector():
    def __init__(self, parent, choices=None, initial=0):
        self.parent = parent
        self.choices = choices
        self.choice = initial

    # Jump to a specific value, if it's valid.
    def jump(self, choice):
        if choice < len(self.choices):
            self.choice = choice

    # Scroll in either direction.
    def scroll(self, amt=1):
        self.choice += amt
        if self.choice < 0:
            self.choice = self.choices-1
        elif self.choice >= len(self.choices):
            self.choice = 0

    def choose(self):
        if self.choices is None:
            self.parent.callback()
        else:
            self.parent.callback(self.choice)

#    def fire(self, arg):
#        if self.action is not None:
#            self.action(arg)

#    def toggle(self, action, text):
#        if self.action == action:
#            self.action = None
#            self.text = None
#        else:
#            self.action = action
#            self.text = text

class Cursor(Component):
    styles = {
        "<>" : [("<", WW), (">", EE)],
        "{}" : [("{", WW), ("}", EE)],
        "[]" : [("[", WW), ("]", EE)],
        "()" : [("[", WW), ("]", EE)],
    }

    def __init__(self, pos, style="{}"):
        Component.__init__(self)
        self.pos = pos
        self.style = style

    def keyin(self, c):
        if c == ord(' '):
            self.parent.cursor = None
            self.suicide()
        # TODO: Replace by hexdirs code
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
                return cell.actor.cursor_color()
            else:
                if cell.terrain or cell.items:
                    return "yellow-black"
                else:
                    return "magenta-black"

    # Seems silly, but this lets the cursor be passed on automatically to
    # children of it. (This can't be done during spawn, of course.)
    def ready(self):
        self.cursor = self
