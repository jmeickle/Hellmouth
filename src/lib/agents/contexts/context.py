"""Temporary objects that determine which responses are available to an event."""

class AgentContext(object):
    """A simple Context where one Agent responds to an event based on either
    one or more members or a source."""

    def __init__(self, agent, members, source):
        self.agent = agent
        self.members = members
        self.source = source

    def get_interactions(self):
        """Return the interactions made available to an Agent by the members of a Context."""
        for member in self.members:
            if member:
                for interaction in member.get_interactions(self.agent, self.source):
                    yield (member, interaction)