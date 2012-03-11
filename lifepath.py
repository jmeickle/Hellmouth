from lifepath_events import eventdata
# A lifepath is the sum of your choices during character generation. It is
# composed of lifepath events, forming a tree structure.

class Lifepath:
    def __init__(self):
        self.initial = None

    # Add the initial event.
    def start(self, event):
        self.initial = event

    def display(self):
        self.initial.display(True)

class LifepathEvent:
    def __init__(self, choice, parent=None):
        # Grab the dict for the chosen event.
        self.data = eventdata.get(choice)

        # Tree structure: parent, child, and lifepath events.
        self.parent = parent
        if self.parent is not None:
            self.parent.child = self
        self.child = None
        self.events = self.data.get('choices', None)

        # Display information for the event.
        self.name = self.data.get('name', choice) # Defaults to the search key.
        self.text = self.data.get('text', 'Missing description.')

        # Actual gameplay effects.
        self.effects = self.data.get('effects', 'No gameplay effects.')
        self.years = self.data.get('years', 99)

    def choose(self, event):
        self.child = LifepathEvent(event, self)

    def display(self, recurse=False):
        print self.name
        print self.text
        print self.effects
        print "Parent: %s, Child: %s" % (self.parent, self.child)
        if recurse is True and self.child is not None:
            self.child.display(True)

def lifepath_test():
    lifepath = Lifepath()
    lifepath.start(LifepathEvent('Warriors'))
    lifepath.initial.choose('Wizards')
    lifepath.display()

if __name__ == "__main__":
    lifepath_test()
