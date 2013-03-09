"""Defines the methods for the basic Agent class."""

from src.lib.agents.contexts.context import agent_context

from src.lib.util.command import Command, CommandRegistry as CMD
from src.lib.util.debug import DEBUG
from src.lib.util.dynamic import caller
from src.lib.util.result import Result, SingleResult
from src.lib.util.hex import *
from src.lib.util.log import Log

class Agent(object):
    # TODO: What Components do all Agents have?
    components = []

    def __init__(self, components=[]):
        self.component_registry = {}

        for component in Agent.components + components:
            self.register_component(component)

        # Positioning information
        self.map = None
        self.pos = None
        self.subposition = CC

    """Component processing methods."""

    def call(self, domain, method=None, *args, **kwargs):
        """Call a method across a number of Components, returning a Result object.

        Every Component (optionally, limited to a domain) is offered a chance
        to respond to the method call and contribute to the result set. After
        the last component has responded, the order reverses."""

        results = kwargs.pop("results", Result(self, domain, method, args, kwargs))
        kwargs["results"] = results

        for component in self.get_components(domain):
            getattr(component, method)(*args, **kwargs)

        # TODO: Attempt to exit early if current result == None?

        # TODO: Handle reversing
        # for implementation in reversed(self.get_components(domain)):
        #    getattr(implementation, operation)(method, results, *args)

        return results

    def get(self, domain, key, default=None):
        """Convenience method to return the result of a keyed get method in a domain."""
        results = SingleResult(self, domain, "get", key)
        return self.call(domain, "get", key, default, results=results).get_result()

    # def set(self, domain, key, *args):
    #     """Convenience method to return the parsed result of a keyed set method in a domain."""
    #     return self.result(domain, "set", key, *args)

    def values(self, domain, method, *args, **kwargs):
        """Yield the results of a method applied to a single domain."""

        for component in self.get_components(domain):
            for result in getattr(component, method)(*args, **kwargs):
                yield result

        # TODO: Attempt to exit early if current result == None?

        # TODO: Handle reversing
        # for implementation in reversed(self.get_components(domain)):
        #    getattr(implementation, operation)(method, results, *args)

        # return results

    """Component helper methods."""

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
        """Return an iterator over Components.

        Optionally, limit to a domain.
        """
        if domain:
            for component in self.component_registry.get(domain, []):
                yield component
        else:
            for domain in self.get_domains():
                for component in self.get_components(domain):
                    yield component

    def get_domains(self):
        """Return an iterator over currently defined domains."""
        return self.component_registry.keys()

    """Event processing methods."""

    def process_event(self, event, context):
        """Find the first Command matching an event, instantiate it, and process it."""
        Log.add("EVENT: %s" % event)

        for command_class, command_arguments in context.get_commands():
            for command_event in command_class.get_events():
                if event != command_event:
                    continue

                command = command_class(context)
                context.update_arguments(**command_arguments)

                result = self.process_command(command)
                context.add_result(command.entry_id, "command", result)

                outcome, cause = context.parse_result(result)
                if outcome is True:
                    Log.add("(+): %s" % cause)
                else:
                    Log.add("(-): %s" % cause)

                return outcome, cause

        Log.add("( ): %s" % event)
        return False

    """Command processing methods."""

    def process_command(self, command):
        """Process a Command object by attempting to process each of its Actions in sequence.

        Returns an outcome and a cause, based on the Context's parsing.
        """
        command.context.append(command.entry_id, command=command)

        prefixes = command.context.get(command.entry_id, "prefixes")
        if not prefixes:
            prefixes = command.get_prefixes()
            command.context.update(command.entry_id, prefixes=prefixes)

        Log.add("CMD: %s (%s)." % (command.__class__.get_name(), prefixes))

        # This is a generator, so we can check the Context object for a
        # different list of actions between go-arounds.
        for action_class in command.get_actions():
            action = action_class(command)
            result = self.process_action(action)
            action.context.add_result(action.entry_id, "action", result)

            outcome, cause = action.context.parse_result(result)
            if outcome is False:
                break

        return command.context.parse_results(command.entry_id, "command")

    def can(self, command):
        """Helper to check whether a Command object can be attempted within its Context."""
        command.context.update(command.entry_id, prefixes=["can"])
        return self.process_command(command)

    """Command processing helper methods."""

    @agent_context
    def get_commands(self, context):
        """Yield the Commands this Agent makes available to itself within a Context."""
        domains = context.domains if context.domains else self.get_domains()

        for domain in domains:
            for command in self.values(domain, "get_commands", context):
                yield command

    # STUB
    def sort_commands(self, commands):
        """Sort the commands accessible to an Agent."""
        return commands

    """Action processing methods."""

    def process_action(self, action):
        """Process this Action by executing its phase sequence within a
        list of prefixes.

        The necessary arguments for each phase are pulled from the provided
        keyword arguments. The return value accumulates the method return
        values into a list like so:

                ["believe", "can", "do"] x ["touch", "get", "drop"]

            =   ["believe_touch", "can_touch", "do_touch",
                "believe_get", "can_get", "do_get",
                "believe_drop", "can_drop", "do_drop"]
        
        If any function returns False, processing will stop, meaning that the
        return value has variable length."""
        Log.add("ACT: %s" % action.__class__.get_name())

        action.context.append(action.entry_id, action=action)
        active_prefix = action.context.get(action.entry_id, "prefixes")[0]
        action.context.update(action.entry_id, active_prefix=active_prefix)

        # This is a generator, so we can check the Context object for a
        # different list of phases between go-arounds.
        for phase in action.get_phases():
            phase, phase_arguments = phase[0], phase[1:]
            # On the other hand, prefixes are fixed per-pass.
            for prefix in action.context.get(action.entry_id, "prefixes"):
                action.context.update(action.entry_id, active_prefix=prefix)
                action.context.append(action.entry_id, phase=phase)
                action.context.require_arguments(phase_arguments)
                arguments = action.context.get_aliased_arguments(phase_arguments)
                result = getattr(action.context.agent, prefix + "_" + phase)(**arguments)
                action.context.add_result(action.entry_id, "phase", result)

                outcome, cause = action.context.parse_result(result)
                Log.add("P: %s (%s)." % (prefix + "_" + phase, outcome))
                if outcome is False:
                    # Return to get_phases(), which typically means we're done
                    # in this function because there will be no next phase.
                    break

        return action.context.parse_results(action.entry_id, "action")

    """Context utility methods."""

    @UNIMPLEMENTED
    def get_context(self, members=[], source=None):
        pass
        # """Return a Context object containing information about the Agent's immediate surroundings."""
        # return Context(self, members, source)

    @UNIMPLEMENTED
    def update_context_variables(self, **kwargs):
        """Update the variables available within a context."""
        pass

    """Miscellaneous methods."""

    @agent_context
    def provide_argument(self, context, arg):
        if arg == "manipulator":
           return self.call("Body", "get_default_manipulator")
        if arg == "weapon":
           return self.call("Combat", "get_default_weapon")

    @agent_context
    def provide_arguments(self, context, required_arguments):
        """Provide in a list of required arguments."""
        for required_argument in required_arguments:
            provided_argument = self.provide_argument(self, context, required_argument)
            if provided_argument: yield provided_argument

    @agent_context
    def provide_commands(self, context):
        """Yield the interaction options an Agent provides to another Agent."""
        if "Combat" in context.domains:
            yield CMD("Attack", target=self, weapon=None)

    # Return your own cell.
    # TODO: Multi-cell creatures.
    # TODO: Move to body.
    def cell(self):
        return self.map.cell(self.pos)

    # Calculate the distance between an actor and a target.
    # TODO: Multi-cell creatures.
    # TODO: Move to Body.
    def dist(self, target):
        return dist(self.pos, target.pos)

    def react(self, identifier, *args):
        """Try to call a reaction method based on the calling method's name
        and a sequence identifier.

        Any string is valid as a sequence identifier, though the most common
        will be "before", "on", and "after". Any method is valid as a reaction
        target, though the most common will be steps within an action like
        "move". This results in callback names like "react_before_do_move" and
        "react_after_do_handle".
        """
        reaction = getattr(self, "react_%s_%s" % (identifier, caller()), None)
        if reaction:
            return reaction(*args)