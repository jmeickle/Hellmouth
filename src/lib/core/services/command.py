"""A service to manage a queue of commands."""

from src.lib.core.kernel import kernel
from src.lib.core.services.service import Service

from src.lib.util import debug

class Command(object):
    def __init__(self, key, name):
        self.active = True
        self.key = key
        self.name = name

    def __call__(self, *commands):
        return self.name in commands

    def __repr__(self):
        return "<'{}' command>".format(self.name)

    def done(self):
        self.active = False

class CommandService(Service):
    def __init__(self, commands={}):
        self.commands = commands
        self.keybindings = {v.get("key"): k for k, v in self.commands.items()}

        self.queue = []

    def pop(self):
        if self.queue:
            command = self.queue.pop()
            debug.log("{} popped: {}".format(self, command))
            return command

    def push(self, value):
        debug.log("{} pushed: {}".format(self, value))
        self.queue.append(value)

    # TODO: Refactor
    def react(self):
        key = kernel.input.pop()
        if key:
            command = Command(key, self.keybindings.get(key, False))
            if command:
                debug.log("{} received command: {}".format(self, command))
                self.push(command)
                return command