"""A Game is a Component responsible for managing all gameplay within a given
scope. This scope often consists of the entirety of gameplay, but a Game could
create other Games as children (e.g., a minigame).

Typically, a Game launches a sequence of startup screens (title, menu, dialogue,
etc.) followed by instantiating a Level containing initial state."""

from src.lib.components.component import Component
from src.lib.components.views.screens.screen import Screen, MenuScreen
from src.lib.components.views.encounter import EncounterWindow
from src.lib.components.views.screens.help import HelpScreen

from src.lib.util.key import *
from src.lib.util import system

from src.games.husk.agents.actors.player import Player
from src.games.husk.data import screens as screen_data
from src.games.husk.levels.outdoors import Farm

class Game(Component):
    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)

        # Whether we're interacting with maps and levels.
        self.gameplay = False

        # Generate the Player.
        # TODO: Move.
        self.player = Player()

    def get_controller(self):
        """Return the Actor serving as primary controller in this Game."""
        return self.player

    def launch(self, resume=False):
        """Prepare the game for play."""

        # Set up the save if necessary.
        if resume is False:
            self.new_game()
        else:
            self.resume_game()

        # Start the game!
        self.before_start()

    """Game start methods."""

    def before_start(self):
        """Do anything required before turning over control to the first level."""

        # Generate the first level.
        self.level = self.generate_level(Farm)

        # Spawn a help screen and a start screen.
        self.screen("start", {"callback" : self.start, "footer_text": screen_data.footer})
        self.spawn(HelpScreen(self.window))

    def start(self):
        """Turn over control to the first level."""

        # Spawn the main game window.
        self.view = self.spawn(EncounterWindow(self.window, self.level.map))

        # Travel to the first level.
        self.enter_level(self.level, map_id=1, entrance_id="prev", exit_id=None)

        self.gameplay = True

    """Game loop methods."""

    def can_continue_gameplay(self):
        """Returns whether the game meets the conditions to keep playing."""
        # TODO: Fix?
        if not self.gameplay:
            self.before_finish()
            return False
        if self.level and not self.level.can_continue_gameplay():
            self.before_finish()
            return False
        return True

    def loop(self):
        """Perform one iteration of the game loop."""

        # Don't continue looping if the game is over.
        if not self.gameplay or not self.alive:
            return False

        # Don't continue looping if we haven't started, or have a screen.
        # if self.children
        #     return False

        # Check whether we should continue to play.
        self.gameplay = self.can_continue_gameplay()

        # If we're playing and in a level, hand over control to it.
        if self.gameplay and self.level:
            self.level.loop()

        # # Show any screens we picked up.
        # # The screens generated first will show up first.
        # for x in range(len(self.screens)):
        #     screenname, arguments, screenclass = self.screens.pop()
        #     self.screen(screenname, arguments, screenclass)

    """Game finish methods."""

    def before_finish(self):
        self.gameplay = False
        self.screen("end", {"callback" : self.finish})

    def finish(self):
        """The game is over. Do anything required before finishing."""
        self.screen("credits", {"callback" : self.suicide})

    """Level management methods."""

    def generate_level(self, level_class, **level_data):
        """Instantiate a Level from a class and argument dict, and then return it."""
        return level_class(self, **level_data)

    def enter_level(self, level, map_id=None, entrance_id=None, exit_id=None):
        """Enter a Level, optionally including information about the trip."""
        if self.level:
            # TODO: Save old levels?
            self.exit_level(level, map_id=None, entrance_id=None, exit_id=None)
        level.before_arrive(map_id, entrance_id, exit_id)
        level.arrive(map_id, entrance_id, exit_id)
        self.level = level

    def exit_level(self, level=None, map_id=None, entrance_id=None, exit_id=None):
        """Exit a Level, optionally including information about the trip."""
        self.level.before_depart(map_id, entrance_id, exit_id)
        self.level.depart(map_id, entrance_id, exit_id)
        del self.level

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

    """UI methods."""

    def keyin(self, c):
        """Handle keyin."""
        # Always allow help.
        if c == ord('?'):
            self.spawn(HelpScreen(self.window))
        # Always allow quitting.
        elif c == ctrl('q'):
            self.parent.relaunch = False
            self.before_finish()
        return True

    def screen(self, screenname="blank", arguments=None, screenclass=None):
        """Spawn a Screen based on a screen name, attributes, and class."""
        if screenclass == None:
            screenclass = Screen

        screendata = screen_data.text.get(screenname, {})
        if arguments is not None:
            screendata.update(arguments)
        self.spawn(screenclass(self.window, **screendata))