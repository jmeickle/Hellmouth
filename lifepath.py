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
            print event

class LifepathEvent:
    def __init__(self, parent=None):
        # Tree structure: parent, choice, and options.
        self.parent = parent
        self.child = None
        self.options = None

        # Actual effects of the event.
        self.name = "Debug event."
        self.text = "Debug text."
        self.effects = {'Combat Reflexes' : 1}


    def choose(self, event):
        self.child = LifepathEvent(self)

    def display(self):
        print self.name
        print self.text
        print self.effects

def lifepath_test():
    lifepath = Lifepath()
    lifepath.start(LifepathEvent())
    lifepath.initial.display()
    lifepath.display()

if __name__ == "__main__":
    lifepath_test()
