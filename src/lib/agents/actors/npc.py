# Derived from the Actor class, NPCs:
# 1) Do not check keyin
# 2) Have AI to control them
# 3) Do need any interface niceties (e.g., figuring out item letters)

import random

from src.lib.agents.actors.ai.astar import AStar
from src.lib.agents.actors.actor import Actor

from src.lib.util import debug
from src.lib.util.geometry.hexagon import Hexagon
from src.lib.util.queue import Queue

# TODO: Make a proper AI class.
class Pathing(object):
    def __init__(self, owner, target=None, astar=None, destination=None, distance=None, path=False, attempts=0):
        self.owner = owner
        self.target = target

        self.astar = astar
        self.destination = destination
        self.distance = distance
        self.path = path

        self.attempts = 0

    # Reset A* and generate a new path.
    def repath(self):
        debug.log("%s repathed." % self.owner.appearance())
        self.astar = AStar(self.owner, self.owner.map)
        self.path = self.astar.path(self.owner.coords, self.destination)

    def retarget(self):
        target = self.owner.call("Faction", "get_target").get_result()
        if target:
            self.target = target
            self.destination = self.target.coords
            debug.log("%s retargeted to %s." % (self.owner.appearance(), self.target.appearance()))
            return True

        destination = self.owner.call("Faction", "get_destination").get_result()
        if destination:
            self.destination = destination
            debug.log("%s found no target but instead a destination." % self.owner.appearance())
            return True

        # Move somewhere random.
        debug.log("%s failed to retarget." % self.owner.appearance())
        self.destination = random.choice([h for h in Hexagon.area(self.owner.coords, 10)])
        return True

class NPC(Actor):
    def __init__(self, components=[]):
        super(NPC, self).__init__(components)
        self.pathing = Pathing(self)

    def act(self):
        debug.log("%s started turn." % self.appearance())
        self._act()
        debug.log("%s ended turn." % self.appearance())
        self.end_turn()

    # AI actions. Currently: move in a random direction.
    def _act(self):
        if not self.turn():
            debug.die("%s tried to act when not the acting actor in queue %s." % (self, Queue))
        if self.controlled:
            debug.die("Player-controlled actor %s tried to hit AI code." % self.appearance())

        # If we don't have a target, try to find a new one.
        if not self.pathing.target and not self.pathing.retarget():
            # wander aimlessly
            return self.do(random.choice(dirs))

        # Repath if our current target isn't correct
        if self.pathing.target:
            if self.pathing.target.coords != self.pathing.destination:
                self.pathing.destination = self.pathing.target.coords
                if isinstance(self.pathing.destination, tuple):
                    debug.die([self, self.pathing.destination, self.pathing.target])
                self.pathing.repath()

            # Calculate the distance to the target.
            self.pathing.distance = self.distance(self.pathing.target)
        else:
            if isinstance(self.pathing.destination, tuple):
                debug.die([self, self.pathing.destination, self.pathing.target])
            self.pathing.repath()

        # TODO: If within attack range, do so.
        # if self.preferred_reach(self.distance) is True:
        #     return self.do(sub(self.target.coords, self.coords))

        # If we've successfully pathed, follow it.
        if self.pathing.path:
            debug.log("%s had a path." % self.appearance())
            next_step = self.pathing.path.pop()
            next_dir = next_step - self.coords
            # # HACK, fixes stuff like teleporting
            # if dir not in dirs:
            #     self.path.append(pos)
            #     dir = CC
            if self.map.cell(next_step).can_block(self, next_dir):
                # TODO: Randomize choice here
                for alt_dir in arc(next_dir)[1:]: # We already checked the first one
                    alt_next = self.coords + alt_dir
                    # Prefer unoccupied cells, but accept sharing.

                    if not self.map.cell(alt_pos).occupied():
                        next_dir = alt_dir
                        break
                    elif self.map.cell(alt_pos).blocked(alt_dir) is False:
                        next_dir = alt_dir

            self.do(next_dir)