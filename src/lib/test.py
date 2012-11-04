from random import randint

hex_width = 801
num_hexes = 6*(hex_width-1) + hex_width
hexes = {}

class Cell:
    def __init__(self):
        self.contents = {}
        for x in range(100):
            self.contents[x] = "-" * randint(1, 10000)

for x in range(num_hexes):
    hexes[x] = Cell()

while True is True:
    continue
