
"""Usage note: if an Action has a prefix like "Un", retain the capitalization
of the prefixed Action. For example, `Equip` should become `UnEquip`. This
permits more convenient references between these classes.
"""

from copy import copy

from src.lib.util.define import *

class Action(object):
    """A sequence of steps that can be called within prefixed scopes."""

    def __init__(self, command):
        """Load the default sequence for that class if one is not provided."""
        self.context = command.context
        self.entry_id = command.entry_id

        # Phase generator example:
        # yield "touch", "target"
        # if self("touch", "target"): yield "grasp", "target"
        # if self("grasp", "target"): yield "force", "target"
        # if self("force", "target"): yield "ready", "target"

    def __call__(self, next_phase, *arguments):
        """Override __call__ to allow concisely checking phase status in get_phases()."""
        if not self.context:
            return True

        for called_phase, result in self.context.get_results(self.entry_id, "phase"):
            outcome, cause = self.context.parse_result(result)
            if next_phase == called_phase:
                return outcome

        return False

    def get_phases(self):
        """Yield the phases required to complete this Action.

        Because this method returns a generator, it's possible to modify the
        Action's associated Context inside of a loop as long as this results in
        no phases being inserted before the most recently visited one.
        """
        for phase in self.__class__.phases:
            yield phase

    def get_default_phases(self):
        """Yield the phases that would normally be required to complete this Action."""
        default = self.copy()
        del default.context
        return default.get_phases()

    @UNIMPLEMENTED
    def get_remaining_phases(self, current_phases):
        """Yield the phases remaining before completion."""
        for remaining_phase in self.get_phases():
            pass

#
# ACTION PRIMITIVE CALLBACK METHODS:
#

# The "can" methods check whether the primitive, if attempted *right now*,
# would be able to be performed (but not whether it would be successful!).

# The "do" methods actually perform primitives and change game state. They
# do NOT check whether what they are attempting to do is valid because they
# always are preceded by appropriate "can" methods. These methods return
# True if the primitive is successfully performed.

# Actions are activities carried out by an agent. The most common kind of agent
# is an actor, but spells or environmental effects can also be agents. Each
# action can be described as "`agent` does `action` to `target`". Even actions
# that have no obvious target, like sleeping, are represented as the agent
# targeting itself.
#
# The basic component of an action is an action primitive. This represents a
# simple, discrete unit of activity that serves as a component of an action
# chain representing a more complex activity. Action primitives can be thought
# of as activities that are too fine-grained to warrant manual control, but
# still important for determining how more complex activities resolve. Some
# examples of action primitives are:
#
# 'touch': Touch the target (with anything).
# 'grasp': Hold on to the target using a manipulator.
# 'wield': Hold the target outward from your body using a manipulator.
#
# From here on out, we'll use 'action' to refer to a chain of action primitives
# and 'primitive' to refer to an action primitive.
#
# This file defines the requirements for primitives and the logic to join them
# into actions. It also defines a basic set of them that should be appropriate
# for most game, though these can be overridden if necessary.

# An individual action primitive.
# TODO: Remove this class; we don't explicitly need an ActionPrimitive class now.
# class ActionPrimitive():
#     # When a primitive is initialized, it generates a class method for each
#     # of its self.methods() according to the pattern in self.add_method(). By
#     # default, these generated class methods call a corresponding actor method
#     # according to the pattern in self.apply().
#     def __init__(self):
#         for method in self.methods():
#             self.add_method(method)

#     # The methods that can be applied to this primitive.
#     # TODO: Make this a dict containing arguments to check against.
#     def methods(self):
#         return ['believe', 'can', 'do']

#     # The name of a corresponding actor method for this primitive. By default
#     # it looks for "believe_touch", "can_grasp", etc.
#     def apply(self, method):
#         return method + '_' + self.__class__.__name__

#     # Add a class method to a primitive to check the corresponding actor method.
#     def add_method(self, method):
#         def _default_method(self, actor, *args):
#             result = getattr(actor, self.apply(method), None)(*args)
#             # If we got None as our result, that means the function either
#             # returned nothing or didn't exist in the first place. Log it.
#             if result is None:
#                 DEBUG("Actor %s did not have method %s(%s)" % (actor.name, method, args))
#                 return (False,)
#             return result
#         _default_method.__name__ = method
#         setattr(self.__class__, _default_method.__name__, _default_method)


#
# ACTIONS:
#

# Dictionary of defined actions.
actiondict = {
    #
    # MOVEMENT AND POSITIONING:
    #

    # Move yourself from one location to another.
    "move_to" : (
        ("move", "actor", "pos"),
    ),

    #
    # ATTACKS AND COMBAT:
    #

    # Avoid an attack.
    "dodge" : (
        ("move", "actor", "pos"),
    ),
}