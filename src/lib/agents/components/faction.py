"""Factions!"""

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
        return

class EnemyFaction(NeutralFaction):
    """Enemy faction."""
    def get_target(self):
        """default to player"""
        return self.owner.map.player