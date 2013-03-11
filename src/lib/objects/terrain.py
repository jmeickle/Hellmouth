# Terrain objects.

from src.lib.agents.agent import Agent
from src.lib.util.command import CommandRegistry as CMD
from src.lib.util.log import Log

class Terrain(Agent):
    def __init__(self, terrain_type=None):
        super(Terrain, self).__init__()
        self.cell = None
        self.name = None
        self.color = None
        self.glyph = None
        self.blocking = True
        self.terrain_type = terrain_type

    # Do additional setup based on the provided terrain type.
    def setup(self):
        return False

    # What the terrain does when an actor interacts with it.
    def interact(self, actor):
        return False

# Generic staircase class.
class Stairs(Terrain):
    def __init__(self, which, destination):
        super(Stairs, self).__init__()
        self.name = "staircase " + which
        self.destination = destination
        self.glyph = ">"
        self.color = "green-black"
        self.blocking = False

    def react_on_do_use(self, user):
        self.cell.map.go(self.destination)
        return True

# Generic lever class.
class Lever(Terrain):
    def __init__(self, target):
        super(Lever, self).__init__()
        self.name = "lever"
        self.target = target
        self.glyph = "|"
        self.color = "magenta-black"
        self.blocking = False
        self.enabled = False

    def provide_commands(self, context):
        """Yield the interaction commands an Agent provides to another Agent
        within a Context.
        """
        if "Manipulation" in context.domains:
            if not self.enabled:
                yield CMD("UseTerrain", target=self, use="enable")
            else:
                yield CMD("UseTerrain", target=self, use="disable")

    def react_on_do_use(self, agent, use):
        """React to being used."""
        if use == "enable" and self.enabled or use == 'disable' and not self.enabled:
            Log.add("The lever won't budge.")
            return True
        else:
            Log.add("<magenta-black>-CLICK!-</> %s %ss the lever." % (agent.appearance(), use))
            if use == "enable" and not self.enabled:
                self.color = "black-magenta"
                self.enabled = True
            elif use == "disable" and self.enabled:
                self.color = "magenta-black"
                self.enabled = False
            return True
        return False

# Meat Arena
class MeatWall(Terrain):
    def __init__(self, terrain_type=None):
        super(MeatWall, self).__init__()
        self.name = "meat wall"
        self.glyph = "X"
        self.color = "red-black"
        self.setup(terrain_type)

    def setup(self, terrain_type):
        if terrain_type == 'inner':
            self.color = "yellow-black"
            self.name = "inner " + self.name

# Caves
class CaveWall(Terrain):
    def __init__(self, terrain_type=None):
        super(CaveWall, self).__init__()
        self.name = "rough-hewn cave wall"
        self.glyph = "#"
        self.color = "yellow-black"