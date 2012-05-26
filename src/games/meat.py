from actors.player import Player
from component import Component
from views.tactical import Window
from views.help import HelpScreen
from levels.meat.arena import MeatArena
from key import *

class Game(Component):
    def __init__(self, window):
        Component.__init__(self)
        self.window = window
        self.player = Player()
        self.level = None
        self.map = None

        self.go(MeatArena)
        self.spawn(Window(window))

    def go(self, destination):
        if self.map is not None:
            self.map.leave(self.player)
        self.level = destination()
        self.map = self.level.map
        self.map.enter(self.player)
        self.inherit()

    def loop(self):
        self.alive = self.conditions()
        if self.alive == False:
            return

        destination = self.map.advance()
        if destination is not None:
            self.go(destination)

        # Draw tree.
        self.window.clear()
        self._draw()
#        self.window.refresh()

        # Keyin tree.
        c = self.window.getch()
        self._keyin(c)

    # Games don't have the normal keyin/_keyin function, since they need to
    # steal input before their children can get to it.

    def _keyin(self, c):
        if self.keyin(c) is False:
            return False
        for child in reversed(self.children):
            if child._keyin(c) is False:
                return False

    def keyin(self, c):
        # Always allow help.
        if c == ord('?'):
            self.spawn(HelpScreen(self.window))

        # Always allow quitting.
        if c == ctrl('q'):
            self.suicide()
        # 'Global' keypresses that work anywhere
#        if c == ord('P'):
#            views[0].player.attack(views[0].player)
#        elif c == ord('g'):
#            views[0].player.get_all()
#        elif c == ord('d'):
#            views[0].player.drop_all()

    # Returns whether we meet the conditions to keep playing.
    def conditions(self):
        if self.map.acting is None and len(self.map.queue) == 0:
            return False
        if self.player.alive is False:
            return False
        return True

    # 'Global' keyin.
#    def keyin(self, c):
#        (for quitting)
#        self.alive = False


