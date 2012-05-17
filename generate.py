# Generate (or improve) an actor's points.
import random

def spend_points(actor, points=None):
    # If we didn't feed in a number of points, we're using the actor's starting points.
    if points is None:
        points = actor.points
    spent = {}
    while points > 0:
        points -= 1

#Tasks:
# 1) Improve existing skills

# Helper class to make choices from a weighted list.
class Generator:
    def __init__(self, choices={}):
        self.choices = choices # See test code for an example of structure.
        self.default = 100 # Default weight.

    # Pick from the weighted list(s).
    def choose(self, current=None):
        if current is None:
            current = self.choices
        choice = None
        sum = reduce(lambda x, y: x+y.get("weight", self.default), current.values(), 0)
        weighting = random.randint(1, sum)

        for k, v in current.items():
            weighting -= v.get("weight", self.default)
            if weighting <= 0:
                options = v.get("options")
                if options is None:
                    return k
                else:
                    return self.choose(options)

# Test code.
if __name__ == "__main__":
    print "Random actor generation test:"
    generator = Generator()

    # Weight defaults to 100, as set above.
    generator.choices = {
        "melee" : {
            "options" : {
                "Melee/Shortsword" : {},
                "Melee/Broadsword" : {},
                "Melee/Axe" : {},
            },
        },
        "magic" : {
            "weight" : 10,
            "options" : {
                "Fire Magic" : {},
                "Ice Magic" : {},
                "Necromancy" : {"weight" : 10},
            },
        },
    }

    picks = 10
    choices = []
    for x in range(picks):
        choices.append(generator.choose())

    print "==CHOICES=="
    for choice in choices:
        print "- %s" % choice
