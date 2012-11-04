from hex import *

# PLEASE DON'T KILL ME
ONE_THIRD = float(1)/3
TWO_THIRD = float(2)/3

vertex_positions = [
    #NW
    (ONE_THIRD, -TWO_THIRD),
    #NE
    ( TWO_THIRD, -ONE_THIRD),
    #CE
    ( ONE_THIRD,  ONE_THIRD),
    #SE
    (-ONE_THIRD,  TWO_THIRD),
    #SW
    (-TWO_THIRD,  ONE_THIRD),
    #CW
    (-ONE_THIRD, -ONE_THIRD),
]

edge_positions = [
(.5, -.5),
(.5, 0),
(0, .5),
(-.5, .5),
(-.5, 0),
(0, -.5)
]

# Constants for turns function.
LEFT = 1
STRAIGHT = 0
RIGHT = -1

# Determine whether the third point is to the left or right of a line.
def turns(pos1, pos2, pos3):
    cross = (pos2[0]-pos1[0]) * (pos3[1]-pos1[1]) - (pos3[0]-pos1[0]) * (pos2[1]-pos1[1])
    if cross > 0:
        return LEFT
    # TODO: Determine what a good float margin of error is.
    elif cross == 0: # abs(cross) < .001:
        return STRAIGHT
    else:
        return RIGHT

# Determine whether more than half of a hex is to a given side of an arm of an arc.
def arc_side(center, arc_arm, vertices, side):
    matches = 0
    for i in range(6):
        direction = turns(center, arc_arm, vertices[i])
        if direction == side:
            matches += 1
    if matches > 3:
        return True
    return False

# Generate the vertices for a hexagon.
def setup_vertices(cells):
    hexagons = []
    for cell in cells:
        vertices = []
        for x in range(6):
            vertices.append(add(cell, vertex_positions[x]))
        hexagons.append((cell, vertices))
    return hexagons

# Generate the edges for a hexagon.
def setup_edges(cells):
    hexagons = []
    for cell in cells:
        edges = []
        for x in range(6):
            edges.append(add(cell, edge_positions[x]))
        hexagons.append((cell, edges))
    return hexagons


# Field of view instance.
class FOV:
    def __init__(self, center, map):
        self.center = center
        self.map = map
        self.cells = [setup_vertices([self.center])]
        self.cells.append(setup_vertices(fov_perimeter(1, self.center)))
        vertices = self.cells[0][0][1]
        self.arcs = []
        self.arcs.append(Arc(self, 0, 2, add(self.center,edge_positions[5]), add(self.center,edge_positions[1])))#vertices[5], vertices[1]))
# WORKS:        self.arcs.append(Arc(self, 1, 2, vertices[0], vertices[2]))
#        self.arcs.append(Arc(self, 2, 3, vertices[1], vertices[3]))
# WORKS:        self.arcs.append(Arc(self, 3, 4, vertices[2], vertices[4]))
#        self.arcs.append(Arc(self, 4, 5, vertices[3], vertices[5]))
# WORKS:        self.arcs.append(Arc(self, 4, 5, vertices[3], vertices[5]))
        self.visible = {}

    # Calculate whether you can see the hexes at the given rank.
    def calculate(self, rank=1):
        # Set up arcs.
        self.cells.append(setup_vertices(fov_perimeter(rank+1, self.center)))

        # Extend arcs.
        remaining = []
        for arc in self.arcs:
            remaining.extend(arc.process(rank))
        self.arcs = remaining

        # Continue to calculate if there are more arcs.
        if self.arcs and rank < 7:
            for arc in self.arcs:
                arc.expand(rank)

            self.calculate(rank+1)

# A FOV arc.
class Arc:
    def __init__(self, parent, start, stop, cw, ccw):
        self.parent = parent
        self.center = self.parent.center
        self.start = start # Starting hexagon.
        self.stop = stop # Stop at this hexagon.
        self.cw = cw # Clockwise arm.
        self.ccw = ccw # Counterclockwise arm.

    def expand(self, rank):

        # Which general face of the hex, and which position along 
        # that face.
        face = self.start / rank
        position = self.start % rank
        start = face * (rank+1) + position + rank % 2

        while start > 0:
            pos, vertices = self.parent.cells[rank+1][start-1]
            if arc_side(self.center, self.cw, vertices, RIGHT) is True:
                break
            start -= 1

        face = self.stop / rank
        position = self.stop % rank
        stop = face * (rank+1) + position# + rank % 2# + 1# - rank/4 + 1#+ 1#- 1# - rank# + 4#- rank#- 1# - 1# + 1#- 1

        while stop < rank+1 * 6 - 1:
            pos, vertices = self.parent.cells[rank+1][stop+1]
            if arc_side(self.center, self.ccw, vertices, LEFT) is True:#RUE:#False:#False:
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

    # Contract an arc in the CW direction.
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

    mapsize = 20
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
                elif fov.visible.get((x,y)):# is True:
                    if map[(x,y)] is False:
                        sys.stdout.write("T")
                    else:
                        sys.stdout.write(".")
                        pygame.draw.circle(window, colors[fov.visible.get((x,y))], draw_pos((x,y)), 2, 0)
                elif fov.visible.get((x,y)) is not None:
                    sys.stdout.write(fov.visible.get((x,y)))
                elif map[(x,y)] is False:
                    sys.stdout.write("x")
                else:
                    sys.stdout.write("~")
            sys.stdout.write("\n")
        sys.stdout.write("\n\n")
        pygame.display.update()

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
