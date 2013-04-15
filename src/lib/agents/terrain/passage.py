"""Terrain that enables moving from one Map to another."""

from src.lib.agents.terrain.terrain import Terrain

from src.lib.util.command import CommandRegistry as CMD

class Passage(Terrain):
    """Base class for Passages, which enable movement from one Map to another."""
    def __init__(self, passage_id, map_id):
        super(Passage, self).__init__()
        self.passage_id = passage_id
        self.map_id = map_id

        self.name = "passage to the " + passage_id
        self.glyph = ">"
        self.color = "green-black"

    def provide_commands(self, context):
        """Yield the interaction commands an Agent provides to another Agent
        within a Context.
        """
        yield CMD("UsePassage", target=self, use="passage")

    def react_on_do_use(self, agent, use):
        if use == 'passage':
            agent.map.level.enter_map(self.map_id)
        return True

class Path(Passage):
    """Base class for road-like Passages."""
    def __init__(self, passage_id, map_id):
        super(Path, self).__init__(passage_id, map_id)
        self.name = "path to the " + passage_id

class Stairs(Passage):
    """Base class for stair-like Passages."""
    def __init__(self, passage_id, map_id):
        super(Stairs, self).__init__(passage_id, map_id)
        self.name = "stairs to the " + passage_id