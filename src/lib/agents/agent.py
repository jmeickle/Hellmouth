"""Defines the methods for the basic Agent class."""

from src.lib.agents.contexts.context import agent_context

from src.lib.util.command import Command, CommandRegistry as CMD
from src.lib.util import debug
from src.lib.util.dynamic import caller
from src.lib.util.result import Result, SingleResult, ActionResult
from src.lib.util.log import Log
from src.lib.util.queue import Queue
from src.lib.util.trait import Traitable

class Agent(object):
    __metaclass__ = Traitable

    name = 'Anonymous'

    # TODO: What Components, if any, do all Agents have?
    components = []

    # TODO: Make this a proper registry using src.lib.util.registry
    def __init__(self, components=[]):
        """Register the provided components."""
        super(Agent, self).__init__()
        self.component_registry = {}

        # TODO: Initialize registry with these arguments.
        for component in Agent.components + components:
            self.register_component(component)

    def __call__(self, method):
        return getattr(self, method)()

    # TODO: Add real coloring support.
    def appearance(self):
        return self.name

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

    def get_controlled_components(self, controller, domain=None):
        """Yield Components controlled by another Agent (optionally, within a domain)."""
        for component in self.get_components(domain):
            if component.controller == controller:
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
            debug.die("Tried to register a component '%s' in the domain '%s', which already has Components %s." % (component_class.__name__, domain, [component.__class__.__name__ for component in self.get_components(domain)]))

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

    def has_domains(self, *domains):
        """Return whether an Agent has components in all provided Domains."""
        current_domains = [domain for domain in self.get_domains()]
        for domain in domains:
            if domain not in current_domains:
                return False
        return True

    def get_domains(self):
        """Yield all currently defined domains."""
        return self.component_registry.keys()

    """Event processing methods."""

    def process_event(self, event, context):
        """Find the first Command matching an event, instantiate it, and process it."""

        if not self.turn():
            debug.die("Event %s by %s; should be acting: %s; queue: %s" % (event, self.appearance(), Queue.get_acting().appearance(), [a.appearance() for a in Queue.queue]))

        if event not in ["Up", "Down"]:
            debug.log("EVENT: %s" % event)

        for command_class, command_arguments in context.get_commands():
            for command_event in command_class.get_events():
                if event != command_event:
                    continue

                command = command_class(context)
                context.update_arguments(**command_arguments)

                result = self.process_command(command)
                outcome, cause = context.parse_result(result)
                if outcome is True:
                    debug.log("(+): %s" % cause)
                    Log.add("(+): %s" % cause)
                else:
                    debug.log("(-): %s" % cause)
                    Log.add("(-): %s" % cause)

                # TODO: Something else to decide this
                self.end_turn()

                # TODO: Instead return whether the event was consumed.
                return outcome, cause

        if event not in ["Up", "Down"]:
            debug.log("( ): %s" % event)
            Log.add("( ): %s" % event)
        # TODO: Instead return whether the event was consumed.
        return False

    """Command processing methods."""

    def process_command(self, command):
        """Process a Command object by attempting to process each of its Actions in sequence.

        Returns an outcome and a cause, based on the Context's parsing.
        """
        ctx = command.context
        # ctx.set_active(command.__class__)
        debug.log("CMD: %s." % command.__class__.get_name())

        # This is a generator, so we can check the Context object for a
        # different list of actions between go-arounds.

        for action_class in command.get_actions(ctx):
            action = action_class(command)

            result = self.process_action(action)
            ctx.append_result(command.__class__, result)
            outcome, cause = ctx.parse_result(result)
            if outcome is False:
                break

        return ctx.parse_results(command.__class__)

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
        debug.log("ACT: %s" % action.__class__.get_name())

        ctx = action.context
        # ctx.set_active(action.__class__)

        # This is a generator, so we can check the Context object for a
        # different list of phases between go-arounds.
        for phase in action.get_phases():
            phase.context = ctx

            result = self.process_phase(phase)
            ctx.append_result(action.__class__, result)
            outcome, cause = ctx.parse_result(result)
            if outcome is False:
                break

        return ctx.parse_results(action.__class__)

    """Phase processing methods."""

    def process_phase(self, phase):
        """Process a Phase object.

        Returns an outcome and a cause, based on the Context's parsing.
        """
        ctx = phase.context
        ctx.set_active(phase)
        debug.log("PHASE: %s" % phase.name)

        # TODO: 7DRL
        ctx.require_arguments(phase.required_arguments)
        # arguments = {}
        # for argument in phase.required_arguments:
        #     arguments[phase.aliases.get(argument, argument)] = ctx.get_argument(argument)

        arguments = {}
        for argument in phase.required_arguments:
            send = ctx.get_argument(argument)
            send_as = phase.aliases.get(argument, argument)
            arguments[send_as] = send

        is_method = getattr(ctx.agent, "is" + "_" + phase.name, None)
        if is_method:
            is_result = is_method(**arguments)
            outcome, cause = ctx.parse_result(is_result)
            if outcome:
                debug.log("***PHASE SATISFIED***: %s (%s)" % ("is" + "_" + phase.name, outcome))
                return True, "done"

        # TODO: Rewrite this entire section, augh
        could_result = getattr(ctx.agent, "could" + "_" + phase.name)()
        outcome, cause = ctx.parse_result(could_result)
        debug.log("METHOD: %s (%s)" % ("could" + "_" + phase.name, outcome))
        if not outcome: return False, "could" + "_" + phase.name

        can_result = getattr(ctx.agent, "can" + "_" + phase.name)(**arguments)
        outcome, cause = ctx.parse_result(can_result)
        debug.log("METHOD: %s (%s)" % ("can" + "_" + phase.name, outcome))
        if not outcome: return False, "can" + "_" + phase.name

        result = getattr(ctx.agent, "do" + "_" + phase.name)(**arguments)
        outcome, cause = ctx.parse_result(result)
        debug.log("METHOD: %s (%s)" % ("do" + "_" + phase.name, outcome))
        ctx.append_result(phase.__class__, result)
        return outcome, cause

    """Context utility methods."""

    def get_context(self, members=[], source=None):
        """Abstract. Return a Context object containing information about the Agent's immediate surroundings."""
        pass

    def update_context_variables(self, **kwargs):
        """Abstract. Update the variables available within a context."""
        pass

    """Miscellaneous methods."""

    @agent_context
    def provide_argument(self, context, arg):
        if arg == "manipulator":
            return self.call("Body", "get_default_manipulator", context).get_result()
        if arg == "weapon":
            target = context.get_argument("target")
            if target:
                weapon = self.call("Combat", "get_default_weapon", context).get_result()
                if weapon:# and self.call("Manipulation", "can_reach", target, weapon).get_result():
                    return weapon
        # TODO: Remove this default
        if arg == "container" and self.has_domain("Container"):
            return self

    @agent_context
    def provide_arguments(self, context, required_arguments):
        """Provide in a list of required arguments."""
        for required_argument in required_arguments:
            provided_argument = self.provide_argument(self, context, required_argument)
            if provided_argument: yield provided_argument

    def provide_commands(self, context):
        """Abstract. Yield the interaction commands an Agent provides to another Agent
        within a Context.
        """
        pass

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

    def turn(self):
        """Whether it's this Agent's turn."""
        if self == Queue.get_acting():
            return True
        return False

    # Mark self as done acting.
    # TODO: Make this part of a Queue component.
    def end_turn(self):
        if self.turn():
            Queue.next()
            self.after_turn()