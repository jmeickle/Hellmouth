from define import *
from dice import _3d6, _d6, roll
from random import choice
from describe import d
import hex

class Actor:
    def __init__(self):
        # Descriptive information
        self.glyph = '@'
        self.color = 'magenta-black'
        self.name = 'Default monster'
        self.description = 'This is the description'

        # More 'permanent' game info: stats, skills, etc.
        self.body = Humanoid(self)
        self.stats = {"Strength" : 0,
                      "Dexterity" : 0,
                      "Intelligence" : 0,
                      "Health" : 0,
                     }
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

    # Do something in a dir - this could be an attack or a move.
    def do(self, dir):
        pos = (self.pos[0]+dir[0], self.pos[1]+dir[1])
        if self.map.valid(pos) is False:
            return False
        if self.map.cell(pos).occupied() is True:
            self.attack(self.map.actor(pos))
        else:
            self.move(pos)

    # Try to move based on an input direction. Return whether it worked.
    def move(self, pos):
        if self.valid_move(pos):
            self.go(pos)
            self.over()
            return True
        else:
            return False

    # Check move validity.
    def valid_move(self, pos):
        # Map border checking:
        if self.map.valid(pos) is False:
            return False

        # Cell content checking:
        if self.map.cell(pos).blocked() is True:
            return False

        return True

    # Currently: move in a random direction.
    def act(self):
        self.do(choice(dirs))

    def randomloc(self):
        roll = _3d6()
        loc = self.body.table.get(roll, None)
        if loc is None:
            subroll = _d6()
            loc = self.body.table[("%s-%s" % (roll, subroll))]
        return loc

    # Do a basic attack.
    def attack(self, target, loc=None):
        att_name = self.name
        def_name = target.name
        verb = "s"
        if self == self.map.player:
            att_name = "you"
            verb = ""
        if target == self.map.player:
            def_name = "you"

        if _3d6() > 8:
            str = "%s @dmg@%s %s" % (att_name, verb, def_name)

            # Mute non-nearby messages
            if str is not None and hex.dist(self.map.player.pos, target.pos) <= 3:
                self.map.log.add(d(str))

            amt = sum(roll(_d6, self.damage))
            target.hit(amt)

        self.over()

    # You were hit by something.
    def hit(self, amt):
        loc = self.randomloc()
        loc.hurt(amt)
        self.hp -= amt
        self.check_dead()

    def check_dead(self):
        if self.hp <= 0:
            if hex.dist(self.map.player.pos, self.pos) <= self.map.viewrange:
                self.map.log.add(d("%s has been slain!" % self.name))
            if self != self.map.acting:
                self.map.queue.remove(self)
            self.map.cell(self.pos).remove(self)

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

    # If it wasn't found in self.stats, it must need to be calculated.
    def calc_stat(self, stat):
        func = getattr(Actor, stat.replace(' ', ''))
        return func(self)

    # Calculated stats:
    # STUB: Insert formulas
    def HitPoints(self):       return 33
    def MaxHitPoints(self):       return 33
    def ManaPoints(self):       return 33
    def MaxManaPoints(self):       return 33
    def FatiguePoints(self):       return 33
    def MaxFatiguePoints(self):       return 33
    def Will(self):       return 33
    def Perception(self): return 33
    def Move(self):       return 33
    def Speed(self):      return 33
    def Dodge(self):      return 33
    def Block(self):      return 32
    def Parry(self):      return 31

    # Return how many points of wounds a location has
    def wound(self, loc, col=True):
        loc = self.body.locs.get(loc, None)
        if loc is None:
            return 0
        else:
            wounds = sum(loc.wounds)
            col = loc.color()
            if loc.status() == SEVERED:
                wounds = 'X'
            elif wounds >= 10:
                wounds = '*'
            if col is True:
                return "<%s-black>%s</>" % (col, wounds)
            else:
                return wounds

    def loccol(self, loc):
        loc = self.body.locs.get(loc, None)
        if loc is None:
            return "white-black"
        else:
            return "%s-black" % loc.color()

class BodyPlan:
    def __init__(self, parent):
        # Size (+0 for a human)
        self.size = None
        # Shape (tall, long, or full)
        self.shape = None
        # Body parts by key
        self.locs = {}
        # Body parts by 3d6 roll
        self.table = {}

    # Build a body from the class information.
    def build(self):
        for partname, parent, sublocation, rolls in self.parts:
            part = HitLoc(partname)
            self.locs[partname] = part
            if parent is not None:
                HitLoc.add_child(self.locs[parent], part)
            for roll in rolls:
                if isinstance(roll, list) is True:
                    base = roll[0]
                    for x in range(len(roll)):
                        if x == 0:
                            continue;
                        subroll = roll[x]
                        self.table["%s-%s" % (base, subroll)] = part
                else:
                    self.table[roll] = part

