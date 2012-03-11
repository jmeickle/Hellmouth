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
        self.text = self.data.get('text', 'Missing long description.')
        self.short = self.data.get('short', 'Missing short description.')

        # Actual gameplay effects.
        self.effects = self.data.get('effects', {'Bug':'99'})
        self.years = self.data.get('years', 99)

    def choose(self, event):
        self.child = LifepathEvent(event, self)

    def undo(self):
        self.parent.child = None

    def display(self, recurse=False):
        print "==%s==" % self.name
        print "  %s\n" % self.text
        print "  GAMEPLAY EFFECTS:"
        for k, v in self.effects.iteritems():
            print "  %s: %+d" % (k, int(v))
        print ""
        print "  This event takes %d years." % self.years
        print ""
        if self.parent is None and self.child is None:
            print "  This is the first, last, and therefore only event in your lifepath."
        elif self.parent is None:
            print "  This is the first event in your lifepath.",
        else:
            print "  This event is preceded by %s." % self.parent.short,
            if self.child is None:
                print "It is the last event in your lifepath."
            else:
                print "It is followed by %s" % self.child.short

        if recurse is True and self.child is not None:
            print ""
            self.child.display(True)

def lifepath_test():
    lifepath = Lifepath()
    lifepath.start(LifepathEvent('Warriors'))
    lifepath.initial.choose('Wizards')
    lifepath.initial.child.choose('Hugs')
    lifepath.display()
    lifepath.initial.child.child.undo()
    lifepath.initial.child.choose('Drugs')
    lifepath.display()

if __name__ == "__main__":
    lifepath_test()
