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
if __name__ == '__main__':
    import sys
    sys.path.insert(0, '/home/eronarn/Code/Hellmouth/')

from src.lib.util.dynamic import *

class ActionPrimitive():
    def __init__(self):
        for method in self.methods():
            self.add_method(method)

    # The actor methods that this primitive will call.
    def methods(self):
        return ['can', 'attempt', 'cancel']

    # The name of the corresponding actor method for this primitive.
    def apply(self, method):
        return method + '_' + self.__class__.__name__

    # Add checks for actor methods to the primitive's class.
    def add_method(self, method):
        def _default_method(self, actor, target):
            return getattr(actor, self.apply(method))(target)
        _default_method.__name__ = method
        setattr(self.__class__, _default_method.__name__, _default_method)

class Action():
    def __init__(self, primitives):
        self.primitives = primitives

    # Check a given method for each primitive in the chain.
    def check(self, method, actor, target):
        for primitive in self.primitives:
            current = globals()[primitive]()
            if getattr(current, method)(actor, target) is False:
                print "Failed at %" % primitive
                return False 
            else:
                print "%s->%s_%s->%s" % (actor.name, method, current.__class__.__name__, target.name)
        return True

# Touch the target (with anything).
class touch(ActionPrimitive): pass

# Hold on to the target using a manipulator.
class grasp(ActionPrimitive): pass

# Let go of a target held in a manipulator.
class ungrasp(ActionPrimitive): pass

# Move the target from one location to another.
class move(ActionPrimitive): pass

# Hold the target outward from your body using a manipulator.
class wield(ActionPrimitive): pass

# Attach the target to your body.
class wear(ActionPrimitive): pass

# Activate the target.
class use(ActionPrimitive): pass

# Get the item into inventory.
class get(ActionPrimitive): pass

# Drop the target from inventory.
class drop(ActionPrimitive): pass

# Throw the target at another target.
class throw(ActionPrimitive): pass

# Swing a sword:
#action = ["touch", "grasp", "wield", "use"]

# Throw a grenade:
#action = ["touch", "grasp", "wield", "throw"]

# Throw a grenade (with pin):
#action = ["touch", "grasp", "wield", "use", "throw"]

# Basic testing code.
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
