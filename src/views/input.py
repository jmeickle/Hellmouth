import curses

from component import Component
from views.view import View
from define import *
from hex import *
from collections import deque

class Scroller(Component):
    def __init__(self, max=0, min=0, initial=0):
        Component.__init__(self)
        self.min = min
        self.max = max
        self.index = initial

    def resize(self, max_sz, min_sz=0):
        self.min = max(0,min_sz)
        self.max = max(0,max_sz)
        self.scroll(0)

    def scroll(self, amt):
        self.index += amt
        if self.min is not None:
            if self.index < self.min:
                self.index = self.min
        if self.max is not None:
            if self.index > self.max:
                self.index = self.max

    def keyin(self, c):
        if c == curses.KEY_UP: self.scroll(-1)
        elif c == curses.KEY_DOWN: self.scroll(1)
        else:
            return True
        return False

# Same as a scroller, but only left/right.
class SideScroller(Scroller):
    def keyin(self, c):
        if c == curses.KEY_LEFT: self.scroll(-1)
        elif c == curses.KEY_RIGHT: self.scroll(1)
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
        "<>"  : [("<", WW), (">", EE)],
        "{}"  : [("{", WW), ("}", EE)],
        "[]"  : [("[", WW), ("]", EE)],
        "()"  : [("(", WW), (")", EE)],
        # TODO: Make 1hex prettier using unicode.
        "1hex" : [("^", NN), ("v", SS), ("|", EE), ("|", WW)],
        "2hex" : [
            ("/", add(WW,add(NW,WW))),#add(NW, add(NW, NW))),
            ("\\", add(NE, EE)),
            ("|", add(EE,add(EE, EE))),
            ("|", add(WW, add(WW, WW))),
            ("\\", add(SW, WW)),
            ("/", add(EE,add(EE, SE)))
        ],
    }

    def __init__(self, pos, style="1hex"):
        Component.__init__(self)
        self.pos = pos
        self.styles = deque(["1hex", "<>", "{}", "[]", "()"])
        self.style = self.styles[0]

    def keyin(self, c):
        if c == ord(' '):
            self.parent.cursor = None
            self.suicide()
        elif c == ord('-'):
            self.styles.rotate(-1)
            self.style = self.styles[0]
        elif c == ord('+'):
            self.styles.rotate(1)
            self.style = self.styles[0]
        # TODO: Replace by hexdirs code
        elif c == ord('5'):
            self.scroll(CC)
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

# Makes a cool hex-y radial menu thing. Useless for now.
#        if self.style == "2hex":
#            for dir in dirs:
#                dir = (dir[0]*3, dir[1]*3)
#                for glyph, offset in Cursor.styles[self.style]:
#                    self.parent.offset_hd(add(self.pos, dir), offset, glyph, color)

        for glyph, offset in Cursor.styles[self.style]:
            self.parent.offset_hd(self.pos, offset, glyph, color)

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

# Generic prompt.
class Prompt(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y/2, start_x, start_y + y/4)
        self.prompt = True

    def ready(self):
        self.scroller = self.spawn(Scroller())

    def draw(self):
        self.window.clear()
        self.border("/")

# Text entry prompt.
class TextPrompt(Prompt):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        Prompt.__init__(self, window, x, y/2, start_x, start_y + y/4)
        self.input = ""
        self.max = 0

    def ready(self):
        self.scroller = self.spawn(SideScroller())

    def draw(self):
        Prompt.draw(self)
        # HACK: This is a guesstimate until I make the text functions more consistent.
        self.max = self.width * (self.height - 1)

        text = self.input[:self.scroller.index]
        if self.scroller.index < self.scroller.max:
            text += "<black-white>%s</>" % self.input[self.scroller.index]
        if len(self.input) > 1:
            text += self.input[self.scroller.index+1:]
        if self.scroller.index == self.scroller.max:
            text += "<black-white>_</>"
        self.cline(text)

    def keyin(self, c):
        if c == curses.KEY_ENTER or c == ord("\n"):
            self.suicide()
        elif c == curses.KEY_BACKSPACE:
            self.backspace()
        elif c == curses.KEY_DC:
            self.delete()
        elif c < 256:
            self.write(c)
        return False

    def write(self, c):
        if len(self.input) == self.max:
            return False
        left = self.input[:self.scroller.index]
        right = self.input[self.scroller.index:]
        self.input = left + chr(c) + right
        self.scroller.resize(len(self.input))
        self.scroller.index += 1

    def backspace(self):
        if self.scroller.index == 0:
            return False
        left = self.input[:self.scroller.index-1]
        right = self.input[self.scroller.index:]
        self.input = left + right

        self.scroller.resize(len(self.input))
        if self.scroller.index != self.scroller.max:
            self.scroller.index -= 1

    def delete(self):
        if self.scroller.index == self.scroller.max:
            return False

        left = self.input[:self.scroller.index]
        right = self.input[self.scroller.index+1:]
        self.input = left + right

        self.scroller.resize(len(self.input))

class ItemPrompt(Prompt):
    def __init__(self):
        Prompt.__init__(self)


