"""Defines the methods for the basic Agent class."""

from src.lib.util.command import Command
from src.lib.agents.contexts.context import AgentContext
from src.lib.util.dynamic import caller
from src.lib.util.hex import *
from src.lib.util.log import Log

class Agent(object):
    # TODO: What Components do all Actors have?
    components = []

    def __init__(self, components=[]):
        self.component_registry = {}

        for component in Agent.components + components:
            self.register_component(component)

        # Positioning information
        self.map = None
        self.pos = None
        self.subposition = CC

    def register_component(self, component, domain=None):
        """Initializes an instance of a Component class and registers it as the sole member of its domain."""
        if not domain:
            domain = component.__name__
        assert domain not in self.component_registry
        self.component_registry[domain] = [component(self)]

    def get_component(self, domain):
        """Return the first Component from a domain."""
        return self.component_registry.get(domain, [None])[0]

    def get_components(self, domain=None):
        """Return an iterator over Components (optionally, limited to a domain)."""
        if domain:
            for component in self.component_registry.get(domain, []):
                yield component
        else:
            for domain, components in self.component_registry.items():
                for component in components:
                    yield component

    # TODO: Handle checking interruptions and the like.
    def process(self, domain, method, *args):
        """Process a method for every Component in a domain.

        Every Component in a domain is offered a chance to process the method
        in turn and contribute to the result set. After the last component has
        responded, the order reverses."""
        implementations = [component for component in self.get_components(domain)]
        result = None

        for implementation in implementations:
            result = implementation.process(method, result, args)
        # TODO: Attempt to exit early if current result == None?
#        for implementation in reversed(implementations):
#            result = implementation.process(method, result, args)
        return result

    # TODO: Let implementations override
    def get(self, domain, key, *args):
        """Return the result of a simple get within a domain."""
        return self.process(domain, "get_" + key, *args)

    # TODO: Let implementations override
    def set(self, domain, key, *args):
        """Return the result of a simple set within a domain."""
        return self.process(domain, "set_" + key, *args)

    def react(self, identifier, *args):
        """Try to call a reaction method based on the calling method's name
        and a sequence identifier.

        Any string is valid as a sequence identifier, though the most common
        will be "before", "on", and "after"."""
        reaction = getattr(self, "react_%s_%s" % (identifier, caller()), None)
        if reaction:
            return reaction(*args)

    def get_context(self, members=[], source=None):
        """Return a Context object containing information used to decide how to process an Agent's event."""
        assert members or source
        return AgentContext(self, members, source)

    def respond(self, event, context, scope=None):
        """Respond to an event occurring within a given Context."""
        commands = [command for command in self.get_commands()] + [interaction for interaction in context.get_interactions()]
#        exit(commands)
        for origin, command in self.sort_commands(commands):
            if event in command.events():
                # TODO: Make this hurt other people less
                actions = command.get_actions()
                kwargs = {"target" : origin}

                if not scope:
                    result = self.attempt(actions, **kwargs)
                else:
                    result = self.action(scope, actions, **kwargs)

                # STUB: need a parse_result function.
                return result
        # Whether to continue
        Log.add("Couldn't do: %s" % event)
        return True

    def get_commands(self, domain=None):
        """Query each Component for the commands it makes accessible to an Agent."""
        return self.process(domain, "get_commands")

    # STUB
    def sort_commands(self, commands):
        """Sort the commands accessible to an Agent."""
        return commands

    def get_interactions(self, agent, source):
        """List the interaction options exposed to another Agent within a given source."""
        yield Command("Attack")

    # Return your own cell.
    # TODO: Multi-cell creatures.
    def cell(self):
        return self.map.cell(self.pos)

    # Calculate the distance between an actor and a target.
    # TODO: Multi-cell creatures.
    def dist(self, target):
        return dist(self.pos, target.pos)

    def action(self, scope, actions, **kwargs):
        """Process an action consisting of a sequence of steps required for completion."""
        # Setup keyword arguments.
        kwargs = self.prep_kwargs(kwargs)

        from src.lib.util.debug import DEBUG
        for action in actions:
            # Get the results of processing the action.
            results = action().process(scope, **kwargs)

            # TODO: Return the full results!
            # A full attempt returns len(scope) * len(action.sequence) results.
            if len(results) != len(action.sequence) * len(scope):
                return False

        # If we did reach the end, we only need to check the last primitive.
        return results[-1][0]

    """Action helper functions - shorthand for calls to self.action()."""

    def believe(self, actions, **kwargs):
        """Check whether an action is believed to be attemptable."""
        return self.action(["believe"], actions, **kwargs)

    def can(self, actions, **kwargs):
        """Check whether an action can actually be attempted."""
        return self.action(["can"], actions, **kwargs)

    def attempt(self, actions, **kwargs):
        """Check whether an action can actually be attempted; if so, attempt it."""
        return self.action(["can", "do"], actions, **kwargs)