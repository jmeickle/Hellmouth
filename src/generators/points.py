# Generate (or improve) an actor's points.

import random

from define import *
from dice import *
from data.generators.points import generators
from generators.generator import Generator

def spend_points(actor, points=None):
    # If we didn't feed in a number of points, we're using the actor's
    # starting points. The alternative is that we're improving the actor.
    if actor.generator is not None:
        generator = Generator(generators[actor.generator])
#    else:
#        generator = Generator()

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
        if generator.choices.get(type) is None:
            continue
        choice, choice_details = generator.choose(type, generator.choices)
        cost = r1d6() * choice_details.get("multiplier", 1)
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
