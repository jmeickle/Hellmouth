from define import *
from random import choice

class Actor:
    def __init__(self):
        # Descriptive information
        self.glyph = 'x'
        self.color = 'red'
        self.name = 'Buggy monster'
        self.description = 'This is the description'

        # More 'permanent' game info: stats, skills, etc.
        self.body = BodyPlan(self, 'humanoid')
        self.stats = {"Strength" : 0,
                      "Dexterity" : 0,
                      "Intelligence" : 0,
                      "Health" : 0,
                      "" : 0,
                      "" : 0,
                      "" : 0,
                      "" : 0,
                      "" : 0}
        self.traits = {}
        self.skills = {}

        # More 'volatile' information: inventory, effects, etc.
        self.map = None
        self.pos = None
        self.inventory = {}
        self.effects = {}

    # Change actor coords and update the relevant cells.
    def go(self, pos):
        self.map.cells[self.pos[0]][self.pos[1]].remove(self)
        self.pos = pos
        self.map.cells[self.pos[0]][self.pos[1]].add(self)

    # Try to move based on an input direction. Return whether it worked.
    def move(self, dir):
        pos = (self.pos[0]+dir[0], self.pos[1]+dir[1])
        if self.valid_move(pos):
            self.go(pos)
            self.over()
            return True
        else:
            return False

    # Check move validity.
    def valid_move(self, pos):
        # Map border checking:
        if pos[0] < 0 or pos[0] >= self.map.width \
        or pos[1] < 0 or pos[1] >= self.map.height:
            return False

        # Cell content checking:
        if self.map.cells[pos[0]][pos[1]].blocked() is True:
            return False

        return True

    # Currently: move in a random direction.
    def act(self):
        self.move(choice(dirs))

    # Mark self as done acting.
    def over(self):
        self.map.acting = None
        self.map.queue.append(self)

    # Retrieve actor stat.
    def stat(self, stat):
        val = self.stats.get(stat)
        if val is None:
            return self.calc_stat(stat)
        else:
            return val
#self.calc_stat(stat))

    # If it wasn't found in self.stats, it must need to be calculated.
    def calc_stat(self, stat):
        func = getattr(Actor, stat)
        return func(self)

    # Calculated stats:
    def Will(self):       return 33
    def Perception(self): return 33
    def Move(self):       return 33
    def Speed(self):      return 33
    def Dodge(self):      return 33
    def Block(self):      return 32
    def Parry(self):      return 31

class BodyPlan:
    def __init__(self, parent, type):
        self.hitlocs = {}

class Humanoid(BodyPlan):
    def __init__(self, parent, type):
        BodyPlan.__init__(self, parent, type)

        self.hitlocs["RArm"] = HitLoc(self, "RArm")

class HitLoc:
    def __init__(self, parent, type):
        self.name = None
        self.HP = None

if __name__ == "__main__":
    testactor = Actor()
    testactor.stats["ST"] = 5
    print testactor.stats
    print "Random movement:",
    print choice(dirs)
