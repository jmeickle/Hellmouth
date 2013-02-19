import random
from src.lib.util.hex import *
from src.lib.util.text import *

class Cell:
    def __init__(self, pos, parent):
        self.map = parent
        self.pos = pos

        # Stuff inside the cell
        self.actor = None
        self.actors = []
        self.terrain = None
        self.items = {}

    # Return a random actor.
    def random_actor(self):
        if not self.actors:
            return
        return random.choice(self.actors)

    # STUB
    def put_terrain(self, terrain):
        self.terrain = terrain
        terrain.cell = self

    # Return a glyph to display for this cell.
    # TODO: improve this function greatly
    def draw(self, all=False):
        glyphs = []
        if self.actors:
            for actor in self.actors:
                glyph = actor.glyph
                color = actor.color
                # TODO: HACK
                if actor.get("Status", "unconscious") is True:
                    if len(self.actors) > 1 and all is False:
                        color += "-magenta"
                    else:
                        color += "-black"
                else:
                    color += "-white"
                glyphs.append((glyph, color, actor.subposition))
        elif self.terrain is not None:
            glyphs.append((self.terrain.glyph, self.terrain.color, CC))
        elif len(self.items) == 1:
            # TODO: Ick!
            for itemlist in self.items.values():
                item = random.choice(itemlist)
                glyphs.append((item.glyph, item.color, CC))
        elif len(self.items) > 1:
            glyphs.append(('+', 'red-black', CC))
        else:
            glyphs.append(self.map.floor + (CC,))
        if all is False:
            return glyphs[0]
        else:
            return glyphs

    # TODO: Options for what to list.
    # TODO: This should go through the 'describe' functions; it should only be returning information, not strings!
    def contents(self):
        list = []
        if self.actors:
            for actor in self.actors:
                list.append("a %s" % actor.appearance())
        if self.terrain is not None:
            list.append("a %s" % self.terrain.name)
        if len(self.items) > 0:
            for appearance, itemlist in self.items.items():
                list.append(appearance)
        if not list:
            list.append("nothing of interest")
        return commas(list)

    # ITEMS

    # 'Forcibly' put an item into a cell.
    def _put(self, item):
        list = self.items.get(item.appearance(), None)
        if list is None:
            self.items[item.appearance()] = [item]
        else:
            list.append(item)

    # Put an item into a cell.
    # TODO: Sanity checks that _put doesn't have.
    def put(self, item):
        self._put(item)

    # 'Forcibly' remove a specific item from a cell.
    # Returns the item if it's successfully removed.
    # Returns false if there are no items matching that appearance.
    # Errors if the item is not in the list.
    def _get(self, item):
        list = self.items.get(item.appearance, None)
        if list is not None:
            return list.remove(item)
        else:
            return False

    # Remove a random item of a given appearance from a cell.
    # Returns the item if it's successfully removed.
    # Returns false if there are no items matching the appearance.
    def get(self, appearance):
        list = self.items.get(appearance, None)
        if list is not None:
            return list.remove(random.choice(list))
        else:
            return False

    # Take an appearance and a list, and tack it onto the cell contents.
    def _merge(self, appearance, list):
        current = self.items.get(appearance, None)
        if current is not None:
            return current.extend(list)
        else:
            self.items[appearance] = list

    # Boolean: whether you can get items from a cell
    # STUB: Add real checks here.
    def can_get(self):
        return True

    # Boolean: whether you can put items into a cell
    # STUB: Add real checks here.
    def can_put(self):
        return True

    # Returns how many items of a given appearance are in the cell.
    def count(self, appearance):
        list = self.items.get(item.appearance, None)
        if list is None:
            return 0
        else:
            return len(list)

    def get_items(self):
        """Get all the items in a cell."""
        items = []
        for item in [item for item in self.items.values()]:
            items.extend(item)
        return items

    # ACTORS

    # Add a actor to a cell.
    def add(self, obj, terrain=False):
        if obj is None:
            exit("Tried to place a non-object")

        if terrain is False:
            self.actors.append(obj)
        else:
            if self.terrain is None:
                self.terrain = obj
                if self.terrain is None:
                   exit("No terrain after placement")
            else:
                return False

    # Stub, for eventually handling multiple things
    def remove(self, obj):
        self.actors.remove(obj)

    # MOVEMENT

    # Return whether the cell has a creature in it.
    def occupied(self):
        if self.actors:
            return True
        return False

    # A list of actors that are blocking movement within a hex.
    def intervening_actors(self, subposition, dir):
        actors = []

        for actor in self.actors:
            # You can always move out of a subposition you're in.
            if subposition == actor.subposition:
                continue

            blocked = []
            # Centrally-located actors block four spots in total.
            if actor.subposition == CC:
                blocked = [CC]
                blocked.extend(arc(flip(subposition)))
            else:
                blocked.extend(arc(actor.subposition))
            if dir in blocked:
                actors.append(actor)
        return actors

    # Whether it's possible to enter a hex from a given direction.
    def accessible_from(self, dir):
        if self.intervening_actors(flip(dir), dir):
            return False
        return True

    # Return whether the cell has blocking terrain in it.
    def impassable(self):
        if self.terrain is not None:
            if self.terrain.blocking is True:
                return True
        return False

    # Return whether the cell is passable
    def blocked(self, dir=CC):
        if self.impassable() is True:
            return True
        if self.occupied() is True:
            if self.accessible_from(dir) is True:
                return True
        return False

