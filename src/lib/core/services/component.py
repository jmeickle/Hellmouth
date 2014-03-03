"""A service to manage components."""

from src.lib.core.kernel import kernel
from src.lib.core.services.service import Service

from src.lib.components.component import Component

from src.lib.util import debug

class ComponentService(Component, Service):
    def __init__(self):
        super(ComponentService, self).__init__()

        self.game = None
        self.relaunch = True

    def react(self):
        """Loop drawing, keyin, and event processing through this Component and
        into its children. If still alive, perform a Game loop."""

        # Input tree.
        command = kernel.command.pop()
        if command:
            self.input(command)

        # The RootComponent dies if it has no children.
        if not self.children:
            self.alive = False

        if self.alive and self.game:
            debug.log("Acting game: {}".format(self.game))
            self.game.loop()

    def launch(self, package_choice):
        """Spawn the selected module's main.Game as a child Component and then
        launch it."""
        # TODO: Handle multiple game folders
        # TODO: Permit class names other than 'main'
        package_name, package_info = package_choice # e.g., hellmouth, Hellmouth, <description>, <version>
        game_module = __import__('src.games.%s.main' % package_name, globals(), locals(), ['main'])
        game_class = game_module.main

        debug.log("In launch")
        # Spawn the game as a child Component, and then launch it.
        self.game = self.spawn(game_class())
        self.game.launch()
        debug.log("Launched the game!")

    def after_loop(self):
        """Return information for after the ComponentService's loop finishes."""
        return {"relaunch" : self.relaunch}