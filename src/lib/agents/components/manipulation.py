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
from src.lib.util.command import Command, CommandRegistry as CMD
from src.lib.util.mixin import Mixin

"""Actions."""

"""Moving Agents to or from manipulators."""

class Pickup(Action):
    """Remove an Agent from the environment, placing it into your manipulator exclusively."""
    phases = [
        ("touch", "target", "manipulator"),
        ("grasp", "target", "manipulator"),
        ("force", "target", "manipulator"),
    ]

class Putdown(Action):
    """Remove an item from your manipulator, placing it into the environment exclusively."""
    phases = [
        ("touch", "item", "manipulator"),
        ("grasp", "item", "manipulator"),
        ("force", "item", "manipulator"),
        ("ungrasp", "item", "manipulator"),
    ]

class Drop(Action):
    """Let an item fall from your manipulator into the environment (uncontrolled)."""
    phases = [
        ("touch", "item", "manipulator"),
        ("grasp", "item", "manipulator"),
        ("ungrasp", "item", "manipulator"),
    ]

class Pack(Action):
    """Remove an item from your manipulator, placing it into a container exclusively."""
    phases = [
        ("touch", "target", "manipulator"),
        ("grasp", "target", "manipulator"),
        ("force", "target", "manipulator"),
        ("store", "target", "container", "manipulator"),
        ("ungrasp", "target", "manipulator"),
    ]

class UnPack(Action):
    """Remove an item from a container, placing it into your manipulator exclusively."""
    phases = [
        ("touch", "target", "manipulator"),
        ("grasp", "target", "manipulator"),
        ("force", "target", "manipulator"),
        ("unstore", "target", "container", "manipulator"),
    ]

"""Interacting with Agents using manipulators."""

class Use(Action):
    """Use a target using a manipulator."""
    phases = [
        ("touch", "target", "manipulator"),
        ("grasp", "target", "manipulator"),
        ("handle", "target", "manipulator"),
        ("use", "target", "manipulator")
    ]

"""Interacting with Agents using manipulators in a way requiring holding them."""

class Wield(Action):
    """"Hold an item in a manipulator out in front of you."""
    phases = [
        ("touch", "item", "manipulator"),
        ("grasp", "item", "manipulator"),
        ("force", "item", "manipulator"),
        ("ready", "item", "manipulator"),
    ]

    def get_phases(self):
        yield "touch", "target", "manipulator"
        if self("touch", "target"): yield "grasp", "target", "manipulator"
        if self("grasp", "target"): yield "force", "target", "manipulator"
        if self("force", "target"): yield "ready", "target", "manipulator"

class UnWield(Action):
    """Lower an item in a manipulator to your side."""
    phases = [
        ("touch", "item", "manipulator"),
        ("grasp", "item", "manipulator"),
        ("force", "item", "manipulator"),
        ("unready", "item", "manipulator"),
    ]

class Brandish(Action):
    """Point at a target using a second, wielded target.

    n.b. - This may unready your second target! For example, pointing a
    warhammer at someone makes it rather useless for combat.
    """
    phases = [
        ("touch", "item", "manipulator"),
        ("grasp", "item", "manipulator"),
        ("force", "item", "manipulator"),
        ("ready", "item", "manipulator"),
    ]

class UnBrandish(Action):
    """Stop pointing at a target using a second, wielded target."""
    phases = [
        ("touch", "item", "manipulator"),
        ("grasp", "item", "manipulator"),
        ("force", "item", "manipulator"),
        ("unready", "item", "manipulator"),
    ]

class Throw(Action):
    """Throw a target at a second target."""
    phases = [
        ("touch", "item", "manipulator"),
        ("grasp", "item", "manipulator"),
        ("force", "item", "manipulator"),
        ("unready", "item", "manipulator"),
    ]

"""Commands."""

"""Retrieve items."""

class Get(Command):
    """Pick up a single nearby item."""
    description = "pick up an item"
    defaults = ("g",)

    def get_actions(self):
        yield Pickup
        if self(Pickup): yield Pack

