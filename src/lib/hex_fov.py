from hex import *

# In this algorithm, hexagons can be referenced in two ways. The first way is
# unique to this algorithm, and involves referring to them by the order they
# would be reached if traveling around that rank. For example:
#
# NW
#     0   1   2
#   11  0   1   3
# 10  5   0   2   4
#   9   4   3   5
#     8   7   6
#               SE
#
# Note that in this arrangement, the northwestern most hex will always be 0.
#
# As elsewhere, we also use a hexagonal grid with two axes. The x-axis
# functions as it would on a square grid, while the y-axis is 'skewed' such
# that moving along it also results in 'horizontal' movement:
#
#       -y
#  \   \   \   \ 
#   \   \   \   \
# ---\---\---\---\---
#     \   \   \   \ 
#      \   \   \   \
# -x ---\---O---\---\--- +x
#        \   \   \   \ 
#         \   \   \   \
#       ---\---\---\---\---
#           \   \   \   \
#            \   \   \   \
#                  +y
#
# Since we represent everything in (x,y) coordinates, a zoomed-in hexagon looks
# like this when its vertices, edge midpoints, etc. are given coordinates:
#
#           /.\                  / \
# y-axis   / . \                /   \
#   \\    /  .  \              /     \
#   ||   /   .   \ (.5,-.5)   /       \
#    \\ /    .    O          /         \
#     \\     .     \        /           \
#     ||     .      \      /             \
#    / \\    .       \    /               \
#   /   \\   .        \  /                 \
#  /.   ||   .     (.33,-.66)               \
#  |  .  \\  .    .    ||                   |
#  |    . \\ .  .      ||                   |
#  |      .||..        ||                   |
# ===========O=======(0,.5)=======O=========|==
#  |       (0,0)       ||       (0,1)       |  x-axis
#  |      .  .\\.      ||                   |
#  |    .    . \\ .    ||                   |
#  |  .      .  ||  .  ||                   |
#  |.        .  \\ (.33,.33)                |
#  \     O   .   \\    /\                   /
#   \(-.33,.33)  ||   /  \                 /
#    \       .   \\  /    \               /
#     \      .    \\/      \             /
#      \     .    ||        \           /
#       \    .    \\         \         /
#        \   .   / \\         \       /
#         \  .  /  ||          \     /
#          \ . /   \\           \   /
#           \./     \\           \ /
#
# Representing this requires floating point math, which would break symmetry in
# this algorithm due to rounding errors. However, every interesting point can
# be achieved with a divisor of 1, 2, or 3. This means that multiplying all
# values by 6 results in a pure-integer representation of the same information:
#
#           /.\                  / \
# y-axis   / . \                /   \
#   \\    /  .  \              /     \
#   ||   /   .   \ (3,-3)     /       \
#    \\ /    .    O          /         \
#     \\     .     \        /           \
#     ||     .      \      /             \
#    / \\    .       \    /               \
#   /   \\   .        \  /                 \
#  /.   ||   .       (2,-4)                 \
#  |  .  \\  .    .    ||                   |
#  |    . \\ .  .      ||                   |
#  |      .||..        ||                   |
# ===========O========(0,3)=======O=========|==
#  |       (0,0)       ||       (0,6)       |  x-axis
#  |      .  .\\.      ||                   |
#  |    .    . \\ .    ||                   |
#  |  .      .  ||  .  ||                   |
#  |.        .  \\    (2,2)                 |
#  \     O   .   \\    /\                   /
#   \(-2,2)  .   ||   /  \                 /
#    \       .   \\  /    \               /
#     \      .    \\/      \             /
#      \     .    ||        \           /
#       \    .    \\         \         /
#        \   .   / \\         \       /
#         \  .  /  ||          \     /
#          \ . /   \\           \   /
#           \./     \\           \ /
#
# Indexing by multiples of 6 would be intensely irritating, so instead it is
# only done when needed (i.e., in this algorithm). Everywhere else in the code,
# the first hexagon to the right of (0,0) will be (0,1).

