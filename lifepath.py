from lifepath_events import eventdata, skip
import random

# A lifepath is the sum of your choices during character generation. It is
# composed of lifepath events, forming a tree structure.

class Lifepath:
    def __init__(self):
        self.skip = skip
        self.first = skip
        self.events = []

    # Add the first event.
    def start(self, event):
        self.first = LifepathEvent(event)
        self.events.append(self.first)

    def display(self):
        self.first.display()

    def debug_display(self):
        self.first.debug_display(True)

    def effects(self):
        return self.first.sum_effects()

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
        self.text = self.data.get('text', '<DEBUG: NO LONG DESC>')
        self.short = self.data.get('short', None)

        # Actual gameplay effects.
        self.effects = self.data.get('effects', {})
        self.years = self.data.get('years', None)

    # Choose a child lifepath.
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
        if self.parent is not None:
            self.parent.child = None

    def display(self):
        print "Nothing right now."

    # Recursively returns lifepath effects.
    # TODO: Merge in a better way.
    def sum_effects(self):
        if self.child is not None:
            ret = self.child.sum_effects()
        else:
            ret = {}
        for k,v in self.effects.iteritems():
            if ret.get(k, None) is not None:
                ret[k] += v
            else:
                ret[k] = v
        return ret

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
    lifepath.first.choose('Mundane Infant')
    lifepath.first.child.choose('Mundane Young Child')
    lifepath.first.child.child.choose('Mundane Child')
    lifepath.first.child.child.child.choose('Mundane Teen')
    lifepath.first.child.child.child.child.choose('Mundane Young Adult')
    lifepath.debug_display()
    #print "===UNDO==="
    #lifepath.first.child.child.undo()
    #random = lifepath.first.child.pick()
    #lifepath.first.child.choose(random)
    #lifepath.debug_display()

if __name__ == "__main__":
    lifepath_test()
