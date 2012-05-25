from actors.player import Player
from component import Component
from views.tactical import Window

from levels.meat.arena import MeatArena

class Game(Component):
    def __init__(self, window):
        Component.__init__(self)
        # Overriding component init - it's not a subwin.
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


