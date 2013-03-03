"""Define Commands as an intermediary layer of abstraction, between keypresses and actions."""

class Command(object):
    actions = []
    description = "no command"
    defaults = []

    def __init__(self, context):
        self.context = context
        self.entry_id = self.context.get_id()

    def get_actions(self):
        """Get actions required to complete this Command."""
        return self.__class__.actions

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