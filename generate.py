# Generate (or improve) an actor's points.
import random
from dice import _3d6, _d6, roll

def spend_points(actor, generator, points=None):
    # If we didn't feed in a number of points, we're using the actor's
    # starting points. The alternative is that we're improving the actor.
    if points is None:
        points = actor.points["total"]

    # Dict of expenditures thus far
    spent = {}

    # Number of tries, to avoid infinite loops
    tries = 0
    allowed = 50

    while points > 0 and tries < allowed:
        tries += 1
        choice, cost = generator.choose()
        if cost <= points:
            # TODO: continue out here, based on logic of skill appropriateness.
            if spent.get(choice) is None:
                spent[choice] = cost
            else:
                spent[choice] += cost
            points -= cost

    # Save any unspent points.
    spent["unspent"] = points
    return spent

#Tasks:
# 1) Improve existing skills

# Helper class to make choices from a weighted list.
class Generator:
    def __init__(self, choices={}):
        self.choices = choices # See test code for an example of structure.
        self.amount = _d6 # Default points per choice made.
        self.weight = 100 # Default weight.

    # Pick from the weighted list(s).
    def choose(self, current=None):
        if current is None:
            current = self.choices
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
                    return self.choose(options)

# Test code.
if __name__ == "__main__":
    print "Random choice test:"
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
        print "- %s (%s points)" % choice

    print ""

    print "Random actor generation test:"

    # Import necessary classes.
    from actor import Actor

    # Generate a dummy actor
    actor = Actor()
    actor.points["total"] = 103

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
        points = _d6()+10+actor.points["skills"].pop("unspent", 0)

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
