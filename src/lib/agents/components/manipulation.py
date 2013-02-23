"""Provides functionality for Agents to manipulate other Agents (typically items).

A Manipulator can be a body part, but it can also be something more poetic like
a gust of wind or a psychic force. Therefore, Manipulation capability says
nothing about Equipment capability (and vice versa). This somewhat complicates
the case of a hand, which is capable of both Manipulating and Equipping. The
functionality provided by a hand is portioned out as so:

* The 'hand' itself is part of a Body. Even if it is severed, the Agent owning
    it can still Manipulate and Equip other Agents.

* The state of wearing a ring requires Equipment capability, but not
    Manipulation capability.

* Putting on or taking off your ring is Manipulating something to change
    whether it is currently Equipped, and requires both sets of functionality.

* Putting on or taking off someone else's ring requires Manipulation
    capability from you and Equipment capability from them.

* Wielding a sword requires Manipulation capability, but not Equipment capability.

* Wielding a katar *properly* requires Equipping it first!

* A psychic force can Manipulate a ring, but can't Equip it.

* A statue can Equip a ring, but can't Manipulate it.

The last example comes with a caveat: the statue would have some Manipulation
capability, e.g., to return whether it is currently grasping a weapon. It
simply wouldn't be able to *change* any of its manipulation states.
"""

from src.lib.agents.components.action import Action
from src.lib.agents.components.component import Component
from src.lib.util.command import Command
from src.lib.util.mixin import Mixin

"""Actions."""

"""Moving Agents to or from manipulators."""

class Pickup(Action):
    """Remove an Agent from the environment, placing it into your manipulator exclusively."""
    sequence = [
        ("touch", "target"),
        ("grasp", "target"),
        ("force", "target"),
    ]

class Putdown(Action):
    """Remove an item from your manipulator, placing it into the environment exclusively."""
    sequence = [
        ("touch", "item"),
        ("grasp", "item"),
        ("force", "item"),
        ("ungrasp", "item"),
    ]

class Drop(Action):
    """Let an item fall from your manipulator into the environment (uncontrolled)."""
    sequence = [
        ("touch", "item"),
        ("grasp", "item"),
        ("ungrasp", "item"),
    ]

class Pack(Action):
    """Remove an item from your manipulator, placing it into a container exclusively."""
    sequence = [
        ("touch", "target"),
        ("grasp", "target"),
        ("force", "target"),
        ("store", "target", "container"),
        ("ungrasp", "target"),
    ]

class UnPack(Action):
    """Remove an item from a container, placing it into your manipulator exclusively."""
    sequence = [
        ("touch", "target"),
        ("grasp", "target"),
        ("force", "target"),
        ("unstore", "target", "container"),
    ]

"""Interacting with Agents using manipulators."""

class Use(Action):
    """Use a target using a manipulator."""
    sequence = [
        ("touch", "target"),
        ("grasp", "target"),
        ("handle", "target"),
        ("use", "target")
    ]

"""Interacting with Agents using manipulators in a way requiring holding them."""

class Wield(Action):
    """"Hold an item in a manipulator out in front of you."""
    sequence = [
        ("touch", "item"),
        ("grasp", "item"),
        ("force", "item"),
        ("ready", "item"),
    ]

class UnWield(Action):
    """Lower an item in a manipulator to your side."""
    sequence = [
        ("touch", "item"),
        ("grasp", "item"),
        ("force", "item"),
        ("unready", "item"),
    ]

class Brandish(Action):
    """Point at a target using a second, wielded target.

    n.b. - This may unready your second target! For example, pointing a
    warhammer at someone makes it rather useless for combat.
    """
    sequence = [
        ("touch", "item"),
        ("grasp", "item"),
        ("force", "item"),
        ("ready", "item"),
    ]

class UnBrandish(Action):
    """Stop pointing at a target using a second, wielded target."""
    sequence = [
        ("touch", "item"),
        ("grasp", "item"),
        ("force", "item"),
        ("unready", "item"),
    ]

# if target.touch():
#     if target.grasp():
#         if target.force():
#             if target.unready():
#                 target.UnBrandish

# # Throw the target at another target.
# class throw(ActionPrimitive): pass


"""Commands."""

class Get(Command):
    """Pick up a single nearby item."""
    description = "pick up an item"
    defaults = ("g",)

    @classmethod
    def get_actions(cls):
        return [Pickup, Pack]

class GetAll(Command):
    """Pick up multiple nearby items."""
    description = "pick up all items"
    defaults = ("G",)

    @classmethod
    def get_actions(cls):
        return [Pickup, Pack]

Command.register(Get, GetAll)

class ReadyWeapon(Command):
    description = "ready an unreadied weapon"
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

"""Mixins."""

