"""A Component is a combination of state and functionality possessed by an Agent."""

from src.lib.util.command import CommandRegistry
from src.lib.util.define import *
from src.lib.util.result import ignore_results

class Component(object):
    commands = None
    dependencies = []
    """Mark a Component as having a dependency on another Component."""

    def __init__(self, owner):
        self.owner = owner

    def trigger(self, *triggers):
        """Respond to triggers."""
        pass

    def process(self, method, *args, **kwargs):
        """Process the results of a method call."""
        return getattr(self, method)(*args, **kwargs)

    @classmethod
    def set_commands(cls, *commands):
        cls.commands = []
        for command in commands:
            cls.commands.append(command)
            CommandRegistry.register(command)

    def get_commands(self, context):
        """Yield the Commands provided by this Component in a context.

        By default, anything in cls.commands is always checked.

        This is a generator because a yield-based return value is friendlier
        for classes that override to define commands only available in certain
        situations."""
        assert self.__class__.commands is not None, "Class '%s' has no get_commands method and unset cls.commands" % self.__class__
        for command in self.__class__.commands:
            yield command

    def before_turn(self):
        """Respond to the Agent's turn starting."""
        pass

    def after_turn(self):
        """Respond to the Agent's turn ending."""
        pass

    @UNIMPLEMENTED
    def get(self, *args):
        pass