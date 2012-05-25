from dice import *
from generators.maps import mapgen
from maps.encounter import Encounter

class MeatArena():
    def __init__(self):
        self.name = "A strange, meaty arena"
        self.exits = None
        self.map = None
        self.generate()

    def generate(self):
        self.map = Encounter()
        self.map.name = "MEAT ARENA"
        self.map.generate(mapgen.MeatArena)

        # Define NPCs to be placed
        from actors.npc import MeatSlave, MeatWorm, MeatGolem, MeatHydra
        monsters = [MeatSlave, MeatSlave, MeatSlave, MeatSlave, MeatWorm, MeatWorm, MeatGolem, MeatHydra] 

        # Place monsters
        num_mons = self.map.size / 2 + r3d6()
        for x in range(num_mons):
            monster = random.choice(monsters)
            monster = monster()
            self.map.put(monster, (self.map.center[0] + flip()*random.randint(1, self.map.size), self.map.center[1] + flip() * random.randint(1,self.map.size)))
