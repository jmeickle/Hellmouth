# Generate (or improve) an actor's points.

import random

from define import *
from dice import *
from generators import *

def spend_points(actor, points=None):
    # If we didn't feed in a number of points, we're using the actor's
    # starting points. The alternative is that we're improving the actor.
    if actor.generator is not None:
        generator = Generator(generators[actor.generator])
    else:
        generator = Generator()

    if points is None:
        points = actor.points["total"]

    # Dict of expenditures thus far
    spent = {}
    for x in point_types:
        spent[x] = {}

    # Number of tries, to avoid infinite loops
    tries = 0
    allowed = 50

    while points > 0 and tries < allowed:
        tries += 1
        type = random.choice(point_types)
        choice, cost = generator.choose(type)
        if choice is None:
            continue
        if cost <= points:
            # TODO: continue out here, based on logic of skill appropriateness.
            if spent[type].get(choice) is None:
                spent[type][choice] = cost
            else:
                spent[type][choice] += cost
            points -= cost

    # Save any unspent points.
    spent["unspent"] = points
    return spent

# Helper class to make choices from a weighted list.
class Generator:
    def __init__(self, choices=generators["default"]):
        self.choices = choices # See test code for an example of structure.
        self.amount = r1d6 # Default points per choice made.
        self.weight = 100 # Default weight.

    # Pick from the weighted list(s).
    def choose(self, type, current=None):
        if current is None:
            current = self.choices.get(type)
            if current is None:
                return (None, 0)

        choice = None
        sum = reduce(lambda x, y: x+y.get("weight", self.weight), current.values(), 0)
        weighting = random.randint(1, sum)

        for k, v in current.items():
            weighting -= v.get("weight", self.weight)
            if weighting <= 0:
                options = v.get("options")
                if options is None:
                    return k, v.get("amount", self.amount())
                else:
                    return self.choose(type, options)

# Test code.
if __name__ == "__main__":
    print "Random choice test:"

    generator = Generator()
    #generator.choices = default_generator

    picks = 10
    choices = []
    for x in range(picks):
        choices.append(generator.choose("skills"))

    print "==CHOICES=="
    for choice in choices:
        print "- %s (%s points)" % choice

    print ""

    print "Random actor generation test:"

    # Import necessary classes.
    from actor import Actor

    # Generate a dummy actor
    actor = Actor()
    actor.points["total"] = 50+r3d6()

    # Spend points!
    spent = spend_points(actor, generator)

    # Store spending:
    actor.points["skills"] = spent

    for choice, points in actor.points["skills"].items():
        print "%s - %s points" % (choice, points)
    print "-"*20
    print "SUM: %s" % sum(actor.points["skills"].values())

    print ""

    print "Random actor improvement test:"

    runs = 3
    for run in range(runs):
        print ""

        # Choose number of points.
        points = r1d6()+10+actor.points["skills"].pop("unspent", 0)

        print "Improved actor by %s points." % points
        print ""

        # Spend points!
        spent = spend_points(actor, generator, points)

        # Merge in prior spending:
        for k,v in spent.items():
            if actor.points["skills"].get(k) is None:
                actor.points["skills"][k] = v
            else:
                actor.points["skills"][k] += v

        for choice, points in actor.points["skills"].items():
            print "%s - %s points" % (choice, points)
        print "-"*20
        print "SUM: %s" % sum(actor.points["skills"].values())