# Vertices:
vertex_positions = [
(4, -2),  # NE-CE
(2, 2),   # CE-SE
(-2, 4),  # SE-SW
(-4, 2),  # SW-CW
(-2, -2), # CW-NW
(2, -4),  # NW-NE
]

# Edges:
edge_positions = [
(0, -3), # NW
(3, -3), # NE
(3, 0),  # CE
(0, 3),  # SE
(-3, 3), # SW
(-3, 0), # CW
]

# Subtriangle centers:
center_positions = [
(0, -2), # NW
(2, -2), # NE
(2, 0),  # CE
(0, 2),  # SE
(-2, 2), # SW
(-2, 0), # CW
]

# TODO: Define these bitmasks
# CC
# NW
# NE
# CE
# SE
# SW
# CW

# Constants for turns function.
LEFT = 1
STRAIGHT = 0
RIGHT = -1

# Determine whether the third point is to the left or right of a line.
def turns(pos1, pos2, pos3):
    cross = (pos2[0]-pos1[0]) * (pos3[1]-pos1[1]) - (pos3[0]-pos1[0]) * (pos2[1]-pos1[1])
    if cross > 0:
        return LEFT
    elif cross == 0:
        return STRAIGHT
    else:
        return RIGHT

# Determine whether a hex is to be treated as to one side of an arc's arm.
def arc_side(center, arc_arm, checkpoints, side, checks=1):
    matches = 0
    for i in range(6):
        direction = turns(center, arc_arm, checkpoints[i])
        if direction == side or direction == STRAIGHT:
            matches += 1
    if matches > checks:
        return True
    return False

# Generate the checkpoints for a hexagon.
def setup_checkpoints(cell, positions):
    checkpoints = []
    for x in range(6):
        checkpoints.append(add(cell, positions[x]))
    return checkpoints

# Generate the checkpoints for a list of hexagons.
def setup_hexagons(cells, positions):
    hexagons = []
    for cell in cells:
        cell = mult(cell, 6)
        checkpoints = []
        for x in range(6):
            checkpoints.append(add(cell, positions[x]))
        hexagons.append((cell, checkpoints))
    return hexagons

# Field of view instance.
class FOV:
    def __init__(self, center, map, range = 20, checkpoints = center_positions):
        # See notes at the top:
        self.center = center # The REAL coordinate.
        self.origin = mult(center, 6) # The FOV algorithm coordinate.

        self.map = map
        self.range = range

        # Which checkpoints to use - can be triangle centers, edges, or vertices.
        self.checkpoints = checkpoints

        # Cells traversed by the algorithm. Starts with the center hex.
        self.cells = [setup_hexagons([self.center], self.checkpoints)]
#        self.cells.append(setup_hexagons(dirs, self.checkpoints))

        # Cells found visible by the algorithm.
        self.visible = {}

        # The center cell's vertices, to generate arcs from.
        cell = setup_hexagons([self.center], vertex_positions)
        vertices = cell[0][1]

        # Arcs are defined as parent, start hex, stop hex, cw arm vertex, ccw arm vertex.
        self.arcs = []

        # Define the initial three arcs that LOS is split into.
        self.arcs.append(Arc(self, 0, 1, vertices[4], vertices[0])) # NW through NE.
#        self.arcs.append(Arc(self, 2, 3, vertices[0], vertices[2])) # CE through SE.
#        self.arcs.append(Arc(self, 4, 5, vertices[2], vertices[4])) # SW through CW.
#        print cell
#        print vertices

    # Get a hexagonal perimeter in the proper order for the algorithm.
    def perimeter(self, rank):
        cells = []
        corner = add(self.center, mult(NW, rank))
        for dir in [CE, SE, SW, CW, NW, NE]:
            cells.append(corner)
            for cell in cardinal_line(corner, rank, dir):
                cells.append(cell)
            corner = cells.pop()
        return cells

    # Calculate whether you can see the hexes at the given rank.
    def calculate(self, rank=1):
        # Set up the next rank of cells.
        self.cells.append(setup_hexagons(self.perimeter(rank), self.checkpoints))

        # Expand the arcs into them.
        for arc in self.arcs:
            arc.expand(rank)

        # Process the expanded arcs.
        remaining = []
        for arc in self.arcs:
            remaining.extend(arc.process(rank))
        self.arcs = remaining

        # Continue to calculate if there are more arcs.
        if self.arcs:
            if rank < self.range:
                self.calculate(rank+1)

