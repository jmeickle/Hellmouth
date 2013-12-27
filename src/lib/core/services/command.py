"""A queue of commands."""

from Queue import Queue

from src.lib.core.kernel import Kernel
from src.lib.core.services.service import Service

class CommandService(Queue):
    command_names = {
        # Game process commands
        "Save" : "save the game",
        "Load" : "load the game",
        "Quit" : "quit the game",

        # Prompt commands
        "Confirm" : "confirm or submit",
        "Cancel" : "cancel or go back",

        # CMD_HEX = "hex direction"
        # CMD_RECT = "rectangular direction"

        # Player character commands
        "Attack" : "attack",
        "Talk" : "talk",
        "Move" : "move"
    }

    key_mappings = {
        "Attack" : ("a",),
        "Talk" : ("t",),
        "Move" : ("1", "3", "4", "6", "7", "9"),
        "Wait" : ("5",),
        "Cancel" : ("Space",),
    }

    @Kernel.helper
    def keymap(self, command):
        """Return the keys mapped to a command."""
        return CommandService.key_mappings.get(command, None)