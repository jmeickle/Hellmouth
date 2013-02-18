"""Defines the methods for the basic Agent class."""

from src.lib.util.dynamic import caller

from src.lib.util.hex import *

class Agent(object):

    def __init__(self, components=[]):
        self.components = []
        self.component_registry = {}

        for component in components + self.components:
            self.register_component(component)

    def action(self, methods, action, **kwargs):
        """Process an action consisting of a sequence of steps required for completion."""
        # Setup keyword arguments.
        kwargs = self.prep_kwargs(kwargs)

        # Get the results of processing the action.
        results = action.process(methods, **kwargs)

        # TODO: Return the full results!
        # A full attempt returns len(methods) * len(self.definition) results.
        if len(results) != len(action.definition) * len(methods):
            return False

        # If we did reach the end, we only need to check the last primitive.
        return results[-1][0]

    """Action helper functions - shorthand for calls to self.action()."""

    def believe(self, act, **kwargs):
        """Check whether an action is believed to be attemptable."""
        return self.action(["believe"], act, **kwargs)

    def can(self, act, **kwargs):
        exit(act)
        """Check whether an action can actually be attempted."""
        return self.action(["can"], act, **kwargs)

    def attempt(self, act, **kwargs):
        """Check whether an action can actually be attempted; if so, attempt it."""
        return self.action(["can", "do"], act, **kwargs)

    # TODO: Implement this properly!
    def process(self, domain, method, *args):
        """Process a method for every Component in a domain.

        Every Component in a domain is offered a chance to process the method
        in turn and contribute to the result set. After the last component has
        responded, the order reverses."""
        implementations = self.component_registry.get(domain)
        result = None
        for implementation in implementations:
            result = implementation.process(method, result, args)
        for implementation in reversed(implementations):
            result = implementation.process(method, result, args)
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
            reaction(*args)

    def register_component(self, component, domain=None):
        """Initializes a Component as the sole member of its domain in the registry."""
        if not domain:
            domain = component.__name__
        assert domain not in self.component_registry
        self.component_registry[domain] = [component(self)]

    # Return your own cell.
    def cell(self):
        return self.map.cell(self.pos)

    # Calculate the distance between an actor and a target.
    def dist(self, target):
        return dist(self.pos, target.pos)