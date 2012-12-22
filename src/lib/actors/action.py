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
            return getattr(actor, self.apply(method))(actor, target)
        _default_method.__name__ = method
        setattr(self.__class__, _default_method.__name__, _default_method)

# Touch the target (with anything).
class touch(ActionPrimitive): pass

# Hold on to the target using a manipulator.
class grasp(ActionPrimitive):
    # TODO: Remove this, it's only here for testing.
    if __name__ == '__main__':
        def can_grasp(self, actor, target):
            return "Yay! Actor: %s; Target: %s" % (actor, target)

if __name__ == '__main__':
    test = grasp()
    print "Class methods:", test.__class__.__dict__
    print "Trying 'can_grasp':", test.can(test, test)
    print "Trying 'cancel_grasp':", test.cancel(test, test)

    # Inspecting function source:
    # import inspect
    # print inspect.getsource(test.can)

