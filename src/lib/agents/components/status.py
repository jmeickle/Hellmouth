"""Defines the Components and Traits that provide status effect functionality to Agents."""

from src.lib.agents.components.component import Component

class Status(Component):
    """Defines the ability to be afflicted by status effects."""

    def __init__(self, owner):
        self.statuses = {}
        self.owner = owner

    def count(self):
        """How many status effects the agent has."""
        return len(self.statuses)

    def get_unconscious(self):
        """Whether the Agent currently has the Unconscious status effect."""
        if self.statuses.get("Unconscious") is not None:
            return False
        return True

    def set_unconscious(self, value):
        """Set the Agent's Unconscious status effect to a value."""
        self.statuses["Unconscious"] = value
        return True