class Humanoid(BodyPlan):
    # These tuples represent:
    # 1: Part name.
    # 2: Parent part. Only list parts that have already been listed.
    # 3: True if it's a sublocation rather than a real one.
    # 4: List representing what 3d6 rolls hit that spot.
    #    If a further d6 roll is required, use a list like:
    #        [[16, 1, 2, 3], 14]
    parts = (
             ('Torso', None, False, [9, 10]),
             ('Groin', 'Torso', False, [11]),
             ('Neck', 'Torso', False, [17, 18]),
             ('Head', 'Neck', False, [3, 4, 5]),
             ('RArm', 'Torso', False, [8]),
             ('LArm', 'Torso', False, [12]),
             ('RHand', 'RArm', False, [15, 1, 2, 3]),
             ('LHand', 'LArm', False, [15, 4, 5, 6],),
             ('RLeg', 'Groin', False, [6, 7]),
             ('LLeg', 'Groin', False, [13, 14]),
             ('RFoot', 'RLeg', False, [[16, 1, 2, 3]]),
             ('LFoot', 'LLeg', False, [[16, 4, 5, 6]]),
    )

    def __init__(self, parent):
        BodyPlan.__init__(self, parent)
        self.build()

class Octopod(BodyPlan):
    # See Humanoid for a description.
    parts = (
             ('Mantle', None, None),
             ('Arm1', 'Mantle', None),
             ('Arm2', 'Mantle', None),
             ('Arm3', 'Mantle', None),
             ('Arm4', 'Mantle', None),
             ('Arm5', 'Mantle', None),
             ('Arm6', 'Mantle', None),
             ('Arm7', 'Mantle', None),
             ('Arm8', 'Mantle', None),
    )

    def __init__(self, parent):
        BodyPlan.__init__(self, parent)
        self.build()

class HitLoc:
    def __init__(self, type):
        self.type = type

        # Combat stats
        self.HP = 0
        self.DR = 0
        self.wounds = []

        # Connectivity
        self.parent = None
        self.children = []
        self.sublocations = []

        # Item-related
        self.worn = []
        self.held = []

    # Stub: return the healthiness of the limb
    def status(self):
        if sum(self.wounds) > 15:    return SEVERED
        elif sum(self.wounds) >= 10: return CRIPPLED
        elif sum(self.wounds) > 4:   return INJURED
        elif sum(self.wounds) > 1:   return SCRATCHED
        else:                        return UNHURT

    # Set up a parent/child relationship.
    def add_child(parent, child):
        parent.children.append(child)
        child.parent = parent

    # Add a sublocation of this part.
    def sublocation(self, part):
        self.sublocations.append(part)

    # Increase the wounds on the location.
    def hurt(self, amt):
        self.wounds.append(amt)

    # Return a color for the limb status.
    def color(self):
        if self.status() == SEVERED:     return "cyan"
        elif self.status() == CRIPPLED:  return "magenta"
        elif self.status() == INJURED:   return "red"
        elif self.status() == SCRATCHED: return "yellow"
        else:                            return "white"

# Test code
if __name__ == "__main__":
    testactor = Actor()
    print "Stats:", testactor.stats

    print "Random movement choice:", choice(dirs)

    print "Actor's parts:"
    for index, part in testactor.body.locs.iteritems():
        print "Part: %s - Children: %s - Parent:%s" % (part.type, part.children, part.parent)

    print "Connectivity test:"
    start = "RFoot"
    curr = testactor.body.locs.get(start)
    while curr.parent is not None:
        print "%s bone's connected to the %s bone..." % (curr.type, curr.parent.type)
        curr = curr.parent

    print "To-hit chart:"
    print "\n".join("%s - %s" % (x[0], x[1].type) for x in sorted(testactor.body.table.items()))

    #print "Connectivity test (Octo):"
    #testactor.body = Octopod(testactor)
    #start = "Arm1"
    #curr = testactor.body.locs.get(start)
    #while curr.parent is not None:
    #    print "%s bone's connected to the %s bone..." % (curr.type, curr.parent.type)
    #    curr = curr.parent

