class Actor:
    def __init__(self, x, y, glyph='x'):
        self.glyph = glyph
        self.pos = [x, y]

        self.stats = {}
        self.traits = {}
        self.skills = {}
        self.inventory = {}
        self.bodyplan = BodyPlan(self, 'humanoid')

    def stat(stat):
        stats.get(stat)

    def move(self, dir):
        pos = (self.pos[0]+dir[0], self.pos[1]+dir[1])
        if pos[0] >= 0 and pos[0] < self.map.width:
            if pos[1] >= 0 and pos[1] < self.map.height:
                self.pos = pos

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
