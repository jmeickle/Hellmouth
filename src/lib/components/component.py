import curses

from src.lib.util.color import Color
from src.lib.util.define import *
from src.lib.util import key
import random

# Component is the minimal base class. They participate in keyin and draw
# loops, but do not have direct access to drawing functions.
class Component():
    def __init__(self):
        self.alive = True
        self.children = []
        self.parent = None
        self.prompt = False

    # CREATION / DELETION

    # Spawn a child and return it.
    def spawn(self, child):
        self.children.append(child)
        child.parent = self
        child.inherit()
        child.ready()
        return child

    # Pass on values that need to be shared across components.
    def inherit(self):
        if self.parent is not None:
            if hasattr(self.parent, 'cursor'):
                self.cursor = self.parent.cursor
            if hasattr(self.parent, 'map'):
                self.map = self.parent.map
            if hasattr(self.parent, 'zoom'):
                self.zoom = self.parent.zoom
            if hasattr(self.parent, 'player'):
                self.player = self.parent.player

        for child in self.children:
            child.inherit()

    # Abstract. Perform actions that the child couldn't during init.
    def ready(self):
        return True

    # Kills children (recursively) and then itself.
    def suicide(self):
        self.alive = False
        for child in self.children:
            child.suicide()
        if self.parent is not None:
            self.parent.children.remove(self)

    # DRAWING:

    # Draw yourself, then recurse through your children to draw them.
    def _draw(self):
        self._reset()
        self.before_draw()
        if self.draw() is not False:
            for child in reversed(self.children):
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
    # TODO: Replace with a curses mixin
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
#        if self.parent is not None and self.prompt is False:
#            if c < 256:
#                if key.globals.get(c) is True:
#                    return None
        return self.keyin(c)

    # Handle keyin. Abstract.
    def keyin(self, c):
        return True

    # Recurse through children trying their keyin functions,
    # until you've done your own.
    def _event(self, e):
        for child in reversed(self.children):
            if child._event(e) is False:
                return False
        return self.event(e)

    # Handle keyin. Abstract.
    def event(self, e):
        return True

    def loop(self):
        # Draw tree.
        self.window.erase()
        self._draw()
        self.window.refresh()

        # Keyin tree.
        c = self.window.getch()
        self._keyin(c)

        # Event processing tree.
        e = key.event(c)
        self._event(e)

        # Die if no children left.
        if not self.children:
            self.alive = False

# The first component called, containing window information.
class RootComponent(Component):
    def __init__(self, window):
        Component.__init__(self)
        self.window = window

    def launch(self, module):
        # Import the chosen game module (in the form of src.games.__GAMEMODE__.main.py).
        # TODO: Permit a classname other than 'Game'
        module_name, module_info = module
        gamemodule = __import__('src.games.%s.main' % module_name, globals(), locals(), ['Game'])
 
        # Spawn the game as a child process and then launch it.
        self.spawn(gamemodule.Game()).launch()