"""Factions!"""

import random

from src.lib.agents.components.component import Component

from src.lib.util import hex

class NeutralFaction(Component):
    """Component that handles an Agent's faction."""

    commands = []
    domain = "Faction"

    def __init__(self, owner, controller):
        super(NeutralFaction, self).__init__(owner)

        self.controller = controller

    """Faction getter functions."""

    def get_faction(self):
        return self.controller

    """Faction setter functions."""

    def set_faction(self, faction):
        self.controller = faction

    """Faction helper methods."""

    def get_target(self):
        """no target"""
        return False

    def get_destination(self):
        """no target"""
        return random.choice(hex.area(self.owner.pos, 10))

class EnemyFaction(NeutralFaction):
    """Enemy faction."""
    def get_target(self):
        """default to controller"""
        return self.owner.map.get_controller()