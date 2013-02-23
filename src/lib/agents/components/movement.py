"""Provides functionality for Agents to change their position on the map."""

from src.lib.agents.components.action import Action
from src.lib.agents.components.component import Component
from src.lib.util.command import Command
from src.lib.util.mixin import Mixin

"""Actions."""

"""Moves resulting in an Agent's position changing."""

class Move(Action):
    """Remove an Agent from the environment, placing it into your manipulator exclusively."""
    sequence = [
        ("touch", "target"),
        ("grasp", "target"),
        ("force", "target"),
    ]

"""Moves resulting in an Agent's posture changing."""


"""Commands."""

class Get(Command):
    """Pick up a single nearby item."""
    description = "pick up an item"
    defaults = ("g",)

    @classmethod
    def get_actions(cls):
        return [Pickup, Pack]

"""Components."""

"""Mixins."""