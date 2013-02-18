"""Defines the Components and Traits that provide inventory functionality to Agents."""

from src.lib.util import db, key
from src.lib.agents.components.component import Component

# TODO: Use database tables!
# On import, try to create the necessary database tables.
# db.query("CREATE TABLE IF NOT EXISTS item (iid int, PRIMARY KEY (iid))")
# db.query("CREATE TABLE IF NOT EXISTS inventory (aid int, root int, depth int, PRIMARY KEY (aid))")
# db.query("CREATE TABLE IF NOT EXISTS inventory_item (aid int, iid int)")
# db.query("CREATE TABLE IF NOT EXISTS item_tag (iid int, tid int, detail int, tag text)")

# TODO: Check item memory!
# # Decorator that forces a function to check an actor's item memory.
# def checks_item_memory(fn):
#     def wrapped(self, *args):
#         if hasattr(self, 'item_memory'):
#             known = (self.item_memory.get(item, Item()),) + args[1:]
#         return fn(self, *args)
#     return wrapped

class Inventory(Component):
    """Defines the ability to contain targets inside or on an Agent."""

    def __init__(self, owner):
        self.inventory = {}
        self.owner = owner

    def count(self):
        return len(self.inventory)

class Store(object):
    """Provides the ability to store targets into an Inventory."""

    # # Whether you believe you can store an item in your inventory.
    # # @checks_item_memory
    # def believe_store(self, item):
    #     return self.can_store(item)

    # Whether you can store an item in your inventory.
    # TODO: Don't use a limit of 5 entries (testing only!).    
    def can_store(self, target):
        """Whether you can store an item into an Inventory."""
        if self.Inventory.count() > 5:
            return False
        return True

    # Store an item in your inventory.
    def do_store(self, target):
        """Store an item into an Inventory."""

        # Store the item based on known properties, if you have item memory.
        # TODO: Nicer way of doing item memory?
        # if hasattr(self, 'memory'):
        #     known = self.memory.get(item, Item())
        #     item_list = self.inventory.get(known.appearance(), [])
        #     item_list.append(item)
        #     self.inventory[known.appearance()] = item_list
        # Otherwise, store it based on raw appearance.
        # else:
        matches = self.inventory.get(target.appearance(), [])
        assert target not in matches
        matches.append(target)
        self.inventory[target.appearance()] = matches
        return True

class Unstore(object):
    """Provides the ability to unstore targets from an Inventory."""

    def can_unstore(self, target):
        """Whether you can unstore an item from an Inventory."""
        return True

    def do_unstore(self, target):
        """Unstore an item from an Inventory."""
        matches = self.inventory.get(target.appearance(), [])
        assert target in matches
        matches.remove(target)
        self.inventory[target.appearance()] = matches        
        return True

class InventoryAgent(Store, Unstore):
    pass

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

# # Provides the ability to make use of targets inside or on self.
# class Equipment():

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

# # Provides the ability to manipulate targets inside or on self.
# class Manipulation():

# # brandish, unbrandish
# # ready, unready
# # handle
# # use_at
# # contact

# Decorator testing.
# if __name__ == '__main__':

    # def checks_knowledge(fn):
    #     def wrapped(self, *args):
    #         if hasattr(self, 'complicated'):
    #             args = ("complication",) + args[1:]
    #         return fn(self, *args)
    #     return wrapped

    # class Simple:
    #     def test(self, tag):
    #         print "Hi! %s" % tag

    # class Complicated(Simple):

    #     @checks_knowledge
    #     def test(self, tag):
    #         print "Hiiii! %s" % tag

    # a = Simple()
    # b = Complicated()
    # a.test("br")
    # b.test("br")
    # b.complicated = True
    # b.test("br")



#for run in range(len(run_results)):
#    t1, t2, num_items = run_results[run]


    # tag_enums = ("color", "shape", "size", "weight", "material")
    # tag_values = (
    #     ["red", "blue", "green"],
    #     ["sphere", "cube", "tetrahedron"],
    #     ["tiny", "average", "big"],
    #     ["light", "normal", "heavy"],
    #     ["wood", "metal", "bone"]
    #     )

    # import random
    # import time

    # run_results = []
    # runs = 100
    # for run in range(runs):
    #     t1 = time.time()

    #     # Make database
        



    #     # Set up inventories
    #     for i in range(20):
    #         conn.execute("INSERT INTO inventory(aid, root, depth) VALUES (?, ?, ?)", (i, None, None))

    #     num_items = 1000
    #     for i in range(num_items):
    #         conn.execute("INSERT INTO item(iid) VALUES (?)", (i,))
    #         conn.execute("INSERT INTO inventory_item(aid, iid) VALUES (?, ?)", (random.choice(range(20)), i))

    #         num_tags = 1 + random.choice(range(4))
    #         for tag in range(num_tags):
    #             tid = random.choice(range(5))
    #             lod = random.choice(range(3))
    #             tag_text = random.choice(tag_values[tid])
    #             conn.execute("INSERT INTO item_tag(iid, tid, detail, tag) VALUES (?, ?, ?, ?)", (i, tid, lod, tag_text))        

    #     txt = random.choice(tag_values[random.choice(range(5))])
    #     results = conn.execute('''SELECT item.iid, item_tag.tid, item_tag.tag FROM item
    #         LEFT JOIN inventory_item ON item.iid == inventory_item.iid
    #         LEFT JOIN inventory ON inventory.aid == inventory_item.aid
    #         LEFT JOIN item_tag ON item.iid == item_tag.iid WHERE item_tag.tag = ? AND item_tag.detail < ? AND item.iid < ?''', (txt, random.choice((1,2,3)), random.choice(range(num_items))))
    #     num_results = 0
    #     for result in results:
    #         num_results += 1
    #     #for iid, tid, tag in results:
    #         #= result
    #         # print "Item #%s has '%s: %s'." % (iid, tag_enums[tid], tag)

    #     conn.close()
    #     t2 = time.time()
    #     run_results.append((t1,t2, num_results))
    #     print 'Run %s: retrieved %s items in %0.3f ms' % (run+1, num_results, (t2-t1)*1000.0)