"""A Level contains game state in a given scenario. This typically includes a
Map and an action queue."""

import random

from src.lib.data import screens
from src.lib.data.generators.items import generators
from src.lib.generators.items import ItemGenerator, generate_item
from src.lib.maps.encounter.map import EncounterMap

from src.lib.util.dice import *
from src.lib.util.hex import *
from src.lib.util.queue import Queue

from src.games.husk.generators.maps import outdoors, indoors
from src.games.husk.agents.actors import humans
from src.games.husk.agents.actors import crows

class Level(object):
    """A Level containing game state."""

    def __init__(self, game, **kwargs):
        self.game = game
        self.map_class = kwargs.pop("map_class", EncounterMap)

        self.name = kwargs.pop("name", "Smith Farm")
        self.map = self.generate_map(kwargs.pop("map_id", 1))

        self.queue = Queue

    def get_controller(self):
        """Return the Actor serving as primary controller in this Level."""
        return self.game.get_controller()

    """Level arrival methods."""

    def before_arrive(self, map_id, entrance_id, exit_id):
        """Do anything required before turning over control to this level's first Map."""
        if self.map:
            self.map.before_arrive(entrance_id, exit_id)

    def arrive(self, map_id, entrance_id, exit_id):
        """Turn over control to the first Map."""
        self.enter_map(map_id, entrance_id, exit_id)

    """Level loop methods."""

    def can_continue_gameplay(self):
        """Return whether the level portion of the game loop."""
        if not Queue.get_acting():
            return False
        for controlled in Queue.get_all_controlled():
            if controlled.alive:
                return True
        return False

    def loop(self):
        """Perform one iteration of the level portion of the game loop."""
        while True:
            actor = Queue.get_acting()
            if actor and not actor.controlled:
                if actor.before_turn():
                    actor.act()
            else:
                break

    """Level departure methods."""

    def before_depart(self, map_id, entrance_id, exit_id):
        """Do anything required before leaving this Level."""
        if self.map:
            self.map.before_depart(map_id, entrance_id, exit_id)

    def depart(self, map_id, entrance_id, exit_id):
        """Leave this Level."""
        if self.map:
            self.map.depart(map_id, entrance_id, exit_id)

    """Actor management methods."""

    def remove_actor(self, actor):
        """Remove an Actor from this Level."""
        if Queue.get_acting() == actor:
            Queue.next()
        Queue.remove(actor)

    """Map management methods."""

    def enter_map(self, map_id, entrance_id="prev", exit_id="next"):
        """Enter a Map, optionally including information about the trip."""
        Queue.clear()
        self.exit_map(map_id, entrance_id, exit_id)
        self.map = self.generate_map(map_id)
        player = self.get_controller()
        self.map.arriving_actor(player, entrance_id, exit_id)
        self.map.arrive(entrance_id, exit_id)
        player.trigger("arrived")
        Queue.addleft(player)
        self.game.view.map = self.map
        self.game.view.inherit()

    def exit_map(self, map_id=None, entrance_id=None, exit_id=None):
        """Exit a Map, optionally including information about the trip."""
        self.map.before_depart(map_id, entrance_id, exit_id)
        self.map.depart(map_id, entrance_id, exit_id)
        del self.map

    """Map factory methods."""

    def generate_map(self, map_id):
        """Generate and return a Map within this Level."""
        # Retrieve and instantiate the appropriate BaseMap subclass.
        map_obj = self.map_class(self, map_id)

        # Configure map settings, typically based on map_id.
        self.configure_map(map_obj)

        # Map layout.
        self.generate_map_layout(map_obj)

        # Terrain placement.
        self.generate_map_terrain(map_obj)

        # Monster placement.
        self.generate_map_monsters(map_obj)

        # Loot placement.
        self.generate_map_items(map_obj)

        return map_obj

    def configure_map(self, map_obj):
        """Configure a Map's setings based on provided travel information."""

        # Map properties that are the same for all map_ids.
        map_obj.center = (0,0)
        map_obj.size = 30

        if map_obj.map_id == 1:
            map_obj.name = "cornfield"
            map_obj.floor = (".", "yellow-black")
            map_obj.layout_generator = outdoors.Cornfield
            map_obj.passages = { "prev" : (map_obj.map_id-1, ANYWHERE), "next" : (map_obj.map_id+1, ANYWHERE) }
        elif map_obj.map_id == 2:
            map_obj.name = "farmhouse"
            map_obj.floor = (".", "green-black")
            map_obj.layout_generator = indoors.Farmhouse
            map_obj.passages = { "prev" : (map_obj.map_id-1, ANYWHERE), "next" : (map_obj.map_id+1, ANYWHERE) }

    def generate_map_layout(self, map_obj):
        """Generate a layout according to the Map configuration."""
        layout_generator = map_obj.layout_generator(map_obj)
        layout_generator.attempt()

        # TODO: Check for validity of the layout

        map_obj.layout = layout_generator

    def generate_map_terrain(self, map_obj):
        """Generate terrain according to the Map layout."""
        # TODO: Method to parse layout generator return values
        for pos, contents in map_obj.layout.cells.items():
            distance, terrain = contents # HACK: This won't always be a tuple like this.
            map_obj.add_cell(pos)

            if terrain:
                assert map_obj.put(terrain, pos, True) is not False

    def generate_map_monsters(self, map_obj):
        num_mons = 3
        loops = 1000
        while num_mons > 0 and loops > 0:
            loops -= 1
            cell = random.choice([cell for cell in map_obj.cells])
            monster_class = random.choice([humans.Human, crows.Crow])
            monster = monster_class()
            # monster.generate_equipment()
            if map_obj.put(monster, cell):
                Queue.add(monster)
                num_mons -= 1

    def generate_map_items(self, map_obj):
        item_count = 30 + r3d6() * map_obj.map_id
        generator = ItemGenerator(generators)
        loops = 1000
        while item_count > 0 and loops > 0:
            loops -= 1
            item = generator.random_item("implements")
            if item:
                random.choice(map_obj.cells.values()).put(item)
                item_count -= 1