"""Temporary objects that determine which responses are available to an event."""

from src.lib.util.result import Result

class Context(object):
    entry_ids = 0
    """The number of context IDs issued so far."""

    def __init__(self, agent, domains=[], participants=[], intent={}, component=None):
        self.agent = agent
        """The Agent that owns this Context."""
        self.domains = domains
        """The Domains that this Context focuses on."""
        self.participants = participants
        """The other Agents involved in this Context."""
        self.intent = intent
        """The intent of the Agent towards the participants in this Context."""
        self.component = component
        """The Component that has control over this Context."""
        self.data = {}
        """Data storage for this Context, mostly used when processing Commands."""
        self.arguments = {}
        """Arguments for this context."""

    """Context participant getter methods."""

    def is_participant(self, agent):
        """Return whether an agent is a participant in a Context."""
        return agent in self.participants

    def get_participants(self):
        """Yield the participants in a Context."""
        for participant in self.participants:
            yield participant

    """Context participant setter methods."""

    def set_participant(self, participant):
        """Set this Context to have a single participant."""
        self.participants = [participant]

    def add_participant(self, participant):
        """Add a participant to a Context."""
        self.participants.append(participant)

    def add_participants(self, participants):
        """Add several participants to a Context."""
        self.participants.extend(participants)

    def remove_participant(self, participant):
        """Remove a participant from a Context."""
        self.participants.remove(participant)

    """Context intent getter methods."""

    def get_intent(self):
        """Return the intent of the Agent towards this Context."""
        return self.intent

    """Context intent setter methods."""

    def update_intent(self, **kwargs):
        """Update the intent of the Agent towards this Context."""
        self.intent.update(kwargs)

    """Context data retrieval methods."""

    def get_data(self, entry_id):
        """Return an entry in this Context's data."""
        return self.data.get(entry_id, {})

    def get(self, entry_id, key, default=None):
        """Return a value from an entry in this Context's data."""
        return self.get_data(entry_id).get(key, default)

    def multiget(self, entry_id, keys, default=None):
        """Yield (key, value) tuples from an entry in this Context's data."""
        data = self.get_data(entry_id)
        for key in keys:
            yield key, data.get(key, default)

    """Context data update methods."""

    def append(self, entry_id, **kwargs):
        """Append the value of (key, value) tuples to the value of existing keys from an entry in this Context's data."""
        entry_data = self.get_data(entry_id)
        for key, value in kwargs.items():
            values = entry_data.get(key, [])
            values.append(value)
            entry_data[key] = values
        self.data[entry_id] = entry_data

    def update(self, entry_id, **kwargs):
        """Update an entry in this Context's data."""
        entry_data = self.get_data(entry_id)
        entry_data.update(kwargs)
        self.data[entry_id] = entry_data

    """Context Command getter methods."""

    def get_agent_commands(self):
        """Yield the Commands the Agent makes available to itself."""
        return self.agent.get_commands(self)

    def get_participant_commands(self, participant):
        """Yield the Commands a single participant makes available to the Agent."""
        for command in participant.provide_commands(self):
            yield command

    def get_participants_commands(self):
        """Yield the Commands that each participant makes available to the Agent."""
        for participant in self.participants:
            for command in self.get_participant_commands(participant):
                yield command

    def get_commands(self):
        """Yield all Commands made available to an Agent by this Context."""
        for command in self.get_agent_commands():
            yield command

        for command in self.get_participants_commands():
            yield command

    """Context result getter methods."""

    # TODO: Rewrite
    def get_results(self, entry_id, key):
        """Helper function to yield (processed object/method, result) tuples from a key within this Context's data."""
        callers, results = [v for k, v in self.multiget(entry_id, [key, key + "_results"], [None])]

        # This can happen due to the generator stuff :(
        # if len(callers) != len(results):
        #     exit("%s, %s" % (callers, results))

        import itertools
        try:
            for caller, result in itertools.izip(callers, results):
                yield caller, result
        except TypeError:
            exit("%s" % results)

    """Context result setter methods."""

    def add_result(self, entry_id, key, result):
        """Helper function to append a result to a key within this Context's data."""
        self.append(entry_id, **{key + "_results" : result})

    """Context result helper methods."""

    # TODO: Move elsewhere
    def parse_result(self, result):
        """Take any type of result and convert it to an outcome bool and a cause tag."""
        if isinstance(result, Result):
            return result.get_outcome(), result.get_cause()
        else:
            try:
                return result[0], result[1:]
            except TypeError:
                return result, "unknown"

    # TODO: Move elsewhere
    def parse_results(self, entry_id, key):
        for caller, result in self.get_results(entry_id, key):
            outcome, cause = self.parse_result(result)
            if outcome is False:
                return outcome, cause
        return True, "ok"

    """Misc. helper methods."""

    def get_id(self):
        """Return an ID global across Contexts."""
        Context.entry_ids += 1
        return Context.entry_ids

