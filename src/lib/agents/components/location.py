"""Provides functionality for Agents to be located within a game."""

from src.lib.util.trait import Trait

"""Traits."""

class Locatable(Trait):
    """Provides methods to manage location within a game (i.e., across maps)."""
    location = None

    @Trait.include
    def __init__(self, *args, **kwargs):
        """Set self's location after performing the rest of self's initialization."""
        Trait.super(Locatable, self).__init__(*args, **kwargs)
        self.location = kwargs.pop("location", self.location)

    @property
    def metric(self):
        """Return the metric space of self's location."""
        return self.location.metric