from dice import *
from generators.maps import meat
from maps.encounter import Encounter
from data import screens
from hex import *

# TODO: Genericize this class.
class MeatArena():
    def __init__(self, player):
        # References.
        self.player = player
        self.map = None
        self.destination = None

        # DISPLAY:
        # Descriptive information about the level itself.
        self.name = "The Meat Arena"
        self.screens = []

        # Handle anything that should happen before arriving at this level is guaranteed.
        self.before_arrive()

    # The level portion of the game loop.
    def loop(self):
        if self.map is not None:
            # If the map has a destination, go to it.
            if self.map.loop() is False:
                self.go(self.map.destination)

        # Don't continue looping if we have a destination.
        if self.destination is not None:
            return False

        # Get screens from the map.
        self.screens = self.map.screens
        self.map.screens = []

    # Go to a specific map.
    def go(self, destination):
        # If this is called with False as a destination, there are no more maps.
        if destination is False:
            return self.before_leave(destination)

        # Otherwise, generate the map and trigger before_arrive() in it.
        self.generate_map(destination)
        self.map.before_arrive()

    # Functions called (before/when) (arriving at/leaving) the level.
    def before_arrive(self):
        self.arrive()

    def arrive(self):
        # When arriving at a level, go to its first map.
        self.go(1)

    def before_leave(self, destination):
        return self.leave(destination)

    def leave(self, destination):
        self.destination = destination

    # Generate a map. The destination parameter can be anything, but depth makes a
    # lot of sense. It's up to you to use it (or not).
    def generate_map(self, destination):
        # Create the map.
        self.map = Encounter(self)

        # Configure map settings, typically based on depth (destination).
        self.configure_map(destination)

        # Call the map's terrain generator.
	self.map.generate_terrain()

        # Monster placement.
        self.place_monsters()

    # Configure the map. (Here, we use destination as a depth parameter.)
    def configure_map(self, destination):
        self.map.depth = destination

        # Map properties that are the same for all depths.
        self.map.name = "Floor %s" % self.map.depth
        self.map.floor = (".", "white-black")
        self.map.layout = meat.MeatArena

        if self.map.depth == 1:
            self.map.exits = { "down" : (self.map.depth+1, ANYWHERE) }
        if self.map.depth == 2:
            self.map.exits = { "down" : (False, ANYWHERE) }

# TODO: Move these to other level classes.
#        if depth == 3:
#            self.map.name = "Grand Gate"
#            self.map.exits = { "down" : (MeatArena, (25, 0)) }
#            self.map.layout = meat.MeatTunnel
#        if depth == 4:
#            self.map.name = "Caves of Primal Meat"
#            self.map.exits = self.exits
#            self.map.layout = meat.MeatArena
#        if depth == 5:
#            self.map.name = "Sauce Vats"
#            self.map.exits = self.exits
#            self.map.layout = meat.MeatArena
#        if depth == 6:
#            self.map.name = "Tower of the Sauceror"
#            self.map.exits = None
#            self.map.layout = meat.MeatTower

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