# A FOV arc.
class Arc:
    def __init__(self, parent, start, stop, cw, ccw):
        self.parent = parent
        self.center = self.parent.origin
        self.start = start # Starting hexagon.
        self.stop = stop # Stop at this hexagon.
        self.cw = cw # Clockwise arm.
        self.ccw = ccw # Counterclockwise arm.

    def expand(self, rank):
        # Which general face of the hex, and which position along that face.
        face = self.start / max(1, rank - 1)
        position = self.start % max(1, rank - 1)
        start = face * rank + position + 1

        while start >= 0 or start < rank * 6 - rank % 2:
            pos, vertices = self.parent.cells[rank][start-1]
            if arc_side(self.center, self.cw, vertices, RIGHT) is True:
                break
            start -= 1

        face = self.stop / rank
        position = self.stop % rank
        stop = face * rank + position

        while stop < rank * 6 - 1:
            pos, vertices = self.parent.cells[rank][stop+1]
            if arc_side(self.center, self.ccw, vertices, LEFT) is True:
                break
            stop += 1

        self.start = start
        self.stop = stop

    def process(self, rank):
        arcs = []

        # Contract the clockwise arm of the arc until a non-blocked hex is found.
        for index in range(self.start, self.stop+1):
            pos, vertices = self.parent.cells[rank][index]
            tile = self.parent.map.get(pos)
            if tile is False:
                self.contractCW(vertices)
                self.start += 1
                self.parent.visible[pos] = "red"
            else:
                self.parent.visible[pos] = "yellow"
                break

        # Contract the counterclockwise arm of the arc until a non-blocked hex is found.
        for index in reversed(range(self.start, self.stop+1)):
            pos, vertices = self.parent.cells[rank][index]
            tile = self.parent.map.get(pos)
            if tile is False:
                self.contractCCW(vertices)
                self.stop -= 1
                self.parent.visible[pos] = "red"
            else:
                self.parent.visible[pos] = "cyan"
                break

        # Exit early if the arc is too small to contain anything.
        if self.empty() is True:
            return arcs

        # Go across the arc's span, excepting the very start and end, splitting into two arcs if an obstacle is detected.
        for index in range(self.start+1, self.stop):
            pos, vertices = self.parent.cells[rank][index]
            tile = self.parent.map.get(pos)
            if tile is not False:
                self.parent.visible[pos] = "magenta"
            else:
                self.parent.visible[pos] = "!"
                child = Arc(self.parent, index+1, self.stop, self.cw, self.ccw)
                child.contractCW(vertices)
                self.stop = index - 1
                self.contractCCW(vertices)
                if child.empty() is False:
                    arcs.extend(child.process(rank))

        # We always pass on our children, but we also keep going if we're not empty.
        if self.empty() is False:
            arcs.append(self)

        return arcs

    # TODO: Remove asymmetry
    # Contract an arc in the CW direction.
    # def contractCW(self, vertices):
    #     best_cw = self.cw
    #     for index in range(6):
    #         matches = 0
    #     for i in range(6):
    #         direction = turns(center, arc_arm, checkpoints[i])
    #         if direction == side or direction == STRAIGHT:
    #             matches += 1
    #     if matches > checks:
    #         return True
    #     return False

    def contractCW(self, vertices):
        best_cw = self.cw
        for index in range(6):
            if turns(self.center, best_cw, vertices[index]) == LEFT:
                best_cw = vertices[index]
        self.cw = best_cw

    # Contract an arc in the CCW direction.
    def contractCCW(self, vertices):
        best_ccw = self.ccw
        for index in range(6):
            if turns(self.center, best_ccw, vertices[index]) == RIGHT:
                best_ccw = vertices[index]
        self.ccw = best_ccw

    # Determine whether an arc is empty.
    def empty(self):
        if self.start > self.stop:
            return True
        if turns(self.center, self.cw, self.ccw) == RIGHT:
            return True
        return False

