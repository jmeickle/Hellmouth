from dice import *

# Helper class to make choices from a weighted list.
class Generator:
    def __init__(self, choices):
        self.choices = choices # See test code for an example of structure.
        self.weight = 100 # Default weight.

    # Pick from the weighted list(s).
    def choose(self, choice, choices=None):
        if choices is None:
            choices = self.choices

        choice_details = choices[choice]
        options = choice_details.get("options")
        if options is None:
            #exit("Choice: %s, choice_details: %s"%(choice, choice_details))
            return choice, choice_details

        sum = reduce(lambda x, y: x+y.get("weight", self.weight), options.values(), 0)
        weighting = random.randint(1, sum)

        for k, v in options.items():
            weighting -= v.get("weight", self.weight)
            if weighting <= 0:
                return self.choose(k, options)

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
