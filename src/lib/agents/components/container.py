"""Provides functionality for Agents to contain other Agents (typically items) inside of themselves."""

from src.lib.agents.components.component import Component

from src.lib.util import debug
from src.lib.util.result import accumulate_results, ignore_results

"""Components."""

class Container(Component):
    """Allows an Agent to contain other Agents inside of itself."""
    commands = []

    def __init__(self, owner):
        self.contents = {}
        self.owner = owner

    """Content getter methods."""

    @accumulate_results
    def get_contents(self):
        """Yield keyed lists of Agents inside the Container."""
        for key, itemlist in self.contents.items():
            yield ((key, itemlist))

    @accumulate_results
    def get_list(self):
        """Yield a flat list of Agents inside the Container."""
        for itemlist in self.contents.values():
            for item in itemlist:
                yield item

    """Content setter methods."""

    def add_contents(self, agent):
        """Add an Agent to a keyed list in this Container."""
        matches = self.contents.get(agent.appearance(), [])

        # This covers only the case of that exact item already being in container.
        if agent in matches: debug.die("Tried to add agent %s to container %s." % (agent, self))

        matches.append(agent)
        self.contents[agent.appearance()] = matches

        return True

    def remove_contents(self, agent):
        """Remove an Agent from a keyed list in this Container."""
        matches = self.contents.get(agent.appearance(), [])

        # This covers only the case of that exact item already being in container.
        if agent not in matches: debug.die("Tried to remove agent %s from container %s." % (agent, self))

        matches.remove(agent)
        if matches:
            self.contents[agent.appearance()] = matches
        else:
            del self.contents[agent.appearance()]

        return True

    """Content utility methods."""

    def count_contents(self):
        """Return the number of Agents inside this Container."""
        return len([agent for agent in self.get_list()])

    # Not currently working:
    # @ignore_results
    # def get(self, key, default=None):
    #     """Default get method."""
    #     # results = [res for res in self.get_contents()]
    #     # if results:
    #     #     exit("key %s, dict %s" % (key, results))
    #     for appearance, itemlist in self.get_contents():
    #         for item in itemlist:
    #             if key == item:
    #                 return True
    #     return False

#    def get_matches(self, appearance):
#        for appearance, itemlist in self.contents.items():
#            yield appearance
#            appearance
#            append = True
#            for item in itemlist:
#                if item.is_equipped() is True:
#                    append = False
#            if append is True:
#                items.append((appearance, itemlist))
#        return sorted(items, key=itemgetter(0))

# TODO: Use database tables!
# On import, try to create the necessary database tables.
#from src.lib.util import db
# db.query("CREATE TABLE IF NOT EXISTS item (iid int, PRIMARY KEY (iid))")
# db.query("CREATE TABLE IF NOT EXISTS container (aid int, root int, depth int, PRIMARY KEY (aid))")
# db.query("CREATE TABLE IF NOT EXISTS container_item (aid int, iid int)")
# db.query("CREATE TABLE IF NOT EXISTS item_tag (iid int, tid int, detail int, tag text)")

# TODO: Check item memory!
# # Decorator that forces a function to check an actor's item memory.
# def checks_item_memory(fn):
#     def wrapped(self, *args):
#         if hasattr(self, 'item_memory'):
#             known = (self.item_memory.get(item, Item()),) + args[1:]
#         return fn(self, *args)
#     return wrapped

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
    #         conn.execute("INSERT INTO container(aid, root, depth) VALUES (?, ?, ?)", (i, None, None))

    #     num_items = 1000
    #     for i in range(num_items):
    #         conn.execute("INSERT INTO item(iid) VALUES (?)", (i,))
    #         conn.execute("INSERT INTO container_item(aid, iid) VALUES (?, ?)", (random.choice(range(20)), i))

    #         num_tags = 1 + random.choice(range(4))
    #         for tag in range(num_tags):
    #             tid = random.choice(range(5))
    #             lod = random.choice(range(3))
    #             tag_text = random.choice(tag_values[tid])
    #             conn.execute("INSERT INTO item_tag(iid, tid, detail, tag) VALUES (?, ?, ?, ?)", (i, tid, lod, tag_text))

    #     txt = random.choice(tag_values[random.choice(range(5))])
    #     results = conn.execute('''SELECT item.iid, item_tag.tid, item_tag.tag FROM item
    #         LEFT JOIN container_item ON item.iid == container_item.iid
    #         LEFT JOIN container ON container.aid == container_item.aid
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