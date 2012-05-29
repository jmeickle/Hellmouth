from dice import *
from generators.maps import mapgen
from maps.encounter import Encounter
from data import screens

class MeatArena():
    depth = 1

    def __init__(self):
        self.name = "A strange, meaty arena"
        self.floor = (".", "white-black")
        self.exits = { "down" : (MeatArena, None) }
        self.map = None
        self.generate_map()
        self.place_monsters()
        self.screens = []
        self.generate_screens()

    # Just returns depth, but can be overridden for strings/etc.
    def current_depth(self):
        return self.__class__.depth

    # Map generation.
    def generate_map(self):
        self.map = Encounter()
        self.map.level = self
        self.map.name = "MEAT ARENA"
        self.map.exits = self.exits
	self.map.generate_terrain(mapgen.MeatArena)

    # TODO: Hand this off to mapgen?
    def place_monsters(self):
        # Define NPCs to be placed
        from actors.npc import MeatSlave, MeatWorm, MeatGolem, MeatHydra
        monsters = [MeatSlave, MeatSlave, MeatSlave, MeatSlave, MeatWorm, MeatWorm, MeatGolem, MeatHydra] 

        # Place monsters
        num_mons = self.map.size / 2 + r3d6()
        for x in range(num_mons):
            monster = random.choice(monsters)
            monster = monster()
            self.map.put(monster, (self.map.center[0] + flip()*random.randint(1, self.map.size), self.map.center[1] + flip() * random.randint(1,self.map.size)))

    def generate_screens(self):
        screen = screens.text.get("meat-%s" % self.current_depth())
        if screen is not None:
            screen["header_right"] = self.name
            screen["footer_text"] = screens.footer
            self.screens.append(screen)
