import random

# Basic d6 roll
def _d6():
    return random.randint(1, 6)

# Basic 3d6 roll
def _3d6():
    return sum(roll(_d6, 3))

# Return n rolls of either d6 or 3d6, with per-roll modifiers
def roll(func, n, per=0):
    return [func() + per for x in range(n)]

# Test function
if __name__ == '__main__':
    print "Ten 1d6 rolls:", roll(_d6, 10)
    print "Ten 3d6 rolls:", roll(_3d6, 10)
