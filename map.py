import random
from random import randint

class Map:
    def __init__(self):
        self.cells = None
        self.height = None
        self.width = None

    def loadmap(self, x, y):
        random.seed("TEST")
        content = ("~", ".", ",", "!", "?")

        self.cells = []
        for Y in range(y):
            self.cells.append([])
            for X in range(x):
                self.cells[Y].append(content[randint(0, 4)])
        self.height = Y+1
        self.width = X+1
