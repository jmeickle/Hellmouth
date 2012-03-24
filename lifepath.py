from lifepath_events import eventdata
import random

# A lifepath is the sum of your choices during character generation. It is
# composed of lifepath events, forming a tree structure.

class Lifepath:
    def __init__(self):
        self.initial = None
        self.start('Start')

    # Add the initial event.
    def start(self, event):
        self.initial = LifepathEvent(event)

    def display(self):
        self.initial.display()

    def debug_display(self):
        self.initial.debug_display(True)

class LifepathEvent:
    def __init__(self, choice, parent=None):
        # Grab the dict for the chosen event.
        self.data = eventdata.get(choice)

        # Tree structure: parent, child, and lifepath events.
        self.parent = parent
        if self.parent is not None:
            self.parent.child = self
        self.child = None

        self.choices = self.data.get('choices', (None, None, None))

        # Display information for the event.
        self.age = self.data.get('age', None)
        self.name = self.data.get('name', choice) # Defaults to the search key.
        self.text = self.data.get('text', 'DEBUG: no long desc.')
        self.short = self.data.get('short', 'DEBUG: no short desc.')

        # Actual gameplay effects.
        self.effects = self.data.get('effects', {'Bug':'99'})
        self.years = self.data.get('years', 99)

    def choose(self, event):
        self.child = LifepathEvent(event, self)

    # Randomly choose. Will cause an infinite crash if there are no further choices.
    def pick(self):
        choice = random.choice(self.choices)
        print "Random choice: %s" % choice
        if choice == '':
            choice = self.pick()
        return choice

    def undo(self):
        self.parent.child = None

    def display(self):
        print "Nothing right now."

    # Display variant for debug code.
    def debug_display(self, recurse=False):
        print ""
        print "==%s==" % self.name
        print ""
        print "  %s" % self.text
        print ""
        print "  GAMEPLAY EFFECTS:"
        for k, v in self.effects.iteritems():
            print "  %s: %+d" % (k, int(v))
        print ""
        print "  This event takes %d years." % self.years
        print ""
        print "  After this event, you can choose:"
        for choice in self.choices:
            print "  * %s" % choice
        print ""
        if self.parent is None and self.child is None:
            print "  This is the first, last, and therefore only event in your lifepath."
        elif self.parent is None:
            print "  This is the first event in your lifepath.",
        else:
            print "  This event is preceded by %s." % self.parent.short
            if self.child is None:
                print "  It is the last event in your lifepath."
            else:
                print "  It is followed by %s" % self.child.short

        if recurse is True and self.child is not None:
            print ""
            self.child.debug_display(True)

# Lifepath test code
def lifepath_test():
    lifepath = Lifepath()
    lifepath.start(LifepathEvent('Start'))
    lifepath.initial.choose('Mundane Infant')
    lifepath.initial.child.choose('Mundane Young Child')
    lifepath.initial.child.child.choose('Mundane Child')
    lifepath.initial.child.child.child.choose('Mundane Teen')
    lifepath.initial.child.child.child.child.choose('Mundane Young Adult')
    lifepath.debug_display()
    #print "===UNDO==="
    #lifepath.initial.child.child.undo()
    #random = lifepath.initial.child.pick()
    #lifepath.initial.child.choose(random)
    #lifepath.debug_display()

if __name__ == "__main__":
    lifepath_test()
