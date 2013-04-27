from copy import copy

from src.lib.objects.items.item import Item
from src.lib.util.text import *

# Corpses!
class Corpse(Item):
    def __init__(self, actor):
        Item.__init__(self)

        # Basic characteristics.
        # TODO: Derive these from the actor.
        #self.size = None
        #self.hp = None
        #self.hp_max = None
        #self.dr = None
        #self.effects = None
        #self.slots = None

        self.actor = actor

    def appearance(self):
        return self.actor.appearance() + " corpse"

class PartialCorpse(Corpse):
    def __init__(self, actor):
        Corpse.__init__(self, actor)

    def appearance(self):
        # TODO: Look up the assemblage of parts for the name of that structure.
        # e.g., "lower body" for everything groin and below.
        parts = []
        for loc in self.actor.body.locs.values():
            parts.append(loc.appearance())
        return self.actor.appearance() + " " + commas(parts)