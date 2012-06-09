from actors.player import Player
from component import Component
from views.screens import Screen
from views.tactical import Window
from views.help import HelpScreen
from levels.meat.arena import MeatArena
from key import *
from data import screens

# TODO: Split this into a generic game class and a meatgame meatclass
class Game(Component):
    def __init__(self, window):
        Component.__init__(self)

        # DISPLAY:
        # Store the provided curses window.
        self.window = window
        self.screens = []

        # Whether we're interacting with maps and levels.
        self.gameplay = True

        # Generate the player, a blank level, and a blank map.
        self.player = Player()
        self.level = None
        self.map = None

        # Perform any actions before starting the game.
        self.before_start()

    def loop(self):
        # Don't continue looping if the game is over.
        if self.alive is False:
            return False

        # Check whether we should keep playing.
        if self.gameplay is True:
            self.gameplay = self.conditions()

        # If we have a level, try to loop.
        if self.gameplay is True and self.level is not None:
            if self.level.map is not None:
                # Pass map to our children if it has changed.
                if self.map != self.level.map:
                    self.map = self.level.map
                    self.inherit()

            # If the level has a destination set, go to it.
            # (This might end the game.)
            if self.level.loop() is False:
                self.go(self.level.destination)

            # When we're in a map, we have to play nice with keyin.
            # HACK: This is likely to break during travel at some point.
            if self.map.acting is None or self.map.acting.controlled is False:
                return True

            # Get screens from the level (which may have gotten some from the map.)
            self.screens.extend(self.level.screens)
            self.level.screens = []

        # Show any screens we picked up.
        # The screens generated first will show up first.
        for x in range(len(self.screens)):
            screenname, arguments, screenclass = self.screens.pop()
            self.screen(screenname, arguments, screenclass)

        # Draw tree.
        self.window.clear()
        self._draw()

        # Keyin tree.
        c = self.window.getch()
        self._keyin(c)

        return True

    def keyin(self, c):
        # Always allow help.
        if c == ord('?'):
            self.spawn(HelpScreen(self.window))

        # Always allow quitting.
        if c == ctrl('q'):
            self.finish()

    # Returns whether we meet the conditions to keep playing.
    def conditions(self):
        # TODO: Move this to the map.
        if self.map is not None:
            if self.map.acting is None and len(self.map.queue) == 0:
                self.before_finish()
                return False
            if self.player.alive is False:
                self.before_finish()
                return False
        return True

    # Functions called (before/when) (starting/finishing) the game.
    def before_start(self):
        self.screen("meat-start", {"callback" : self.start, "footer_text": screens.footer})
        self.spawn(HelpScreen(self.window))

    def start(self):
        # Go to the first level.
        self.go(MeatArena)

        # Spawn the main game window.
        self.view = self.spawn(Window(self.window))

    def before_finish(self):
        self.gameplay = False
        self.screen("meat-end")#, {"callback" : self.finish})

    # The game is over. Do anything required before exiting.
    def finish(self):
        self.screen("credits", {"callback" : self.suicide})

    # Go to a new level.
    def go(self, destination):
        # If this is called with False as a destination, no more levels.
        # This means the game is likely over.
        if destination is False:
            return self.before_finish()

        # Generate the level and store it.
        self.level = destination(self.player)

        # Store the generated map.
        self.map = self.level.map

    # Spawn a screen based on a screen name, attributes, and class.
    def screen(self, screenname="blank", arguments=None, screenclass=None):
        if screenclass == None:
            screenclass = Screen

        screendata = screens.text.get(screenname)
        if arguments is not None:
            screendata.update(arguments)
        self.spawn(screenclass(self.window, **screendata))
