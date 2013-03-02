"""Defines the Components and Traits that provide status effect functionality to Agents."""

from src.lib.agents.components.component import Component
from src.lib.util.result import accumulate_results, ignore_results, single_results

class Status(Component):
    """Defines the ability to be afflicted by status effects."""

    def __init__(self, owner):
        self.statuses = {}
        self.owner = owner

    def before_turn(self):
        """Respond to the Agent's turn starting."""
        if self.statuses.get("Retreat") is not None:
            del self.statuses["Retreat"]

        if self.statuses.get("Unconscious") is False and self.owner.HP() < 0:
            check, margin = self.owner.sc('HT', self.owner.MaxHP() / self.owner.HP())
            if check < TIE:
                # TODO: Improve messaging
                #Log.add("%s passes out." % self.appearance())
                self.owner.knockout()

    def after_turn(self):
        """Respond to the Agent's turn ending."""

        # Shock ends at the end of your turn.
        # TODO: Handle the case of getting shock in your own turn.
        if self.statuses.get("Shock") is not None:
            del self.statuses["Shock"]

        for effect, details in self.effects.items():
            if effect == "Stun":
                # TODO: Mental Stun
                check, margin = self.sc('HT')
                if check > TIE:
                    del self.effects["Stun"]
                    # TODO: Real message.
                    if self.get("Status", "unconscious") is True:
                        Log.add("%s shrugs off the stun." % self.appearance())

    @single_results
    def get(self, method, *args):
        return self.get_status(method, *args)

    def get_status(self, status_name, default=None):
        """Return the status in question."""
        status = self.statuses.get(status_name)
        if status:
            return status
        else:
            return default

    def update(self):
#        if change in ('HP', 'MaxHP'):
#            self.
        pass

    def set_status(self, status_name, value=None):
        """Sets the value of a status. If no value is provided, """
        # if self.get_status(status_name) != value:
        #     return False
        # else:
        #     return True        
        pass

    def has(self, status_name, value=None, results=None):
        """Returns whether a status exists within this Component (optionally, only statuses matching a value.)"""
        if self.get_status(status_name) != value:
            return False
        else:
            return True

    @accumulate_results
    def get_view_data(self, view):
        """Retrieve the raw data for a View."""
        shock = self.statuses.get("Shock", 0)
        if shock > 0:
            if shock == 4:
                color = "magenta-black"
            elif shock == 3:
                color = "red-black"
            elif shock == 2:
                color = "yellow-black"
            else:
                color = "cyan-black"
            yield ("Shock", color)
        if self.statuses.get("Stun"):
            yield ("Stun", "red-black")
        if self.statuses.get("Unconscious"):
            yield ("KO'd", "red-black")
        if self.statuses.get("Reeling"):
            yield ("Reeling", "red-black")
        if self.statuses.get("Exhausted"):
            yield ("Exh", "yellow-black")

    def count(self):
        """How many status effects the agent has."""
        return len(self.statuses)

    def get_unconscious(self):
        """Whether the Agent currently has the Unconscious status effect."""
        if self.statuses.get("Unconscious") is not None:
            return False
        return True

    def set_unconscious(self, value):
        """Set the Agent's Unconscious status effect to a value."""
        self.statuses["Unconscious"] = value
        return True

    # Whether you're so injured as to be reeling.
    def is_reeling(self):
        if self.owner.HP() < self.owner.MaxHP()/3:
            return True
        else:
            return False

    # Whether you're so fatigued as to be exhausted.
    def is_exhausted(self):
        if self.owner.FP() < self.owner.MaxFP()/3:
            return True
        else:
            return False