class Map:
    def __init__(self):
        self.map = None
        self.height = None
        self.width = None

    def loadmap(self, x, y, initial):
        self.map = []
        for Y in range(y):
            self.map.append([])
            for X in range(x):
                self.map[Y].append(initial)
        self.height = Y+1
        self.width = X+1
