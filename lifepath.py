# A lifepath is the sum of your choices during character generation. It is
# composed of lifepath events, forming a tree structure.

class Lifepath:
    def __init__(self):
        self.initial = None
        self.events = []

    # Add the initial event.
    def start(self, event):
        self.initial = event
        self.events.append(event)

    def display(self):
        for event in self.events:
            event.display()

class LifepathEvent:
    def __init__(self, choice, parent=None):
        choices = {
        'Wizards' : {
            'name': "Hello",
            'text' : "Your parents were mighty wizards.",},
        'Warriors' : {
            'text' : "Your parents were fearsome warriors.",},
        }
        self.choice = choices.get(choice)

        # Tree structure: parent, choice, and options.
        self.parent = parent
        self.child = None
        self.options = None

        # Display information for the event.
        self.name = self.choice.get('name', choice) # Defaults to the search key.
        self.text = self.choice.get('text', 'Missing description.')

        # Actual gameplay effects.
        self.effects = self.choice.get('effects', 'No gameplay effects.')

    def choose(self, event):
        self.child = LifepathEvent(self)

    def display(self):
        print self.name
        print self.text
        print self.effects

def lifepath_test():
    lifepath = Lifepath()
    lifepath.start(LifepathEvent('Warriors'))
    lifepath.display()

if __name__ == "__main__":
    lifepath_test()

