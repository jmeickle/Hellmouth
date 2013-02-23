"""Defines a set of target manipulation Traits used across Agents.""" 
#
# ACTION PRIMITIVE CALLBACK METHODS:
#

# The "can" methods check whether the primitive, if attempted *right now*,
# would be able to be performed (but not whether it would be successful!).

# The "do" methods actually perform primitives and change game state. They
# do NOT check whether what they are attempting to do is valid because they
# always are preceded by appropriate "can" methods. These methods return
# True if the primitive is successfully performed.

from src.lib.actors.action import Action
from src.lib.agents.components.component import Component
from src.lib.util.command import Command
from src.lib.util.mixin import Mixin

"""Actions."""

class Use(Action):
    """Use a target using a manipulator."""
    sequence = [
        ("touch", "target"),
        ("grasp", "target"),
        ("handle", "target"),
        ("use", "target")
    ]

class Pickup(Action):
    """Lift an item from the environment into your manipulator."""
    sequence = [
        ("touch", "target"),
        ("grasp", "target"),
        ("force", "target"),
    ]

class Putdown(Action):
    """Move an item from your manipulator into the environment."""
    sequence = [
        ("touch", "item"),
        ("grasp", "item"),
        ("force", "item"),
        ("ungrasp", "item"),
    ]

class Drop(Action):
    """Let an item fall down from your manipulator into the environment (uncontrolled)."""
    sequence = [
        ("touch", "item"),
        ("grasp", "item"),
        ("ungrasp", "item"),
    ]

class Wield(Action):
    """"Hold an item in a manipulator out in front of you."""
    sequence = [
        ("touch", "item"),
        ("grasp", "item"),
        ("force", "item"),
        ("ready", "item"),
    ]

class Unwield(Action):
    """Lower an item in a manipulator to your side."""
    sequence = [
        ("touch", "item"),
        ("grasp", "item"),
        ("force", "item"),
        ("unready", "item"),
    ]


"""Commands."""

class Ready(Command):
    description = "ready an item"
    defaults = ("R",)

class UseTerrain(Command):
    description = "use a terrain feature"
    defaults = ("U",)

    @classmethod
    def get_actions(cls):
        return [Use]

class Wield(Command):
    description = "wield a weapon"
    defaults = ("w",)

Command.register(UseTerrain)

"""Components."""

"""Mixins."""

class TouchMixin(Mixin):
    """Provides the ability to touch a target with a manipulator.

    Unlike many other Traits, there is no corresponding 'Untouch' Trait because
    this is an instantaneous effect with no 'on' state."""

    # STUB
    def can_touch(self, target, manipulator=None):
        return True

    # STUB
    def do_touch(self, target, manipulator=None):
        return True

# Touch the target (with a specific item).
class ContactMixin(Mixin):
    """Provides the ability to touch a target with a second target.


    Unlike many other Traits, there is no corresponding 'Uncontact' Trait because
    this is an instantaneous effect with no 'on' state."""

    # Return whether the actor can touch the target with the item.
    # TODO: Enhanced return values.
    def can_contact(self, contacted_target, contacting_target):
        """Whether you can touch a target with a second target."""
        # TODO: Restructure attack option structure so that items can figure
        # this out based on how they are being held
        distance = self.dist(contacted_target)
        attack_option = self.attack_options[self.attack_option]
        min_reach = attack_option[3][0] + self.min_reach()
        max_reach = attack_option[3][-1] + self.max_reach()

        # Check whether it's too close to reach
#        min_reach = self.min_reach() + item.min_reach(self.attack_option)
        if distance < min_reach:
            return (False,)

        # Check whether it's too far to reach
#        max_reach = self.max_reach() + item.max_reach(self.attack_option)
        if distance > max_reach:
            return (False,)
        return (True,)

    def do_contact(self, contacted_target, contacting_target):
        """Touch a target with a second target."""
        return True

class GraspMixin(Mixin):
    """Provides the ability to hold a the target with a manipulator."""

    # STUB
    def can_grasp(self, target, manipulator=None):
        return True

    # STUB
    def do_grasp(self, target, manipulator=None):
        return True

