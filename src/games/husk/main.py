
from src.lib.components.component import Component
from src.lib.components.views.screens.screen import Screen, MenuScreen
from src.lib.components.views.tactical import Window
from src.lib.components.views.screens.help import HelpScreen

from src.lib.util.key import *
from src.lib.util import system
from src.lib.util.queue import Queue

from src.games.husk.agents.actors.player import Player
from src.games.husk.data import screens as screen_data
from src.games.husk.levels.outdoors import Cornfield

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

    # Launch actions (post-initialization, pre-start).
    def launch(self, resume=False):
        # Display:

        # Store the provided curses window.
        self.window = self.parent.window
        self.screens = []

        # Set up the save if necessary.
        if resume is False:
            self.new_game()
        else:
            self.resume_game()

        # Perform any actions before starting the game.
        self.before_start()

    # STUB: Define the save path for this game.
    def save_path(self):
        return 'saves/%s/%s' % (self.__class__.__name__, self.player.name)

    def new_game(self):
        # Create a directory structure to match the new game.
        path = self.save_path()
        folders = ["db", "exports",]
        for folder in folders:
            system.makedir("%s/%s" % (path, folder))

        # Launch the database.
        from src.lib.util import db

        # TODO: Create any necessary tables.

    # STUB: Resume a game from a directory.
    def resume_game(self):
        pass

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

    def keyin(self, c):
        # Always allow help.
        if c == ord('?'):
            self.spawn(HelpScreen(self.window))
        # Always allow quitting.
        elif c == ctrl('q'):
            self.finish()
        return True

    # Returns whether we meet the conditions to keep playing.
    def conditions(self):
        # TODO: Move this to the map.
        if self.map is not None:
            if not Queue.get_acting():
                self.finish()#before_finish()
                return False
            if self.player.alive is False:
            #    self.before_finish()
                return False
        return True

    # Functions called (before/when) (starting/finishing) the game.
    def before_start(self):
        self.screen("start", {"callback" : self.start, "footer_text": screen_data.footer})
        self.spawn(HelpScreen(self.window))

    def start(self):
        # Go to the first level.
        self.go(Cornfield)

        # Spawn the main game window.
        self.view = self.spawn(Window(self.window))

    def before_finish(self):
        self.gameplay = False
        self.screen("end")#, {"callback" : self.finish})

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

        screendata = screen_data.text.get(screenname)
        if arguments is not None:
            screendata.update(arguments)
        self.spawn(screenclass(self.window, **screendata))