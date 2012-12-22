import curses

from src.lib.util.component import Component
from src.lib.util.define import *
from src.lib.util.hex import *
from src.lib.util.key import *

from view import View

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

# Primary cycling selector, controlled with + and -.
class Selector(Scroller):
    def keyin(self, c):
        if c == ord('+'): self.scroll(1)
        elif c == ord('-'): self.scroll(-1)
        else:
            return True
        return False

    # Jump to a specific value, if it's valid.
    def scroll_to(self, choice):
        if choice <= self.max and choice >= self.min:
            self.index = choice

    # Scroll, but loop back if necessary.
    def scroll(self, amt):
        self.index += amt
        if self.min is not None:
            if self.index < self.min:
                self.index = self.max
        if self.max is not None:
            if self.index > self.max:
                self.index = self.min

# Primary cycling selector, controlled with / and *.
class SecondarySelector(Selector):
    def keyin(self, c):
        if c == ord('/'): self.scroll(1)
        elif c == ord('*'): self.scroll(-1)
        else:
            return True
        return False

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

# Makes a cool hex-y radial menu thing. Useless for now.
#        if self.style == "2hex":
#            for dir in dirs:
#                dir = (dir[0]*3, dir[1]*3)
#                for glyph, offset in Cursor.styles[self.style]:
#                    self.parent.offset_hd(add(self.pos, dir), offset, glyph, color)

    def __init__(self, pos):
        Component.__init__(self)
        self.pos = pos
        self.styles = ["[]", "1hex", "<>", "{}", "()"]

    def keyin(self, c):
        # TODO: Dup code.
        pos = self.pos
        cell = self.map.cell(pos)
        if cell is not None:
            if cell.actors:
                actor = cell.actors[self.selector.index]
                for command in actor.list_commands():
                    if cmd(c, command):
                        self.player.perform(command, actor)
                        return False
        if cmd(c, CMD_HEX):
            self.scroll(hexkeys(c))
        elif cmd(c, CMD_CANCEL):
            self.parent.cursor = None
            self.suicide()
        else: return True
        return False

    # Move the cursor (hexagonally).
    def scroll(self, dir):
        self.pos = add(self.pos, dir)
        self.resize()

    def draw(self):
        pos = self.pos
        cell = self.map.cell(pos)
        color = "black-black"
        
        if cell is not None:
            if cell.actors:
                actor = cell.actors[self.selector.index]
                color = actor.cursor_color()
                # HACK: Magic number
                if self.zoom == 2:
                    pos = add(pos, actor.subposition)
            elif cell.terrain or cell.items:
                color = "yellow-black"
            else:
                color = "magenta-black"

        for glyph, offset in Cursor.styles[self.styles[self.secondary.index]]:
            self.parent.offset_hd(pos, offset, glyph, color)

    def ready(self):
        # Seems silly, but this lets the cursor be passed on automatically to
        # children of it. (This can't be done during spawn, of course.)
        self.cursor = self
        self.selector = self.spawn(Selector())
        self.secondary = self.spawn(SecondarySelector(len(self.styles)-1))
        self.resize()

    # Resize based on features.
    def resize(self):
        actors = self.map.actors(self.pos)
        self.selector.resize(len(actors)-1)

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


