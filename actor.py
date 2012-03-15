class Actor:
    def __init__(self):
        # Descriptive information
        self.glyph = 'x'
        self.color = 'red'
        self.name = 'Buggy monster'
        self.description = 'This is the description'

        # More 'permanent' game info: stats, skills, etc.
        self.body = BodyPlan(self, 'humanoid')
        self.stats = {}
        self.traits = {}
        self.skills = {}

        # More 'volatile' information: inventory, effects, etc.
        self.map = None
        self.pos = None
        self.inventory = {}
        self.effects = {}

    # Change actor coords.
    def go(self, pos):
        self.pos = pos

    # Try to move and return whether it worked.
    def move(self, dir):
        pos = (self.pos[0]+dir[0], self.pos[1]+dir[1])
        if self.valid_move(pos):
            self.go(pos)
            return True
        else:
            return False

    # Check move validity.
    def valid_move(self, pos):
        if pos[0] >= 0 and pos[0] < self.map.width:
            if pos[1] >= 0 and pos[1] < self.map.height:
                return True

    # Retrieve actor stats.
    def stat(stat):
        stats.get(stat)

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
    testactor = Actor(5, 5)
    testactor.stats["ST"] = 5
    print testactor.stats
