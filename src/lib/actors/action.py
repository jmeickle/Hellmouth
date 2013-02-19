# TODO: REMOVE THIS FILE.

from src.lib.util.debug import DEBUG
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
class ActionPrimitive():
    # When a primitive is initialized, it generates a class method for each
    # of its self.methods() according to the pattern in self.add_method(). By
    # default, these generated class methods call a corresponding actor method
    # according to the pattern in self.apply().
    def __init__(self):
        for method in self.methods():
            self.add_method(method)

    # The methods that can be applied to this primitive.
    # TODO: Make this a dict containing arguments to check against.
    def methods(self):
        return ['believe', 'can', 'do']

    # The name of a corresponding actor method for this primitive. By default
    # it looks for "believe_touch", "can_grasp", etc.
    def apply(self, method):
        return method + '_' + self.__class__.__name__

    # Add a class method to a primitive to check the corresponding actor method.
    def add_method(self, method):
        def _default_method(self, actor, *args):
            result = getattr(actor, self.apply(method), None)(*args)
            # If we got None as our result, that means the function either
            # returned nothing or didn't exist in the first place. Log it.
            if result is None:
                DEBUG("Actor %s did not have method %s(%s)" % (actor.name, method, args))
                return (False,)
            return result
        _default_method.__name__ = method
        setattr(self.__class__, _default_method.__name__, _default_method)

class Action(object):
    """A sequence of primitives to be called."""

    def __init__(self, sequence=None):
        if not sequence:
            sequence = self.__class__.sequence
            """Load the default sequence for that class if one is not provided."""
        assert sequence is not None

    def process(self, scopes, **kwargs):
        """Process this Action by executing its primitive sequence within a
        list of scopes.

        The necessary arguments for each primitive are pulled from the provided
        keyword arguments. The return value accumulates the method return
        values into a 'striped' list:
            [Method1, Method2, Method3] x [Primitive1, Primitive2, Primitive3]
            == M1P1, M2P1, M3P1, M1P2, M2P2, M3P2, M1P3, M2P3, M3P3
        
        If any function returns False, processing will stop, meaning that the
        return value has variable length."""

        results = []
        # For each primitive in this action's definition...
        for primitive_definition in self.sequence:

            # Get the name of the current primitive.
            primitive = primitive_definition[0]

            # Get the primitive's desired arguments from the action definition.
            primitive_args = primitive_definition[1:]

            # Always use actor as the first argument.
            args = (kwargs["actor"],)

            # Populate the rest of the arguments, if any.
            for primitive_arg in primitive_args:
                # We don't do this here - what if an argument really *should*
                # be none? Leave it up to the function to assert.
                # assert(kwargs.get(primitive_arg) is not None)
                args += (kwargs.get(primitive_arg),)

            # Process that primitive within each scope.
            for scope in scopes:
                result = self.process_primitive(scope, primitive, *args)

                # Handle the case of pure T/F function returns.
                # TODO: Make all reachable functions return better data rather
                # than just T/F.
                try:
                    if result[0]:
                        pass
                except TypeError:
                    result = (result,)

                # Store the function result.
                results.append(result)

                # If the function's primary result was False, exit early.
                if result[0] is False:
                    return results
        return results

    def process_primitive(self, scope, primitive, *args):
        """Call the primitive's initiator's method within a scope."""
        return getattr(args[0], scope + "_" + primitive)(*args[1:])

class Attack(Action):
    """Attack a target with a weapon held in a manipulator."""
    sequence = [
        ("touch", "weapon"),
        ("grasp", "weapon"),
        # ("lift", "weapon"),
        # ("handle", "weapon"),
        ("ready", "weapon"),
        ("contact", "target", "weapon"),
        ("use_at", "target", "weapon")
    ]

class Toggle(Action):
    """Toggle a target using a manipulator."""
    sequence = [
        ("touch", "target"),
        ("grasp", "target"),
        # ("handle", "target"),
        ("use", "target")
    ]

class Pickup(Action):
    """Lift an item from the environment into your manipulator."""
    sequence = [
        ("touch", "target"),
        ("grasp", "target"),
#        ("lift", "target"),
#        ("handle", "target"),
    ]

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
    # ITEM INTERACTION AND INVENTORY MANAGEMENT:
    #

    # Move an item from your manipulator into the environment.
    "putdown" : (
        ("touch", "item"),
        ("grasp", "item"),
        ("lift", "item"),
        ("handle", "item"),
        ("ungrasp", "item"),
    ),

    # Let an item fall down into the environment (uncontrolled).
    "drop" : (
        ("touch", "item"),
        ("grasp", "item"),
        ("lift", "item"),
        ("ungrasp", "item"),
    ),

    # Move an item from a manipulator onto your body.
    "wear" : (
        ("touch", "item"),
        ("grasp", "item"),
        ("lift", "item"),
        ("handle", "item"),
        ("equip", "item"),
    ),

    # Move an item from your body into a manipulator.
    "unwear" : (
        ("touch", "item"),
        ("grasp", "item"),
        ("unequip", "item"),
        ("lift", "item"),
        ("handle", "item"),
    ),

    # Hold an item in a manipulator out in front of you.
    "wield" : (
        ("touch", "item"),
        ("grasp", "item"),
        ("lift", "item"),
        ("handle", "item"),
        ("ready", "item"),
    ),

    # Hold an item in a manipulator at your side.
    "unwield" : (
        ("touch", "item"),
        ("grasp", "item"),
        ("lift", "item"),
        ("handle", "item"),
        ("unready", "item"),
    ),

    #
    # ATTACKS AND COMBAT:
    #

    # Avoid an attack.
    "dodge" : (
        ("move", "actor", "pos"),
    ),

    # Use a ready item to parry an attack.
    # n.b. - The 'target' is the other item!
    "parry" : (
        ("touch", "item"),
        ("grasp", "item"),
        ("lift", "item"),
        ("handle", "item"),
        ("ready", "item"),
        ("contact", "target", "item"),
        ("use_at", "target", "item")
    ),

    # Use a ready item to disarm.
    # n.b. - The 'target' is the other item!
    "disarm" : (
        ("touch", "item"),
        ("grasp", "item"),
        ("lift", "item"),
        ("handle", "item"),
        ("ready", "item"),
        ("contact", "target", "item"),
        ("use_at", "target", "item")
    ),    
}