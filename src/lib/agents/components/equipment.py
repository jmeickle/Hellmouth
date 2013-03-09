"""Provides functionality for Agents to use equipment."""

from src.lib.agents.components.action import Action
from src.lib.agents.components.component import Component, ignore_results
from src.lib.agents.components.manipulation import Pack
from src.lib.util.command import Command, CommandRegistry
from src.lib.util.mixin import Mixin

"""Actions."""

"""Interacting with Agents using manipulators."""

class Equip(Action):
    """Attach a target to your body."""
    phases = [
        ("touch", "target"),
        ("grasp", "target"),
        ("handle", "target"),
        ("equip", "target")
    ]

class UnEquip(Action):
    """Remove a target from your body."""
    phases = [
        ("touch", "target"),
        ("grasp", "target"),
        ("handle", "target"),
        ("unequip", "target")
    ]

"""Commands."""

class Wear(Command):
    description = "wear an item"
    defaults = ("W",)

    def get_actions(self):
        yield UnPack
        if self(UnPack): yield UnEquip

class Remove(Command):
    description = "remove an item"
    defaults = ("R",)

    def get_actions(self):
        yield UnEquip
        if self(UnEquip): yield Pack

CommandRegistry.register(Wear, Remove)

"""Components."""

class Equipment(Component):
    """Allows an Agent to equip Agents on itself."""
    commands = []

    # TODO: Less hack-ish.
    def drop_grasped(self):

        for agent in self.grasped():
            self.process("drop", agent)

    def get_weapons(self):
        return []

    @ignore_results
    def get_worn(self):
        """Get a list representation of the Agent's worn Equipment."""
        return self.owner.values("Body", "get_worn")

    @ignore_results
    def get_containers(self):
        """Get a nested representation of the Actor's Containers and their contents."""
        return self.owner.values("Body", "get_containers")

        # if self.is_holding_items() is False:
        #     return False
        # for loc in self.body.locs.values():
        #     for appearance, itemlist in loc.held.items():
        #         for item in itemlist:
        #             self._drop(item)
        # TODO: Change message.
        #log.add("%s drops its items!" % self.appearance())

    # def add(self, agent):
    #     """Add an Agent to this Container."""
    #     matches = self.contents.get(agent.appearance(), [])

    #     # This covers only the case of that exact item already being in container.
    #     assert agent not in matches

    #     matches.append(agent)
    #     self.contents[agent.appearance()] = matches

    #     return True

    # def remove(self, agent):
    #     """Remove an Agent from this Container."""
    #     matches = self.contents.get(agent.appearance(), [])

    #     # This covers only the case of that exact item already being in container.
    #     assert agent in matches

    #     matches.remove(agent)
    #     if matches:
    #         self.contents[agent.appearance()] = matches
    #     else:
    #         del self.contents[agent.appearance()]

    #     return True

    # def count(self):
    #     """Return the number of Agents inside this Container."""
    #     return len(self.contents)

"""Mixins."""

#     # Whether you believe you can retrieve an item in your inventory.
#     @checks_item_memory
#     def believe_unstore(self, item):
#         return self.can_unstore(item)

#     # Retrieve an item in your inventory.
#     # TODO: Nicer way of doing item memory?
#     def do_unstore(self, item):   
#         # Retrieve the item based on known properties, if you have item memory.
#         if hasattr(self, 'memory'):
#             known = self.memory.get(item, Item())
#             item_list = self.inventory.get(known.appearance(), [])
#             item_list.remove(item)
#             self.inventory[known.appearance()] = item_list
#         # Otherwise, retrieve it based on raw appearance.
#         else:
#             item_list = self.inventory.get(item.appearance(), [])
#             item_list.remove(item)
#             self.inventory[item.appearance()] = item_list
#         return True

#     #
#     # EQUIP:
#     #

#     # Whether you believe you can equip an item.
#     @checks_item_memory
#     def believe_equip(self, item, usage=None, slots=None):
#         return self.can_equip(item, usage, slots)

#     # Whether you can equip an item.
#     def can_equip(self, item, usage=None, slots=None):
#         # TODO: Allow items to be equipped multiply?
#         if item.equipped() is True:
#             return False

#         # TODO: Move usage/slots retrieval into a wrapper function?

#         # Use the item's preferred usage if not provided.
#         if usage is None:
#             usage = item.preferred_usage()

#         # Use the item's preferred slots if not provided.
#         if slots is None:
#             slots = item.preferred_slots(usage)

#         # Check the applicability of the provided usage for each slot.
#         validity = True
#         results = []
#         for slot in slots:
#             result = getattr(self.body.locs[slot], "can_" + usage)(item)
#             results.append((result, slot))
#             if result is False:
#                 valid = False

#         # Return overall validity and a list of slot results.
#         return (validity, results)

#     # Equip an item.
#     # TODO: Nicer way of doing item memory?
#     def do_equip(self, item, usage=None, slots=None):
#         if hasattr(self, 'memory'):
#             known = self.memory.get(item, Item())
#         else:
#             known = item

#         # TODO: Move usage/slots retrieval into a wrapper function?

#         # Use the item's preferred usage if not provided.
#         if usage is None:
#             usage = known.preferred_usage()

#         # Use the item's preferred slots if not provided.
#         if slots is None:
#             slots = known.preferred_slots(usage)

#         # Perform the provided usage for each slot.
#         validity = True
#         results = []
#         for slot in slots:
#             result = getattr(self.body.locs[slot], "do_" + usage)(item)
#             results.append((result, slot))
#             if result is False:
#                 validity = False

#         return (validity, results)

#     #
#     # UNEQUIP:
#     #

#     # Whether you believe you can unequip an item.
#     @checks_item_memory
#     def believe_unequip(self, item, usage=None, slots=None):
#         return self.can_unequip(item, usage, slots)

#     # Whether you can unequip an item.
#     def can_unequip(self, item, usage=None, slots=None):
#         if item.equipped() is False:
#             return False

#         # TODO: Pass in usage/slots

#         # Use the item's preferred usage if not provided.
#         if usage is None:
#             usage = item.preferred_usage()

#         # Use the item's preferred slots if not provided.
#         if slots is None:
#             slots = item.preferred_slots(usage)

#         # Check the applicability of the provided removal for each slot.
#         validity = True
#         results = []
#         for slot in slots:
#             result = getattr(self.body.locs[slot], "can_un" + usage)(item)
#             results.append((result, slot))
#             if result is False:
#                 valid = False

#         # Return overall validity and a list of slot results.
#         return (validity, results)

#     # Unequip an item.
#     # TODO: Nicer way of doing item memory?
#     def do_unequip(self, item, usage=None, slots=None):
#         # if hasattr(self, 'memory'):
#         #     known = self.memory.get(item, Item())
#         # else:
#         #     known = item

#         # TODO: Pass in usage/slots

#         # Use the item's preferred usage if not provided.
#         if usage is None:
#             usage = item.preferred_usage()

#         # Use the item's preferred slots if not provided.
#         if slots is None:
#             slots = item.preferred_slots(usage)

#         # Perform the provided usage for each slot.
#         validity = True
#         results = []
#         for slot in slots:
#             result = getattr(self.body.locs[slot], "do_" + usage)(item)
#             results.append((result, slot))
#             if result is False:
#                 validity = False

#         return (validity, results)