import curses

from views.color import Color
from define import *

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
        child.ready()
        return child

    # Abstract. Perform actions that the child couldn't during init.
    def ready(self):
        return True

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

    # Returns true if a screen coordinate cannot be drawn to.
    def undrawable(self, pos):
        x, y = pos
        if x < 0 or y < 0:
            return True
        if x >= TERM_X or y >= TERM_Y:
            return True
        return False

    # Set up curses attributes on a string
    # TODO: Handle anything but basic colors
    def attr(self, color=None, attr=None):
        if color is not None:
            col = Color.pairs.get(color)
            if col is None:
                fg, bg = color.split("-")
                fg = random.choice(Color.colors[fg])
                bg = random.choice(Color.colors[bg])
                col = Color.pairs.get(fg+"-"+bg)
            return curses.color_pair(col)
        return 0

    # KEYIN

    # Recurse through children trying their keyin functions,
    # until you've done your own.
    def _keyin(self, c):
        for child in reversed(self.children):
            if child._keyin(c) is False:
                return False
        return self.keyin(c)

    # Handle keyin. Abstract.
    def keyin(self, c):
        return True