class UngraspMixin(Mixin):
    """Provides the ability to let go of a target with a manipulator."""

    # STUB
    def can_ungrasp(self, target, manipulator=None):
        return True

    # STUB
    def do_ungrasp(self, target, manipulator=None):
        return True

class GetMixin(Mixin):
    """Provides the ability to touch a target with a manipulator.

    Unlike many other Traits, there is no corresponding 'Untouch' Trait because
    this is an instantaneous effect with no 'on' state."""

    # STUB
    def can_touch(self, target, manipulator=None):
        return True

    # STUB
    def do_touch(self, target, manipulator=None):
        return True

class ReadyMixin(Mixin):
    """Provides the ability to raise the target outward from your body."""

    # STUB
    def can_ready(self, target, manipulator=None):
        return True

    # STUB
    def do_ready(self, target, manipulator=None):
        return True

class UnreadyMixin(Mixin):
    """Provides the ability to lower the target to the side of your body."""

    # STUB
    def can_unready(self, target, manipulator=None):
        return True

    # STUB
    def do_unready(self, target, manipulator=None):
        return True

class UseMixin(Mixin):
    """Provides the ability to use a target for an intended function.

    Unlike many other Traits, there is no corresponding 'Unuse' Trait because
    this is an instantaneous effect with no 'on' state."""
    # TODO: ^ What about canceling use of an item?

    # STUB
    def can_use(self, target):
        """Whether you can use a target."""
        return True

    def do_use(self, target):
        """Use a target."""
        target.react("on", self)
        return True

class UseAtMixin(Mixin):
    """Provides the ability to use a target at a second target.

    Unlike many other Traits, there is no corresponding 'UnuseAt' Trait because
    this is an instantaneous effect with no 'on' state."""
    # TODO: ^ What about canceling use of an item?


    # STUB
    def can_use_at(self, target, item):
        """Whether you can use a target at a second target."""
        return True

    # Use an item at a target.
    # STUB
    def do_use_at(self, target, item):
        """Use a target at a second target."""
        return True

class ForceMixin(Mixin):
    """Provides the ability to exert force to reposition a target whose mass is controlled by you."""

    # STUB
    def can_force(self, target):
        """Whether you can exert force to reposition a target whose mass is controlled by you.."""
        return True

    # STUB
    def do_force(self, target):
        """Exert force to reposition a target whose mass is controlled by you."""
        return True

class SlideMixin(Mixin):
    """Provides the ability to exert force to drag, slide, or shove a target against a surface."""

    # STUB
    def can_slide(self, target, surface):
        """Whether you can exert force to drag, slide, or shove a target against a surface."""
        return True

    # STUB
    def do_slide(self, target, surface):
        """Exert force to drag, slide, or shove a target against a surface."""
        return True

class HandleMixin(Mixin):
    """Provides the ability to exert force to reposition or manipulate part of a target.

    n.b. - You can handle some targets even if you can't Force or Slide them."""

    # STUB
    def can_handle(self, target):
        """Whether you can exert force to reposition or manipulate part of a target."""
        return True

    # STUB
    def do_handle(self, target):
        """Exert force to reposition or manipulate part of a target."""
        return True

class ManipulatingAgent(TouchMixin, ContactMixin, GraspMixin, UngraspMixin, ReadyMixin, UnreadyMixin, UseMixin, UseAtMixin, ForceMixin, SlideMixin, HandleMixin):
    """Convenience mixin class for Agents that have manipulators capable of holding items."""
    pass

# Everything below here is stub functions!
# # Throw the target at another target.
# class throw(ActionPrimitive): pass

# # Attach the target to your body.
# class equip(ActionPrimitive): pass

# # Unattach the target from your body.
# class unequip(ActionPrimitive): pass

# # Typically, these will require a single actor or item as a first target, and a
# # location as a second target:

# # Move the target from one map location to another.
# class move(ActionPrimitive): pass

# # Typically, these will require a single actor or item as a first target, and a
# # single item as a second target:

# # Point a readied target at a second target.
# # n.b. - It is up to the item whether brandishing is compatible with readying!
# class brandish(ActionPrimitive): pass

# # Stop pointing a readied target at a second target.
# # n.b. - This can have a second target because you can pointedly lower your
# # weapon 'at' someone, e.g., if asked to by a guard.
# class unbrandish(ActionPrimitive): pass