"""Define Commands as an intermediary layer of abstraction, between keypresses and actions."""

class Command(object):

    registry = {}

    action = None
    description = "no command"
    defaults = []

    def __new__(self, command):
        return Command.get(command)

    @staticmethod
    def get(command):
        return Command.registry.get(command, Command)

    @staticmethod
    def register(command):
        Command.register_command(command.__name__, command)
        Command.register_events(command.events(), command)

    @staticmethod
    def register_command(name, command):
        Command.registry[name] = command

    @staticmethod
    def register_events(events, command):
        for event in events:
            command_list = Command.registry.get(event, [])
            command_list.append(command)
            Command.registry[event] = command_list

    @classmethod
    def events(cls):
        return cls.defaults

    @classmethod
    def name(cls):
        return cls.__name__

    @classmethod
    def get_action(cls):
        return cls.action

class Save(Command):
    description = "save the game"

class Load(Command):
    description = "load the game"

class Quit(Command):
    description = "quit the game"

class Attack(Command):
    description = "attack"
    defaults = ("a",)

class Talk(Command):
    description = "talk"
    defaults = ("t",)

# This is a bit hackish, but it beats registering them all by hand!
for command in [Save, Load, Quit, Attack, Talk]:
    if command.__name__[0] != "_":
        Command.register(command)

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