"""A Game is a Component responsible for managing all gameplay within a given
scope. This scope often consists of the entirety of gameplay, but a Game could
create other Games as children (e.g., a minigame).

Typically, a Game launches a sequence of startup screens (title, menu, dialogue,
etc.) followed by instantiating a Level containing initial state."""

from src.lib.components.component import Component
from src.lib.components.views.screens.screen import Screen, MenuScreen
from src.lib.components.views.tactical import Window
from src.lib.components.views.screens.help import HelpScreen

from src.lib.util.key import *
from src.lib.util import system
from src.lib.util.queue import Queue

from src.games.husk.agents.actors.player import Player
from src.games.husk.data import screens as screen_data
from src.games.husk.levels.outdoors import Farm

class Game(Component):
    def __init__(self, **kwargs):
        Component.__init__(self)

        # Whether to keep playing.
        self.alive = True

        # Whether we're interacting with maps and levels.
        self.gameplay = True

        # Generate the player, a blank level, and a blank map.
        self.player = Player()
        self.level = None
        self.map = None

    def launch(self, resume=False):
        """Prepare the game for play."""

        # Store the provided curses window.
        self.window = self.parent.window # TODO: Unnecessary?
        self.screens = []

        # Set up the save if necessary.
        if resume is False:
            self.new_game()
        else:
            self.resume_game()

        # Perform any actions before starting the game.
        self.before_start()

    """Game start methods."""

    def before_start(self):
        """Do anything required before turning over control to the first level."""
        self.screen("start", {"callback" : self.start, "footer_text": screen_data.footer})
        self.spawn(HelpScreen(self.window))

    def start(self):
        """Turn over control to the first level."""

        # Instantiate and then go to the first level.
        self.go(Farm)

        # Spawn the main game window.
        self.view = self.spawn(Window(self.window))

    """Game loop methods."""

    def can_continue_gameplay(self):
        """Returns whether the game meets the conditions to keep playing."""
        # TODO: Move this to the map.
        if self.map is not None:
            if not Queue.get_acting():
                self.finish()#before_finish()
                return False
            if self.player.alive is False:
            #    self.before_finish()
                return False
        return True

    def loop(self):
        """Main game loop."""

        # Don't continue looping if the game is over.
        if self.alive is False:
            return False

        # Check whether we should keep playing.
        if self.gameplay is True:
            self.gameplay = self.can_continue_gameplay()

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
            acting = Queue.get_acting()
            if not acting or not acting.controlled:
                return True

            # Get screens from the level (which may have gotten some from the map.)
            self.screens.extend(self.level.screens)
            self.level.screens = []

        # Show any screens we picked up.
        # The screens generated first will show up first.
        for x in range(len(self.screens)):
            screenname, arguments, screenclass = self.screens.pop()
            self.screen(screenname, arguments, screenclass)

        return True

    """Game finish methods."""

    def before_finish(self):
        self.gameplay = False
        self.screen("end", {"callback" : self.finish})
    
    def finish(self):
        """The game is over. Do anything required before finishing."""
        self.screen("credits", {"callback" : self.suicide})

    """UI methods."""

    def keyin(self, c):
        # Always allow help.
        if c == ord('?'):
            self.spawn(HelpScreen(self.window))
        # Always allow quitting.
        elif c == ctrl('q'):
            self.before_finish()
        return True

    # Spawn a screen based on a screen name, attributes, and class.
    def screen(self, screenname="blank", arguments=None, screenclass=None):
        if screenclass == None:
            screenclass = Screen

        screendata = screen_data.text.get(screenname, {})
        if arguments is not None:
            screendata.update(arguments)
        self.spawn(screenclass(self.window, **screendata))

    """Level management methods."""

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

    """Game data methods."""

    def new_game(self):
        # Create a directory structure to match the new game.
        path = self.save_path()
        folders = ["db", "exports",]
        for folder in folders:
            system.makedir("%s/%s" % (path, folder))

        # Launch the database.
        from src.lib.util import db

        # TODO: Create any necessary tables.

    # STUB: Define the save path for this game.
    def save_path(self):
        return 'saves/%s/%s' % (self.__class__.__name__, self.player.name)

    # STUB: Resume a game from a directory.
    def resume_game(self):
        pass