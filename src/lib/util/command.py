"""Define Commands as an intermediary layer of abstraction, between keypresses and actions."""

from copy import copy

class Command(object):
    actions = []
    description = "no command"
    defaults = []

    def __init__(self, context):
        self.context = context
        self.entry_id = self.context.get_id()

    def __call__(self, next_action, *arguments):
        """Override __call__ to allow concisely checking Action status in get_phases()."""
        if not self.context:
            return True

        for called_action, result in self.context.get_results(self.entry_id, "action"):
            outcome, cause = self.context.parse_result(result)
            if next_action == called_action:
                return outcome

        return False

    def get_actions(self):
        """Yield the Actions required to complete this Command.

        Because this method returns a generator, it's possible to modify the
        Command's associated Context inside of a loop as long as this results
        in no actions being inserted before the most recently visited one.
        """
        for action in self.__class__.actions:
            yield action

    def get_default_actions(self):
        """Yield the Actions that would normally be required to complete this Command."""
        default = self.copy()
        del default.context
        return default.get_phases()

    def get_prefixes(self):
        intent = self.context.get_intent()
        if "attempt" in intent:
            return ["can", "do"]

    @classmethod
    def events(cls):
        return cls.defaults

    @classmethod
    def name(cls):
        return cls.__name__

class Save(Command):
    description = "save the game"

class Load(Command):
    description = "load the game"

class Quit(Command):
    description = "quit the game"

class Talk(Command):
    description = "talk"
    defaults = ("t",)

class Cancel(Command):
    description = "cancel or go back"
    defaults = (" ",)

class Confirm(Command):
    description = "confirm or submit"
    defaults = ("\n",)

# class Backspace(Command):
#     description = "confirm or submit"
#     defaults = ("Backspace",)

# class Delete(Command):
#     description = "confirm or submit"
#     defaults = ("Delete",)

class CommandRegistry(object):
    registry = {}

    def __new__(self, command_name, context=None, **kwargs):
        """Return the Command class corresponding to a provided name.

        If a Context is provided, return an instance of that Command instead."""
        command_class = CommandRegistry.get(command_name)
        assert command_class, "Attempted to retrieve unregistered command: '%s'" % command_name

        if context:
            command = command_class(context)
            context.update(command.entry_id, **kwargs)
            return command
        else:
            return command_class

    @staticmethod
    def get(command_name, default=Command):
        return CommandRegistry.registry.get(command_name, default)

    @staticmethod
    def register(*commands):
        for command in commands:
            assert command.name() not in CommandRegistry.registry, "Attempted to register command twice: '%s'" % command.name()
            CommandRegistry.register_command(command.name(), command)
            CommandRegistry.register_events(command.events(), command)

    @staticmethod
    def register_command(name, command):
        CommandRegistry.registry[name] = command

    @staticmethod
    def register_events(events, command):
        for event in events:
            command_list = CommandRegistry.get(event, [])
            command_list.append(command)
            CommandRegistry.registry[event] = command_list

# This is a bit hackish, but it beats registering them all by hand!
CommandRegistry.register(Save, Load, Quit, Talk, Cancel, Confirm)

# # Player character commands
# CMD_ATTACK = 
# CMD_TALK = "talk"
# CMD_HEX = "hex direction"
# CMD_RECT = "rectangular direction"
# CMD_CONFIRM = "confirm or submit"
# CMD_CANCEL = "cancel or go back"

# commands = {}
# commands[CMD_ATTACK] = ("a",)
# commands[CMD_TALK] = ("t",)
# commands[CMD_HEX] = ("1", "3", "4", "6", "7", "9", "5")
# commands[CMD_CANCEL] = (' ',)