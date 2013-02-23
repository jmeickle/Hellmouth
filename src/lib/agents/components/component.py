"""A Component is a combination of state and functionality possessed by an Agent."""

from src.lib.util.command import Command

class Component(object):
    commands = []
    dependencies = []
    """Mark a Component as having a dependency on another Component."""

    def __init__(self, owner):
        self.owner = owner

    def process(self, method, result, args):
        return getattr(self, method)(*args)

    @classmethod
    def set_commands(cls, *commands):
        cls.commands = []
        for command in commands:
            cls.commands.append(command)
            Command.register(command)

    def get_commands(self):
        """Return the commands provided by this Component.

        This is a generator because a yield-based return value is friendlier
        for classes that override to define commands only available in certain
        situations."""
        for command in self.__class__.commands:
            yield command