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

# Hack to allow running this script as a single file.
# TODO: Remove.
if __name__ == '__main__':
    import sys
    sys.path.insert(0, '/home/eronarn/Code/Hellmouth/')

# An individual action primitive.
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
        return ['believe', 'can', 'attempt', 'cancel']

    # The name of a corresponding actor method for this primitive. By default
    # it looks for "believe_touch", "can_grasp", etc.
    def apply(self, method):
        return method + '_' + self.__class__.__name__

    # Add a class method to a primitive to check the corresponding actor method.
    def add_method(self, method):
        def _default_method(self, actor, *args):
            return getattr(actor, self.apply(method))(*args)
        _default_method.__name__ = method
        setattr(self.__class__, _default_method.__name__, _default_method)

# A chain of multiple action primitives.
class Action():
    # When an action is initialized, it retrieves its definition.
    def __init__(self, action_key):
        self.definition = actiondict[action_key]

    # Process a list of methods for each primitive in this action's
    # definition. The necessary arguments for each primitive are pulled from
    # the provided keyword arguments. The return value accumulates the method
    # return values in a 'striped' list:
    #
    # [Method1, Method2, Method3] x [Primitive1, Primitive2, Primitive3]
    # == M1P1, M2P1, M3P1, M1P2, M2P2, M3P2, M1P3, M2P3, M3P3
    #
    # If any function returns False, processing will stop, meaning that the
    # return value has variable length.
    def process(self, methods, **kwargs):
        results = []
        # For each primitive in this action's definition...
        for primitive_definition in self.definition:

            # Get the name of the current primitive.
            primitive = primitive_definition[0]

            # Get the primitive's desired arguments from the action definition.
            primitive_args = primitive_definition[1:len(primitive_definition)]

            # Always use actor as the first argument.
            args = (kwargs["actor"],)

            # Populate the rest of the arguments, if any.
            for primitive_arg in primitive_args:
                # We don't do this here - what if an argument really *should*
                # be none? Leave it up to the function to assert.
                # assert(kwargs.get(primitive_arg) is not None)
                args += (kwargs.get(primitive_arg),)

            # Process each method of the current primitive.
            for method in methods:
                result = self.process_primitive(method, primitive, *args)

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

    # Process a single method for a single primitive.
    # TODO: Restructure this.
    def process_primitive(self, method, primitive, *args):
        return getattr(globals()[primitive](), method)(*args)

#
# ACTION PRIMITIVES:
#

# Typically, these can take either a single actor or item as target:

# Touch the target (with anything).
class touch(ActionPrimitive): pass

# Hold on to the target.
class grasp(ActionPrimitive): pass

# Let go of the target.
class ungrasp(ActionPrimitive): pass

# Hold the target outward from your body.
class ready(ActionPrimitive): pass

# Hold the target at the side of your body.
class unready(ActionPrimitive): pass

# Throw the target at another target.
class throw(ActionPrimitive): pass

# Use the target.
class use(ActionPrimitive): pass

# Attach the target to your body.
class wear(ActionPrimitive): pass

# Unattach the target from your body.
class unwear(ActionPrimitive): pass

# Typically, these will require a single item as target:

# Store the target into inventory.
class store(ActionPrimitive): pass

# Drop the target from inventory.
class unstore(ActionPrimitive): pass

# Typically, these will require a single actor or item as a first target, and a
# location as a second target:

# Move the target from one map location to another.
class move(ActionPrimitive): pass

# Typically, these will require a single actor or item as a first target, and a
# single item as a second target:

# Touch the target (with a specific item).
class contact(ActionPrimitive): pass

# Point a readied target at a second target.
# n.b. - It is up to the item whether brandishing is compatible with readying!
class brandish(ActionPrimitive): pass

# Stop pointing a readied target at a second target.
# n.b. - This can have a second target because you can pointedly lower your
# weapon 'at' someone, e.g., if asked to by a guard.
class unbrandish(ActionPrimitive): pass

# Use an item at the target.
class use_at(ActionPrimitive): pass

#
# ACTIONS:
#

# Dictionary of defined actions.
actiondict = {
    "attack" : (
        ("touch", "item"),
        ("grasp", "item"),
        ("ready", "item"),
        ("contact", "target", "item"),
        ("use_at", "target", "item")
    ),
}

# Basic testing code.
# TODO: Deprecated!
if __name__ == '__main__':
#    test = grasp()
#    print "Class methods:", test.__class__.__dict__
#    print "Trying 'can_grasp':", test.can(test, test)
#    print "Trying 'cancel_grasp':", test.cancel(test, test)

    # Inspecting function source:
    # import inspect
    # print inspect.getsource(test.can)
#    import action
#    test2 = getattr(action, 'grasp')()
#    print "Second object:", test2
#    print "Trying 'can_grasp':", test2.can(test2, test2)

    import actor
    # Actor 1
    a1 = actor.Actor()
    # Actor 2
    a2 = actor.Actor()

    # Throw a grenade:
    throw_grenade = Action(["touch", "grasp", "wield", "throw"])
    if throw_grenade.check("can", a1, a2):
        throw_grenade.check("attempt", a1, a2)
