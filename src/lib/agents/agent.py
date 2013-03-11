"""Defines the methods for the basic Agent class."""

from src.lib.agents.contexts.context import agent_context

from src.lib.util.command import Command, CommandRegistry as CMD
from src.lib.util.debug import debug, DEBUG, die
from src.lib.util.dynamic import caller
from src.lib.util.result import Result, SingleResult, ActionResult
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

    def trigger(self, *triggers):
        """Respond to triggers."""
        if "rebuild" in triggers:
            self.trigger_components("rebuild")

    """Component processing methods."""

    def call(self, domain, method, *args, **kwargs):
        """Call a method across a number of Components, returning a Result object.

        Every Component (optionally, limited to a domain) is offered a chance
        to respond to the method call and contribute to the result set. After
        the last component has responded, the order reverses."""

        results = kwargs.pop("results", Result)()

        for component in self.get_components(domain):
            results.add_result(getattr(component, method)(*args, **kwargs))
            if not results.can_add_result():
                break

        # TODO: Attempt to exit early if current result == None?

        # TODO: Handle reversing
        # for implementation in reversed(self.get_components(domain)):
        #    getattr(implementation, operation)(method, results, *args)

        return results

    def get(self, domain, key, default=None):
        """Convenience method to return the result of a keyed get method in a domain."""
        result = self.call(domain, "get", key, results=SingleResult).get_outcome()
        return result if result is not None else default

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

    """Component getter methods."""

    def get_component(self, domain):
        """Return the first Component within a domain."""
        return self.component_registry.get(domain, [None])[0]

    def get_components(self, domain=None):
        """Yield this Agent's Components (optionally, within a domain)."""
        if domain:
            for component in self.component_registry.get(domain, []):
                yield component
        else:
            for domain in self.get_domains():
                for component in self.get_components(domain):
                    yield component

    """Component setter methods."""

    def append_component(self, component, domain=None, trigger=True):
        """Append a Component to a domain."""
        if not domain:
            domain = component.__class__.get_domain()

        components = self.component_registry.get(domain, [])
        components.append(component)
        self.component_registry[domain] = components

        if trigger:
            component.trigger("registered")

    def prepend_component(self, component, domain=None, trigger=True):
        """Prepend a Component to a domain."""
        if not domain:
            domain = component.__class__.get_domain()

        components = self.component_registry.get(domain, [])
        components.insert(0, component)
        self.component_registry[domain] = components

        if trigger:
            component.trigger("registered")

    def remove_component(self, component, domain=None, trigger=True):
        """Remove a Component from a domain."""
        if not domain:
            domain = component.__class__.get_domain()

        components = self.component_registry.get(domain, [])
        components.remove(component)

        if components:
            self.component_registry[domain] = components
        else:
            del self.component_registry[domain]

        if trigger:
            component.trigger("deregistered")

    """Component helper methods."""

    def register_component(self, component_class, domain=None):
        """Initialize an instance of a Component class, register it as the sole
        member of its domain, and send a "registration" trigger to it."""
        if not domain:
            domain = component_class.get_domain()

        if domain in self.component_registry:
            die("Tried to register a component '%s' in the domain '%s', which already has Components %s." % (component_class.__name__, domain, [component.__class__.__name__ for component in self.get_components(domain)]))

        component = component_class(self)
        self.append_component(component, domain)
        component.trigger("registered")

    def trigger_components(self, *triggers, **kwargs):
        """Send a list of triggers to each Component in a domain."""
        for component in self.get_components(kwargs.pop("domain", None)):
            component.trigger(*triggers)

    """Domain helper methods."""

    def has_domain(self, domain):
        """Return whether an Agent has any components in a Domain."""
        return True if domain in self.component_registry else False

    def get_domains(self):
        """Yield all currently defined domains."""
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
                outcome, cause = context.parse_result(result)
                if outcome is True:
                    Log.add("(+): %s" % cause)
                else:
                    Log.add("(-): %s" % cause)

                # TODO: Instead return whether the event was consumed.
                return outcome, cause

        Log.add("( ): %s" % event)
        # TODO: Instead return whether the event was consumed.
        return False

    """Command processing methods."""

    def process_command(self, command):
        """Process a Command object by attempting to process each of its Actions in sequence.

        Returns an outcome and a cause, based on the Context's parsing.
        """
        ctx = command.context
        ctx.set_active(command.__class__)

        prefixes = ctx.get_argument("prefixes")
        if not prefixes:
            ctx.set_argument("prefixes", command.get_prefixes())

        Log.add("CMD: %s (%s)." % (command.__class__.get_name(), prefixes))

        # This is a generator, so we can check the Context object for a
        # different list of actions between go-arounds.

        for action_class in command.get_actions(ctx):
            debug("Starting action: %s" % action_class)
            action = action_class(command)

            result = self.process_action(action)
            ctx.append_result(command.__class__, result)
            outcome, cause = ctx.parse_result(result)
            if outcome is False:
                break

        return ctx.parse_results(command)

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

        ctx = action.context
        ctx.set_active(action.__class__)

        # This is a generator, so we can check the Context object for a
        # different list of phases between go-arounds.
        for phase in action.get_phases():
            phase, phase_arguments = phase[0], phase[1:]
            ctx.set_active(phase)
            # On the other hand, prefixes are fixed per-pass.
            for prefix in ctx.get_argument("prefixes"):
                ctx.set_argument("active_prefix", prefix)
                ctx.require_arguments(phase_arguments)
                arguments = ctx.get_aliased_arguments(phase_arguments)

                result = getattr(ctx.agent, prefix + "_" + phase)(**arguments)
                ctx.append_result(action.__class__, result)
                # TODO: ugh. only here so the ctx can get this info in the get_phases loop.
                if prefix == "do":
                    ctx.append_result(phase, result)
                outcome, cause = ctx.parse_result(result)
                Log.add("P: %s (%s)." % (prefix + "_" + phase, outcome))
                if outcome is False:
                    # Return to get_phases(), which typically means we're done
                    # in this function because there will be no next phase.
                    break

        return ctx.parse_results(action.__class__)

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
           return self.call("Body", "get_default_manipulator", context).get_result()
        if arg == "weapon":
           return self.call("Combat", "get_default_weapon", context).get_result()
        # TODO: Remove this default
        if arg == "container" and self.has_domain("Container"):
            return self

    @agent_context
    def provide_arguments(self, context, required_arguments):
        """Provide in a list of required arguments."""
        for required_argument in required_arguments:
            provided_argument = self.provide_argument(self, context, required_argument)
            if provided_argument: yield provided_argument

    @UNIMPLEMENTED
    def provide_commands(self, context):
        """Yield the interaction commands an Agent provides to another Agent
        within a Context.
        """
        pass

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

    def react(self, *args, **kwargs):
        """Try to call a reaction method based on the calling method's name
        and a sequence identifier (by default, the identifier is "on").

        Any string is valid as a sequence identifier, though the most common
        will be "before", "on", and "after". Any method is valid as a reaction
        target, though the most common will be steps within an action like
        "move". This results in callback names like "react_before_do_move" and
        "react_after_do_handle".
        """
        reaction = getattr(self, "react_%s_%s" % (kwargs.pop("identifier", "on"), caller()), None)
        if reaction:
            return reaction(*args, **kwargs)