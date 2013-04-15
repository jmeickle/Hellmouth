"""Terrain that enables modifying other Terrain when activated."""

from src.lib.agents.terrain.terrain import Terrain

class Lever(Terrain):
    """Base class for lever-like Passages."""
    def __init__(self, target):
        super(Lever, self).__init__()
        self.name = "lever"
        self.target = target
        self.glyph = "|"
        self.color = "magenta-black"
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