class GetAll(Command):
    """Pick up multiple nearby items."""
    description = "pick up all items"
    defaults = ("G",)

    def get_actions(self):
        yield Pickup
        if self(Pickup): yield Pack

CMD.register(Get, GetAll)

"""Change how an item is manipulated."""

class ReadyWeapon(Command):
    description = "ready an unreadied weapon"
    defaults = ("r",)

class WieldWeapon(Command):
    description = "wield a weapon"
    defaults = ("w",)

    def get_actions(self):
        yield Wield, "target"

CMD.register(ReadyWeapon, WieldWeapon)

"""Manipulate an agent."""

class UseTerrain(Command):
    description = "use a terrain feature"
    defaults = ("U",)

    def get_actions(self):
        yield Use, "target"

CMD.register(UseTerrain)

"""Mixins."""

class ReachMixin(Mixin):
    """Provides the ability to reach a target with a manipulator."""

    def can_reach(self, target, manipulator):
        return True

    def do_reach(self, target, manipulator):
        return True

class TouchMixin(Mixin):
    """Provides the ability to touch a target with a manipulator."""

    def can_touch(self, target, manipulator):
        return True

    def do_touch(self, target, manipulator):
        return True

class UnTouchMixin(Mixin):
    """Provides the ability to stop touching a target with a manipulator."""

    # STUB
    def can_untouch(self, target, manipulator):
        return True

    # STUB
    def do_untouch(self, target, manipulator):
        return True

class TouchingAgent(ReachMixin, TouchMixin, UnTouchMixin):
    """Convenience Mixin to represent an Agent with touching capability."""
    pass

class GraspMixin(Mixin):
    """Provides the ability to hold a target with a manipulator."""

    # STUB
    def can_grasp(self, target, manipulator):
        return True

    # STUB
    def do_grasp(self, target, manipulator):
        return True

class UnGraspMixin(Mixin):
    """Provides the ability to let go of a target with a manipulator."""

    # STUB
    def can_ungrasp(self, target, manipulator):
        return True

    # STUB
    def do_ungrasp(self, target, manipulator):
        return True

class GraspingAgent(TouchingAgent, GraspMixin, UnGraspMixin):
    """Convenience Mixin to represent an Agent with grasping capability."""
    pass

class WieldMixin(Mixin):
    """Provides the ability to hold a target with a manipulator in a way
    permitting its use as a tool.
    """

    # STUB
    def can_wield(self, target, manipulator):
        return True

    # STUB
    def do_wield(self, target, manipulator):
        return True

class UnWieldMixin(Mixin):
    """Provides the ability to hold a target with a manipulator in a way
    permitting its use as a tool.
    """

    # STUB
    def can_unwield(self, target, manipulator):
        if not target.is_wielded(self):
            return False
        return True

    # STUB
    def do_unwield(self, target, manipulator):
        return True

class ReadyMixin(Mixin):
    """Provides the ability to raise a target held with a manipulator outward
    from your body.
    """

    # STUB
    def can_ready(self, target, manipulator):
        return True

    # STUB
    def do_ready(self, target, manipulator):
        return True

class UnReadyMixin(Mixin):
    """Provides the ability to lower a target held with a manipulator to the
    side of your body.
    """

    # STUB
    def can_unready(self, target, manipulator):
        return True

    # STUB
    def do_unready(self, target, manipulator):
        return True

class ContactMixin(Mixin):
    """Provides the ability to touch a target with a second target held in a
    manipulator.
    """

    def can_contact(self, contacted_target, contacting_target, manipulator):
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
            return False, "too close"

        # Check whether it's too far to reach
#        max_reach = self.max_reach() + item.max_reach(self.attack_option)
        if distance > max_reach:
            return False, "too far"
        return True

    def do_contact(self, contacted_target, contacting_target, manipulator):
        """Touch a target with a second target."""
        return True

class UnContactMixin(Mixin):
    """Provides the ability to stop touching a target with a second target held
    in a manipulator.
    """

    def can_uncontact(self, contacted_target, contacting_target, manipulator):
        """Whether you can stop touching a target with a second target."""
        pass

    def do_uncontact(self, contacted_target, contacting_target, manipulator):
        """Stop touching a target with a second target."""
        return True

class HoldingAgent(GraspingAgent, WieldMixin, UnWieldMixin, ReadyMixin, UnReadyMixin, ContactMixin, UnContactMixin):
    """Convenience Mixin to represent an Agent that can manipulate held Agents
    in a variety of ways."""
    pass

class ForceMixin(Mixin):
    """Provides the ability to exert force to reposition a target whose mass is controlled by you."""

    # STUB
    def can_force(self, target, manipulator):
        """Whether you can exert force to reposition a target whose mass is controlled by you.."""
        return True

    # STUB
    def do_force(self, target, manipulator):
        """Exert force to reposition a target whose mass is controlled by you."""
        return True

class SlideMixin(Mixin):
    """Provides the ability to exert force to drag, slide, or shove a target against a surface."""

    # STUB
    def can_slide(self, target, surface, manipulator):
        """Whether you can exert force to drag, slide, or shove a target against a surface."""
        return True

    # STUB
    def do_slide(self, target, surface, manipulator):
        """Exert force to drag, slide, or shove a target against a surface."""
        return True

class HandleMixin(Mixin):
    """Provides the ability to exert force to reposition or manipulate part of a target.

    n.b. - You can handle some targets even if you can't Force or Slide them."""

    # STUB
    def can_handle(self, target, manipulator):
        """Whether you can exert force to reposition or manipulate part of a target."""
        return True

    # STUB
    def do_handle(self, target, manipulator):
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
    def can_use(self, target, manipulator):
        """Whether you can use a target."""
        return True

    def do_use(self, target, manipulator):
        """Use a target."""
        target.react("on", self)
        return True

class UseAtMixin(Mixin):
    """Provides the ability to use a target at a second target.

    Unlike many other Mixins, there is no corresponding 'UnuseAt' Trait because
    this is an instantaneous effect with no 'on' state."""
    # TODO: ^ What about canceling use of an item?


    # STUB
    def can_use_at(self, target, item, manipulator):
        """Whether you can use a target at a second target."""
        return True

    # Use an item at a target.
    # STUB
    def do_use_at(self, target, item, manipulator):
        """Use a target at a second target."""
        return True

class UsingAgent(TouchingAgent, UseMixin, UseAtMixin):
    """Convenience Mixin to represent an Agent that use its manipulators to use other Agents."""
    pass

class StoreMixin(Mixin):
    """Provides the ability to store targets into a Container."""

    # TODO: Don't use a limit of 5 entries (testing only!).    
    def can_store(self, target, manipulator, container=None):
        """Whether you can store an item into a Container."""

        # TODO: Remove default
        if container is None:
            container = self.get_component("Container")

        if container is None:
            return False

        if container.count() > 5:
            return False
        return True

    # Store an item in your container.
    def do_store(self, target, manipulator, container=None):
        """Store an item into a Container."""

        # TODO: Remove default
        if container is None:
            container = self.get_component("Container")

        if container is None:
            return False

        if target.react("on", container) is False:
            return False

        if container.add(target):
            return True
        return False

class UnstoreMixin(Mixin):
    """Provides the ability to unstore targets from a Container."""

    def can_unstore(self, target, manipulator, container=None):
        """Whether you can unstore an item from a Container."""

        # TODO: Remove default
        if container is None:
            container = self.get_component("Container")

        if container is None:
            return False

        return True

    def do_unstore(self, target, manipulator, container=None,):
        """Unstore an item from a Container."""

        # TODO: Remove default
        if container is None:
            container = self.get_component("Container")

        if container is None:
            return False

        matches = container.get(target.appearance(), [])
        assert target in matches
        matches.remove(target)
        container[target.appearance()] = matches
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