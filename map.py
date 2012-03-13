class Map:
    def __init__(self):
        self.cells = None
        self.height = None
        self.width = None

    def loadmap(self, x, y):
        content = ("~", ".", ",")

        self.cells = []
        for Y in range(y):
            self.cells.append([])
            for X in range(x):
                self.cells[Y].append(content[X%3])
        self.height = Y+1
        self.width = X+1