class TouchMixin(Mixin):
    """Provides the ability to touch a target with a manipulator."""

    # STUB
    def can_touch(self, target, manipulator=None):
        return True

    # STUB
    def do_touch(self, target, manipulator=None):
        return True

class UnTouchMixin(Mixin):
    """Provides the ability to stop touching a target with a manipulator."""

    # STUB
    def can_untouch(self, target, manipulator=None):
        return True

    # STUB
    def do_untouch(self, target, manipulator=None):
        return True

class TouchingAgent(TouchMixin, UnTouchMixin):
    """Convenience Mixin to represent an Agent with touching capability."""
    pass

class GraspMixin(Mixin):
    """Provides the ability to hold a target with a manipulator."""

    # STUB
    def can_grasp(self, target, manipulator=None):
        return True

    # STUB
    def do_grasp(self, target, manipulator=None):
        return True

class UnGraspMixin(Mixin):
    """Provides the ability to let go of a target with a manipulator."""

    # STUB
    def can_ungrasp(self, target, manipulator=None):
        return True

    # STUB
    def do_ungrasp(self, target, manipulator=None):
        return True

class GraspingAgent(TouchingAgent, GraspMixin, UnGraspMixin):
    """Convenience Mixin to represent an Agent with grasping capability."""
    pass

class ContactMixin(Mixin):
    """Provides the ability to touch a target with a second target."""

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

class UnContactMixin(Mixin):
    """Provides the ability to stop touching a target with a second target."""

    def can_uncontact(self, contacted_target, contacting_target):
        """Whether you can stop touching a target with a second target."""

    def do_uncontact(self, contacted_target, contacting_target):
        """Stop touching a target with a second target."""
        return True

class ReadyMixin(Mixin):
    """Provides the ability to raise the target outward from your body."""

    # STUB
    def can_ready(self, target, manipulator=None):
        return True

    # STUB
    def do_ready(self, target, manipulator=None):
        return True

class UnReadyMixin(Mixin):
    """Provides the ability to lower the target to the side of your body."""

    # STUB
    def can_unready(self, target, manipulator=None):
        return True

    # STUB
    def do_unready(self, target, manipulator=None):
        return True

class HoldingAgent(GraspingAgent, ContactMixin, UnContactMixin, ReadyMixin, UnReadyMixin):
    """Convenience Mixin to represent an Agent that can manipulate held Agents."""
    pass

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

class PositioningAgent(TouchingAgent, ForceMixin, SlideMixin, HandleMixin):
    """Convenience Mixin to represent an Agent that can use its manipulators to position other Agents."""
    pass

class UseMixin(Mixin):
    """Provides the ability to use a target for an intended function.

    Unlike many other Mixins, there is no corresponding 'Unuse' Trait because
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

    Unlike many other Mixins, there is no corresponding 'UnuseAt' Trait because
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

class UsingAgent(TouchingAgent, UseMixin, UseAtMixin):
    """Convenience Mixin to represent an Agent that use its manipulators to use other Agents."""
    pass

class StoreMixin(Mixin):
    """Provides the ability to store targets into a Container."""

    # TODO: Don't use a limit of 5 entries (testing only!).    
    def can_store(self, target, container=None):
        """Whether you can store an item into a Container."""
        if container is None:
            container = self.get_component("Container")

        if container is None:
            return False

        if container.count() > 5:
            return False
        return True

    # Store an item in your container.
    def do_store(self, target, container=None):
        """Store an item into a Container."""

        if container is None:
            container = self.get_component("Container")

        if target.react("on", container) is False:
            return False

        if container.add(target):
            return True
        return False

class UnstoreMixin(Mixin):
    """Provides the ability to unstore targets from a Container."""

    def can_unstore(self, target):
        """Whether you can unstore an item from a Container."""
        return True

    def do_unstore(self, target):
        """Unstore an item from a cOntainer."""
        matches = self.container.get(target.appearance(), [])
        assert target in matches
        matches.remove(target)
        self.container[target.appearance()] = matches        
        return True

class StoringAgent(StoreMixin, UnstoreMixin):
    """Convenience Mixin to represent an Agent that can use its manipulators to store items in Containers."""
    pass

class ManipulatingAgent(HoldingAgent, PositioningAgent, UsingAgent, StoringAgent, Mixin):
    """Convenience Mixin to represent an Agent with full Manipulation capabilities."""
    pass

    # # Whether you believe you can store an item in your container.
    # # @checks_item_memory
    # def believe_store(self, item):
    #     return self.can_store(item)

    # Whether you can store an item in your container.

    # Store the item based on known properties, if you have item memory.
    # TODO: Nicer way of doing item memory?
    # if hasattr(self, 'memory'):
    #     known = self.memory.get(item, Item())
    #     item_list = self.container.get(known.appearance(), [])
    #     item_list.append(item)
    #     self.container[known.appearance()] = item_list
    # Otherwise, store it based on raw appearance.
    # else: