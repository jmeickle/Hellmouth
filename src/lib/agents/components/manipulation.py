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

import random

from src.lib.agents.components.action import Action
from src.lib.agents.components.component import Component
from src.lib.agents.components.phase import Phase
from src.lib.agents.contexts.context import action_context, command_context

from src.lib.util.command import Command, CommandRegistry as CMD
from src.lib.util import debug
from src.lib.util.trait import Trait

"""Actions."""

"""Moving Agents to or from manipulators."""

class Pickup(Action):
    """Remove an Agent from the environment, placing it into your manipulator exclusively."""
    @action_context
    def get_phases(self, ctx):
        yield Phase("touch", "target", "manipulator")
        if ctx(): yield Phase("grasp", "target", "manipulator")
        if ctx(): yield Phase("force", "target", "manipulator")
        if ctx(): yield Phase("get", "target", "environment", "manipulator")

# class Putdown(Action):
#     """Remove an item from your manipulator, placing it into the environment exclusively."""
#     phases = [
#         ("touch", "item", "manipulator"),
#         ("grasp", "item", "manipulator"),
#         ("force", "item", "manipulator"),
#         ("ungrasp", "item", "manipulator"),
#     ]

# class Drop(Action):
#     """Let an item fall from your manipulator into the environment (uncontrolled)."""
#     phases = [
#         ("touch", "item", "manipulator"),
#         ("grasp", "item", "manipulator"),
#         ("ungrasp", "item", "manipulator"),
#     ]

class Pack(Action):
    """Remove an item from your manipulator, placing it into a container exclusively."""
    @action_context
    def get_phases(self, ctx):
        yield Phase("touch", "target", "manipulator")
        if ctx(): yield Phase("grasp", "target", "manipulator")
        if ctx(): yield Phase("force", "target", "manipulator")
        if ctx():
            yield Phase("store", "target", "container", "manipulator")
            if ctx(): yield Phase("ungrasp", "target", "manipulator")
        else:
            yield Phase("ungrasp", "target", "manipulator")
        if ctx(): yield Phase("untouch", "target", "manipulator")

class Unpack(Action):
    """Remove an item from a container, placing it into your manipulator exclusively."""
    @action_context
    def get_phases(self, ctx):
        yield Phase("touch", "target", "manipulator")
        if ctx(): yield Phase("grasp", "target", "manipulator")
        if ctx(): yield Phase("force", "target", "manipulator")
        if ctx():
            yield Phase("unstore", "target", "container", "manipulator")

"""Interacting with Agents using manipulators."""

class Use(Action):
    """Use a target using a manipulator."""
    @action_context
    def get_phases(self, ctx):
        yield Phase("touch", "target", "manipulator")
        if ctx(): yield Phase("grasp", "target", "manipulator")
        if ctx(): yield Phase("handle", "target", "manipulator")
        if ctx(): yield Phase("use", "target", "manipulator", "use")

"""Interacting with Agents using manipulators in a way requiring holding them."""

class Wield(Action):
    """"Hold an item in a manipulator out in front of you."""
    @action_context
    def get_phases(self, ctx):
        yield Phase("touch", "target", "manipulator")
        if ctx(): yield Phase("grasp", "target", "manipulator")
        if ctx(): yield Phase("force", "target", "manipulator")
        if ctx(): yield Phase("wield", "target", "manipulator")
        if ctx(): yield Phase("ready", "target", "manipulator")

# class UnWield(Action):
#     """Lower an item in a manipulator to your side."""
#     phases = [
#         ("touch", "item", "manipulator"),
#         ("grasp", "item", "manipulator"),
#         ("force", "item", "manipulator"),
#         ("unready", "item", "manipulator"),
#     ]

# class Brandish(Action):
#     """Point at a target using a second, wielded target.

#     n.b. - This may unready your second target! For example, pointing a
#     warhammer at someone makes it rather useless for combat.
#     """
#     phases = [
#         ("touch", "item", "manipulator"),
#         ("grasp", "item", "manipulator"),
#         ("force", "item", "manipulator"),
#         ("ready", "item", "manipulator"),
#     ]

# class UnBrandish(Action):
#     """Stop pointing at a target using a second, wielded target."""
#     phases = [
#         ("touch", "item", "manipulator"),
#         ("grasp", "item", "manipulator"),
#         ("force", "item", "manipulator"),
#         ("unready", "item", "manipulator"),
#     ]

# class Throw(Action):
#     """Throw a target at a second target."""
#     phases = [
#         ("touch", "item", "manipulator"),
#         ("grasp", "item", "manipulator"),
#         ("force", "item", "manipulator"),
#         ("unready", "item", "manipulator"),
#     ]

"""Commands."""

"""Retrieve items."""

class Get(Command):
    """Pick up a single nearby item."""
    description = "pick up an item"
    defaults = ("g",)

    @command_context
    def get_actions(self, ctx):
        yield Pickup
        if ctx(Pickup): yield Pack

class GetAll(Command):
    """Pick up multiple nearby items."""
    description = "pick up all items"
    defaults = ("G",)

    @command_context
    def get_actions(self, ctx):
        yield Pickup
        yield Pack

CMD.register(Get, GetAll)

"""Change how an item is manipulated."""

class ReadyWeapon(Command):
    short_desc = "ready"
    description = "ready an unreadied weapon"
    defaults = ("r",)

    # TODO: Distinct Ready action?
    @command_context
    def get_actions(self, ctx):
        yield Wield

class WieldWeapon(Command):
    short_desc = "wield"
    description = "wield a weapon from inventory"
    defaults = ("w",)

    @command_context
    def get_actions(self, ctx):
        yield Unpack
        yield Wield

CMD.register(ReadyWeapon, WieldWeapon)

"""Manipulate an agent."""

class UseTerrain(Command):
    description = "use a terrain feature"
    defaults = ("U",)

    @command_context
    def get_actions(self, ctx):
        yield Use

# TODO: Move to Movement.
class UsePassage(Command):
    description = "travel to a different map"
    defaults = ("<", ">")

    @command_context
    def get_actions(self, ctx):
        yield Use

CMD.register(UseTerrain, UsePassage)

"""Components."""

class Manipulation(Component):
    """Component that handles an Agent's manipulation capabilities."""

    commands = []

    def can_reach(self, target, wielded=None, manipulator=None):
        """Return whether the Agent can reach when manipulating."""
        if not wielded and not manipulator: debug.die("Tried to check reach without providing an item or manipulator.")
        if wielded and not manipulator:
            manipulator = wielded.call("Wielded", "get_manipulator").get_result()
        # die("target %s, wielded %s, manip %s" % (target, wielded, manipulator))

        min_reach, max_reach = self.get_reach(wielded, manipulator)
        distance = self.owner.dist(target)
        # die("dist %s, min %s, max %s" % (distance, min_reach, max_reach))

        # Check whether it's too close to reach
        if distance < min_reach:
            return False#, "too close"

        # Check whether it's too far to reach
        if distance > max_reach:
            return False#, "too far"

        return True

    def get_reach(self, wielded=None, manipulator=None):
        min_reach = 0
        max_reach = 0

        body_reach = self.owner.call("Body", "get_reach").get_result()
        if body_reach:
            max_reach += body_reach

        if wielded:
            wielded_reach = wielded.call("Wielded", "get_reach").get_result()
            if wielded_reach:
                wielded_min_reach, wielded_max_reach = wielded_reach
                min_reach += wielded_min_reach
                max_reach += wielded_max_reach

        if manipulator:
            manipulator_min_reach, manipulator_max_reach = manipulator.get_reach()
            min_reach += manipulator_min_reach
            max_reach += manipulator_max_reach

        return min_reach, max_reach

    # TODO: redo manipulation as a controlled component

    def get_manipulators(self):
        """Yield manipulators."""
        return self.owner.values("Body", "get_manipulators")

    def get_grasped(self, manipulators=None):
        """Yield Agents grasped by this Agent."""
        if not manipulators:
            manipulators = self.get_manipulators()

        for manipulator in manipulators:
            for agent in manipulator.get_grasped():
                yield agent

    def get_wielded(self, manipulators=None):
        """Yield Agents wielded by this Agent."""
        if not manipulators:
            manipulators = self.get_manipulators()

        for manipulator in manipulators:
            for agent in manipulator.get_wielded():
                yield agent

    # TODO: Less hack-ish.
    def drop_grasped(self):
        """Drop all grasped items."""
        for agent in self.get_grasped():
            yield self.call("Manipulation", Drop, agent)

class Grasped(Component):
    """Component that handles a grasped Agent's functionality."""
    def __init__(self, owner, controller, manipulator):
        super(Grasped, self).__init__(owner)

        self.controller = controller
        self.manipulator = manipulator

class Wielded(Component):
    """Component that handles a wielded Agent's functionality."""

    def __init__(self, owner, controller, manipulator):
        super(Wielded, self).__init__(owner)

        self.controller = controller
        self.manipulator = manipulator
        self.wielding_mode = 0
        self.wielding_modes = []
        self.ready = True

    def trigger(self, *triggers):
        """Respond to triggers."""
        if "rebuild" in triggers:
            self.rebuild_wielding_modes()

    # TODO: this is definitely nottttttt the way to do this...
    def rebuild_wielding_modes(self):
        self.wielding_mode = 0
        self.wielding_modes = []
        if hasattr(self.owner, "get_wielding_modes"):
            for mode in self.owner.get_wielding_modes():
                if self.controller.trait(mode[0]): # TODO: ICK. (Skipping past modes with no skill)
                    self.wielding_modes.append(mode)

    """Wielding getter methods."""

    def get_wielding_mode(self):
        """Return the current wielding mode."""
        if self.wielding_modes:
            return self.wielding_modes[self.wielding_mode]

    def get_parry(self, can_retreat, retreat_positions):
        """Get the parry value of this wielded agent."""
        wielding_mode = self.get_wielding_mode()

        # TODO: Bug!
        if not wielding_mode:
            return False, None

        # Wielding mode, for now:
        #  0      1        2      3      4      5       6,     7
        # trait, name, damage, d.type, reach, parry, min ST, hands

        parry_mod = wielding_mode[5]
        # TODO: Handle balanced
        # if isinstance(parry_mod, tuple):
        #     parry_mod, balanced = parry_mod
        # else:
        #     balanced = True

        trait_name = wielding_mode[0]
        trait_level = self.controller.trait(trait_name)

        if not trait_level:
            return False, None

        parry_value = trait_level/2 + 3 + parry_mod

        # TODO: Choose retreat position more intelligently
        retreat_position = random.choice(retreat_positions) if retreat_positions else None

        if can_retreat:
            parry_value += 1

        # TODO: Handle previous parries
        return parry_value, retreat_position

    def get_manipulator(self):
        return self.manipulator

    def get_reach(self):
        """Return the minimum and maximum reach of the current wielding mode, exclusive of manipulator."""
        wielded = self.get_wielding_mode()
        if wielded:
            return self.owner.get_reach(self.get_wielding_mode())
        return False

    """Wielding setter methods."""

    def set_ready(self, readiness):
        """Set whether the wielded Agent is ready."""
        self.ready = readiness
        return True

    def set_wielding_mode(self, amount):
        """Return the current wielding mode."""
        self.wielding_mode += amount

        if self.wielding_mode >= len(self.wielding_modes):
            self.wielding_mode = 0
        elif self.wielding_mode < 0:
            self.wielding_mode = len(self.wielding_modes) - 1

"""Traits."""

class Reach(Trait):
    """Provides the ability to reach a target with a manipulator."""

    def could_reach(self):
        """Whether the Agent could reach an unspecified target."""
        return True

    def can_reach(self, target, manipulator):
        """Whether the Agent can reach a target with a manipulator."""
        return True

    def do_reach(self, target, manipulator):
        """Reach a target with a manipulator."""
        return True

    # def is_reach(self, target, manipulator):
    #     """Whether the Agent is reaching a target with a manipulator."""
    #     return True

class Touch(Trait):
    """Provides the ability to touch a target with a manipulator."""

    def could_touch(self):
        return True

    def can_touch(self, target, manipulator):
        return True

    def do_touch(self, target, manipulator):
        return True

    # def is_touch(self, target, manipulator):
    #     return True

class UnTouch(Trait):
    """Provides the ability to stop touching a target with a manipulator."""

    def could_untouch(self):
        return True

    # STUB
    def can_untouch(self, target, manipulator):
        return True

    # STUB
    def do_untouch(self, target, manipulator):
        return True

    # # STUB
    # def is_untouch(self, target, manipulator):
    #     return True

class Grasp(Trait):
    """Provides the ability to hold a target with a manipulator."""

    def could_grasp(self):
        return True

    def can_grasp(self, target, manipulator):
        if manipulator.can_grasp(target):
            return True
        return False

    def do_grasp(self, target, manipulator):
        if manipulator.do_grasp(target):
            return True
        return False

    def is_grasp(self, target, manipulator):
        if manipulator.is_grasp(target):
            return True
        return False

class UnGrasp(Trait):
    """Provides the ability to let go of a target with a manipulator."""

    def could_ungrasp(self):
        return True

    def can_ungrasp(self, target, manipulator):
        if manipulator.can_ungrasp(target):
            return True
        return False

    def do_ungrasp(self, target, manipulator):
        if manipulator.do_ungrasp(target):
            return True
        return False

    def is_ungrasp(self, target, manipulator):
        if manipulator.is_ungrasp(target):
            return True
        return False

class Wield(Trait):
    """Provides the ability to raise a target grasped with a manipulator outward
    from your body.
    """

    # TODO: argh...
    def could_wield(self):
        """Return whether the Agent could wield something."""
        for manipulator in self.values("Body", "get_manipulators"):
            if manipulator.could_wield():
                return True
        return False

    def can_wield(self, target, manipulator):
        if manipulator.can_wield(target):
            return True
        return False

    def do_wield(self, target, manipulator):
        if manipulator.do_wield(target):
            return True
        return False

    def is_wield(self, target, manipulator):
        if manipulator.is_wield(target):
            return True
        return False

class UnWield(Trait):
    """Provides the ability to lower a target grasped with a manipulator
    inward towards your body.
    """

    def can_unwield(self, target, manipulator):
        if manipulator.can_unwield(target):
            return True
        return False

    def do_unwield(self, target, manipulator):
        if manipulator.do_unwield(target):
            return True
        return False

class Ready(Trait):
    """Provides the ability to hold a wielded target in a way permitting its use as a tool."""
    # STUB
    def could_ready(self):
        return True

    # STUB
    def can_ready(self, target, manipulator):
        if self.is_ready(target, manipulator):
            return False
        return True

    # STUB
    def do_ready(self, target, manipulator):
        if target.call("Wielded", "set_ready", True).get_result():
            return True
        return False

    def is_ready(self, target, manipulator):
        """Return whether the wielded Agent is ready."""
        # TODO: access via method instead
        return target.get_component("Wielded").ready

class UnReady(Trait):
    """Provides the ability to stop holding a wielding a target in a way permitting its use as a tool."""

    # STUB
    def could_unready(self):
        return True

    # STUB
    def can_unready(self, target, manipulator):
        if target.call("Wielded", "can_ready").get_result() is False:
            return True
        return False

    # STUB
    def do_unready(self, target, manipulator):
        if target.call("Wielded", "set_ready", False).get_result():
            return True
        return False

    def is_unready(self, target, manipulator):
        """Return whether the wielded Agent is ready."""
        # TODO: fix
        return not self.is_ready(target)

class Contact(Trait):
    """Provides the ability to touch a target with a second target held in a
    manipulator.
    """

    # STUB
    def could_contact(self):
        return True

    def can_contact(self, target, instrument, manipulator):
        """Whether you can touch a target with an instrument."""
        # TODO: Restructure attack option structure so that items can figure
        # this out based on how they are being held
        return self.call("Manipulation", "can_reach", target, instrument, manipulator).get_result()

    def do_contact(self, target, instrument, manipulator):
        """Touch a target with an instrument."""
        return True

class UnContact(Trait):
    """Provides the ability to stop touching a target with a second target held
    in a manipulator.
    """

    def could_uncontact(self):
        return True

    def can_uncontact(self, target, instrument, manipulator):
        """Whether you can stop touching a target with an instrument."""
        return True

    def do_uncontact(self, target, instrument, manipulator):
        """Stop touching a target with an instrument."""
        return True

class Force(Trait):
    """Provides the ability to exert force to reposition a target whose mass is controlled by you."""

    # STUB
    def could_force(self):
        return True

    # STUB
    def can_force(self, target, manipulator):
        """Whether you can exert force to reposition a target whose mass is controlled by you.."""
        return True

    # STUB
    def do_force(self, target, manipulator):
        """Exert force to reposition a target whose mass is controlled by you."""
        return True

    # # STUB
    # def is_force(self, target, manipulator):
    #     """Exert force to reposition a target whose mass is controlled by you."""
    #     return True

class Slide(Trait):
    """Provides the ability to exert force to drag, slide, or shove a target against a surface."""

    # STUB
    def can_slide(self, target, surface, manipulator):
        """Whether you can exert force to drag, slide, or shove a target against a surface."""
        return True

    # STUB
    def do_slide(self, target, surface, manipulator):
        """Exert force to drag, slide, or shove a target against a surface."""
        return True

class Handle(Trait):
    """Provides the ability to exert force to reposition or manipulate part of a target.

    n.b. - You can handle some targets even if you can't Force or Slide them."""

    # STUB
    def could_handle(self):
        return True

    # STUB
    def can_handle(self, target, manipulator):
        """Whether you can exert force to reposition or manipulate part of a target."""
        return True

    # STUB
    def do_handle(self, target, manipulator):
        """Exert force to reposition or manipulate part of a target."""
        return True

    # # STUB
    # def is_handle(self, target, manipulator):
    #     return True

class Get(Trait):
    """Provides the ability to get a target from an environment."""

    # STUB
    def could_get(self):
        return True

    # STUB
    def can_get(self, target, environment, manipulator):
        """Whether you can get a target from an environment."""
        return True

    # STUB
    def do_get(self, target, environment, manipulator):
        """Get a target from an environment."""
        environment._get(target)
        return True

    # # STUB
    # def is_get(self, target, environment, manipulator):
    #     return True

class Put(Trait):
    """Provides the ability to put a target into an environment."""

    def could_put(self):
        return True

    # STUB
    def can_put(self, target, environment, manipulator):
        """Whether you can put a target into an environment."""
        return True

    # STUB
    def do_put(self, target, environment, manipulator):
        """Put a target into an environment."""
        environment._put(target)
        return True

class Use(Trait):
    """Provides the ability to use a target for an intended function.

    Unlike many other Traits, there is no corresponding 'Unuse' Trait because
    this is an instantaneous effect with no 'on' state."""

    # STUB
    def could_use(self):
        return True

    # STUB
    def can_use(self, target, manipulator, use):
        """Whether you can use a target."""
        return True

    # Rewrite!
    def do_use(self, target, manipulator, use):
        """Use a target."""
        target.react(self, use)
        return True

    # # STUB
    # def is_use(self, target, manipulator, use):
    #     return True

class UseAt(Trait):
    """Provides the ability to use a target at a second target.

    Unlike many other Traits, there is no corresponding 'UnuseAt' Trait because
    this is an instantaneous effect with no 'on' state."""
    # TODO: ^ What about canceling use of an item?

    def could_use_at(self):
        return True

    # STUB
    def can_use_at(self, target, instrument, manipulator, use):
        """Whether you can use an instrument at a target."""
        return True

    # Use an item at a target.
    # STUB
    def do_use_at(self, target, instrument, manipulator, use):
        """Use an instrument at a target."""
        domain, callback = instrument.get_use_callback(use)
        if domain and callback:
            self.call(domain, callback, target, instrument, manipulator).get_result()
            # TODO: Figure out whether we can continue the process
            return True
        return False

class Store(Trait):
    """Provides the ability to store targets into a Container."""

    def could_store(self):
        return True

    def can_store(self, target, container, manipulator):
        """Whether you can store an item into a Container."""
        # TODO: Don't use a limit of 5 entries (testing only!).
        if container.call("Container", "count_contents").get_result() > 5:
            return False
        return True

    # Store an item in your container.
    def do_store(self, target, container, manipulator):
        """Store an item into a Container."""
        if container.call("Container", "add_contents", target).get_result():
            return True
        return False

    # def is_store(self, target, manipulator, container):
    #     return True

class Unstore(Trait):
    """Provides the ability to unstore targets from a Container."""

    def could_unstore(self):
        return True

    def can_unstore(self, target, container, manipulator):
        """Whether you can unstore an item from a Container."""
        return True

    def do_unstore(self, target, container, manipulator):
        """Unstore an item from a Container."""
        if container.call("Container", "remove_contents", target).get_result():
            return True
        return False

    # def is_unstore(self, target, manipulator, container):
    #     """Whether you can unstore an item from a Container."""
    #     return True

"""Sets of manipulation Traits."""

TouchingTraits = {Reach, Touch, UnTouch}
PositioningTraits = TouchingTraits | {Force, Slide, Handle, Get, Put}
GraspingTraits = TouchingTraits | {Grasp, UnGrasp}
HoldingTraits = GraspingTraits | {Wield, UnWield, Ready, UnReady, Contact, UnContact}
UsingTraits = TouchingTraits | {Use, UseAt}
StoringTraits = {Store, Unstore}

ManipulatingTraits = TouchingTraits | PositioningTraits | GraspingTraits | HoldingTraits | UsingTraits | StoringTraits

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