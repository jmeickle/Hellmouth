"""A Component is a combination of state and functionality possessed by an Agent."""

from src.lib.util.command import Command
from src.lib.util.result import ignore_results

class Component(object):
    commands = []
    dependencies = []
    """Mark a Component as having a dependency on another Component."""

    def __init__(self, owner):
        self.owner = owner

    def process(self, method, *args, **kwargs):
        """Process the results of a method call."""
        return getattr(self, method)(*args, **kwargs)

    @classmethod
    def set_commands(cls, *commands):
        cls.commands = []
        for command in commands:
            cls.commands.append(command)
            Command.register(command)

    @ignore_results
    def get_commands(self):
        """Return the commands provided by this Component.

        This is a generator because a yield-based return value is friendlier
        for classes that override to define commands only available in certain
        situations."""
        for command in self.__class__.commands:
            yield command

    def before_turn(self):
        """Respond to the Agent's turn starting."""
        pass

    def after_turn(self):
        """Respond to the Agent's turn ending."""
        pass

    def get(self, *args):
        assert False, "Unimplemented!"