# Test code.
if __name__ == '__main__':
    import pygame
    pygame.init()
    pygame.display.set_caption('Hex FOV Test')

    window = pygame.display.set_mode((1000, 1000))
    
    font = pygame.font.Font('freesansbold.ttf', 10)

    colors = {}
    colors['red'] = pygame.Color(255, 0, 0)
    colors['green'] = pygame.Color(0, 255, 0)
    colors['blue'] = pygame.Color(0, 0, 255)
    colors['yellow'] = pygame.Color(255, 255, 0)
    colors['cyan'] = pygame.Color(0, 255, 255)
    colors['magenta'] = pygame.Color(255, 0, 255)
    colors['white'] = pygame.Color(255, 255, 255)
    colors['grey'] = pygame.Color(128, 128, 128)

    # Screen position to draw to, given a map position.
    def draw_pos(pos):
        return pos[0]*50, pos[1]*50

    # Type something out to the screen.
    def type(msg, pos):
        message = font.render(msg, False, colors['white'])
        message_rect = message.get_rect()
        message_rect.topleft = add(pos, (-10, -15))
        window.blit(message, message_rect)

    # Draw a hex.
    def draw_hex(hex):
        center, edges = hex
        vertices = []
        for x in range(6):
            vertices.append(add(center, vertex_positions[x]))
        pygame.draw.circle(window, colors['grey'], draw_pos(center), 1, 0)
        type("(%s,%s)" % center, draw_pos(center))
        for i in range(6):
            pygame.draw.line(window, colors['grey'], draw_pos(vertices[i]), draw_pos(vertices[(i+1)%6]), 1)

    mapsize = 30
    center = (mapsize/2, mapsize/2)

    # Generate map
    def generatemap():
        map = {}
        for x in range(mapsize):
            for y in range(mapsize):
                map[(x,y)] = True

        # Set up random blocking columns
        import random
        for column in range(mapsize):
            x = random.randint(0, mapsize-1)
            y = random.randint(0, mapsize-1)
            map[(x,y)] = False
        return map
    #pygame.draw.circle(window, colors['grey'], draw_pos((x,y)), 12, 0)

    # Generate FOV map.
    map = generatemap()
    fov = FOV(center, map)
    fov.calculate()

    def mapdraw():
        #pygame.draw.circle(window, colors['magenta'], draw_pos(center), 6, 0)
        #pygame.display.update()
        import sys
        for y in range(mapsize):
            sys.stdout.write(" " * y)
            for x in range(mapsize):
                sys.stdout.write(" ")
                if center == (x,y):
                    sys.stdout.write("@")
                elif fov.visible.get((x*6,y*6)):# is True:
                    if map[(x,y)] is False:
                        sys.stdout.write("T")
                    else:
                        sys.stdout.write(".")
                        #pygame.draw.circle(window, colors[fov.visible.get((x,y))], draw_pos((x,y)), 2, 0)
                elif fov.visible.get((x*6,y*6)) is not None:
                    sys.stdout.write(fov.visible.get((x*6,y*6)))
                elif map[(x,y)] is False:
                    sys.stdout.write("x")
                else:
                    sys.stdout.write("~")
            sys.stdout.write("\n")
        sys.stdout.write("\n\n")
        #pygame.display.update()

    while True is True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                map = generatemap()
                fov = FOV(center, map)
                fov.calculate()
                mapdraw()
#        for x in range(len(self.cells[rank])):
#            pos, vertices = self.cells[rank][x]
#            type("%s"%x, draw_pos(pos))
#        for arc in self.arcs:
#            pygame.draw.line(window, colors['yellow'], draw_pos(arc.center), draw_pos(arc.cw), 1)
#            pygame.draw.circle(window, colors['yellow'], draw_pos(arc.cw), 2, 0)
#            pygame.draw.line(window, colors['cyan'], draw_pos(arc.center), draw_pos(arc.ccw), 1)
#            pygame.draw.circle(window, colors['cyan'], draw_pos(arc.ccw), 2, 0)
#            pygame.draw.line(window, colors['red'], draw_pos(arc.cw), draw_pos(arc.ccw), 1)
