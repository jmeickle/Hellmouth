# Derived from the Actor class, NPCs:
# 1) Do not check keyin
# 2) Have AI to control them
# 3) Do need any interface niceties (e.g., figuring out item letters)

from src.lib.agents.actors.ai.astar import AStar
from src.lib.agents.actors.actor import Actor

from src.lib.util.debug import debug
from src.lib.util.hex import *
from src.lib.util.queue import Queue

class NPC(Actor):

    def __init__(self, components=[]):
        super(NPC, self).__init__(components)

        # TODO: Make an AI class.

        # AI-related properties.
        self.target = None

        self.astar = None
        self.destination = None
        self.distance = None
        self.path = False

        self.attempts = 0

    def act(self):
        debug("%s started turn." % self.appearance())
        self._act()
        debug("%s ended turn." % self.appearance())
        self.end_turn()

    # AI actions. Currently: move in a random direction.
    def _act(self):
        if not self.turn():
            die("%s tried to act when not the acting actor %s." % (self.appearance(), Queue.get_acting()))
        if self.controlled:
            die("Player-controlled actor %s tried to hit AI code." % self.appearance())

        # If we don't have a target, try to find a new one.
        if not self.target:
            if not self.retarget():
                return

        # Repath if our current target isn't correct
        if self.target.pos != self.destination:
            self.destination = self.target.pos
            self.repath()

        # Calculate the distance to the target.
        self.distance = dist(self.pos, self.target.pos)

        # TODO: If within attack range, do so.
        # if self.preferred_reach(self.distance) is True:
        #     return self.do(sub(self.target.pos, self.pos))

        # If we've successfully pathed, follow it.
        if self.path:
            debug("%s had a path." % self.appearance())
            next_step = self.path.pop()
            next_dir = sub(next_step, self.pos)
            # # HACK, fixes stuff like teleporting
            # if dir not in dirs:
            #     self.path.append(pos)
            #     dir = CC
            if self.map.cell(next_step).blocked(next_dir):
                # TODO: Randomize choice here
                for alt_dir in arc(next_dir)[1:]: # We already checked the first one
                    alt_next = add(self.pos, alt_dir)
                    # Prefer unoccupied cells, but accept sharing.

                    if not self.map.cell(alt_pos).occupied():
                        next_dir = alt_dir
                        break
                    elif self.map.cell(alt_pos).blocked(alt_dir) is False:
                        next_dir = alt_dir

            self.do(next_dir)

    # Reset A* and generate a new path.
    def repath(self):
        debug("%s repathed." % self.appearance())
        self.astar = AStar(self.map)
        self.path = self.astar.path(self.pos, self.destination)

    def retarget(self):
        debug("%s retargeted." % self.appearance())
        if self.map.player:
            self.target = self.map.player
            self.destination = self.target.pos
            return True
        debug("%s failed to retarget." % self.appearance())
        return False