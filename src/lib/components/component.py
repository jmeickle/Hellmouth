"""Components are the minimal base user interface class. They participate in
keyin and draw loops, but do not have direct access to drawing methods."""

import curses

from src.lib.util.color import Color
from src.lib.agents.contexts.context import Context
from src.lib.util.define import *
from src.lib.util import key
import random

class Component(object):
    """An interface Component taking part in UI control flow."""
    def __init__(self):
        self.alive = True
        self.children = []
        self.parent = None
        self.prompt = False

    def spawn(self, child):
        """Spawn a child and return it."""
        self.children.append(child)
        child.parent = self
        child.inherit()
        child.ready()
        return child

    def inherit(self):
        """Pass on values that need to be shared across components."""
        # TODO: Dependency injection?
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

    def ready(self):
        """Abstract. Perform actions that the child couldn't during init."""
        return True

    def suicide(self):
        """Recursively kill this Component's children, and then itself."""

        for child in self.children:
            child.suicide()
        if self.parent is not None:
            self.parent.children.remove(self)
        self.alive = False

    def _draw(self):
        """Draw yourself, then recurse through your children to draw them."""
        self._reset()
        self.before_draw()
        if self.draw() is not False:
            for child in reversed(self.children):
                if child._draw() is False:
                    return False
            return True
        else:
            return False

    def _reset(self):
        """Abstract. Reset yourself to prepare for drawing."""
        pass

    def before_draw(self):
        """Abstract. Do something before drawing yourself."""
        pass

    def draw(self):
        """Abstract. Draw self."""
        pass

    def undrawable(self, pos):
        """Returns true if a screen coordinate cannot be drawn to."""
        x, y = pos
        if x < 0 or y < 0:
            return True
        if x >= TERM_X or y >= TERM_Y:
            return True
        return False

    def attr(self, color=None, attr=None):
        """Set up curses attributes on a string."""
        # TODO: Handle anything but basic colors
        # TODO: Replace with a curses mixin
        if color is not None:
            col = Color.pairs.get(color)
            if col is None:
                fg, bg = color.split("-")
                fg = random.choice(Color.colors[fg])
                bg = random.choice(Color.colors[bg])
                col = Color.pairs.get(fg+"-"+bg)
            return curses.color_pair(col)
        return 0

    def _keyin(self, c):
        """Recurse through children trying their keyin functions until you've
        done your own."""
        for child in reversed(self.children):
            if child._keyin(c) is False:
                return False
        # TODO: Remove?
#        if self.parent is not None and self.prompt is False:
#            if c < 256:
#                if key.globals.get(c) is True:
#                    return None
        return self.keyin(c)

    def keyin(self, c):
        """Abstract. Handle keyin."""
        return True

    def _event(self, e):
        """Recurse through children trying their keyin functions until you've
        done your own."""
        for child in reversed(self.children):
            if child._event(e) is False:
                return False
        return self.event(e)

    def event(self, e):
        """Abstract. Handle keyin."""
        return True

    def loop(self):
        """Loop drawing, keyin, and event processing through this Component and
        into its children."""
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

    def get_context(self, **kwargs):
        """Build a Context for this Component."""
        # TODO: Rename?
        context_class = kwargs.pop("context_class", Context)

        kwargs["agent"] = kwargs.get("agent", self.player)
        kwargs["intent"] = kwargs.get("intent", {"attempt" : True})
        kwargs["component"] = kwargs.get("component", self)

        return context_class(**kwargs)

class RootComponent(Component):
    """The first component called, containing window information."""
    def __init__(self, window):
        Component.__init__(self)
        self.window = window

    def launch(self, selected_module):
        """Spawn the selected module's main.Game as a child Component and then
        launch it."""
        # Import the chosen game module (as src.games.__GAMEMODE__.main.py).
        # TODO: Permit a classname other than 'main'
        module_name, module_info = selected_module
        gamemodule = __import__('src.games.%s.main' % module_name, globals(), locals(), ['main'])
 
        # Spawn the game as a child Component, and then launch it.
        self.game = self.spawn(gamemodule.main())
        self.game.launch()

    def loop(self):
        """Perform a Component loop. If still alive, perform a Game loop."""
        super(RootComponent, self).loop()
        if self.alive:
            self.game.loop()