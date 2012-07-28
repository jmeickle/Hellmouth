from hex import *
import pygame
pygame.init()
window = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption('Hex FOV Test')

def draw_pos(pos):
    return pos[0]*50, pos[1]*50

pygame_colors = {}
pygame_colors['red'] = pygame.Color(255, 0, 0)
pygame_colors['green'] = pygame.Color(0, 255, 0)
pygame_colors['blue'] = pygame.Color(0, 0, 255)
pygame_colors['yellow'] = pygame.Color(255, 255, 0)
pygame_colors['cyan'] = pygame.Color(0, 255, 255)
pygame_colors['magenta'] = pygame.Color(255, 0, 255)
pygame_colors['white'] = pygame.Color(255, 255, 255)
pygame_colors['grey'] = pygame.Color(128, 128, 128)

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

font = pygame.font.Font('freesansbold.ttf', 10)

def type(msg, pos):
    message = font.render(msg, False, pygame_colors['white'])
    message_rect = message.get_rect()
    message_rect.topleft = add(pos, (-10, -15))
    window.blit(message, message_rect)

def draw_hex(hex):
    center, vertices = hex
    pygame.draw.circle(window, pygame_colors['grey'], draw_pos(center), 1, 0)
    #type("(%s,%s)" % center, draw_pos(center))
    for i in range(6):
        pygame.draw.line(window, pygame_colors['grey'], draw_pos(vertices[i]), draw_pos(vertices[(i+1)%6]), 1)
    pygame.display.update()

# Constants for turns function.
LEFT = 1
STRAIGHT = 0
RIGHT = -1

# Generate the vertices for a hexagon.
def setup_vertices(cells):
    hexagons = []
    for cell in cells:
        vertices = []
        for x in range(6):
            vertices.append(add(cell, vertex_positions[x]))
#            vertex = mult(add(dirs[x%6], dirs[(x+1)%6]), .333)
#            vertices.append(add(cell, vertex))
        hexagons.append((cell, vertices))
#    exit(hexagons)
    for hexagon in hexagons:
        draw_hex(hexagon)
    return hexagons

# Determine which side a point is on.
def turns(pos1, pos2, pos3):
    cross = (pos2[0]-pos1[0]) * (pos3[1]-pos1[1]) - (pos3[0]-pos1[0]) * (pos2[1]-pos1[1])
    if cross > 0:
        return LEFT
    elif cross == 0: #abs(cross) < .001:
        return STRAIGHT
    else:
        return RIGHT

def arc_side(center, arc, vertices, side):
    matches = 0
    for i in range(6):
        direction = turns(center, arc, vertices[i])
        if direction == side:# or direction == STRAIGHT:
            matches += 1
    if matches > 2:
        return True
    return False

class FOV:
    def __init__(self, center, map):
        self.center = center
        self.map = map
        self.cells = [setup_vertices([self.center])]
        self.cells.append(setup_vertices(fov_perimeter(1, self.center)))
        vertices = self.cells[0][0][1]
        self.arcs = []
        self.arcs.append(Arc(self, 1, 2, vertices[0], vertices[2]))
#        self.arcs.append(Arc(self, 2, 3, vertices[1], vertices[3]))
# WORKS:        self.arcs.append(Arc(self, 3, 4, vertices[2], vertices[4]))
#        self.arcs.append(Arc(self, 4, 5, vertices[3], vertices[5]))


#        self.arcs = [Arc(self, 1, 2, vertices[0], vertices[2])]
#        self.arcs = [Arc(self, 3, 4, vertices[2], vertices[4])]

        pygame.draw.circle(window, pygame_colors['yellow'], draw_pos(self.arcs[0].cw), 2, 0)
        pygame.draw.circle(window, pygame_colors['cyan'], draw_pos(self.arcs[0].ccw), 2, 0)
#        self.arcs.append(Arc(self, 1, 2, vertices[1], vertices[3]))

#        self.arcs.append(Arc(self, 2, 3, vertices[1], vertices[3]))
#        self.arcs.append(Arc(self, 4, 5, vertices[0], vertices[4]))
#        self.arcs.append(Arc(self, 4, 5, vertices[0], vertices[3]))
#        self.arcs.append(Arc(self, 3, 4, vertices[5], vertices[3]))
#(vertices[0][0], self.center[1]), (self.center[0], vertices[4][1])))
#        self.arcs.append(Arc(self, 3, 4, (vertices[0][0], self.center[1]), (self.center[0], vertices[4][1])))
#        self.arcs.append(Arc(self, 4, 5, (vertices[0][0], self.center[1]), (self.center[0], vertices[4][1])))
#        pygame.draw.circle(window, pygame_colors['magenta'], draw_pos((vertices[4][0], self.center[1])), 4, 0)
#        pygame.draw.circle(window, pygame_colors['magenta'], draw_pos((self.center[0], vertices[0][1])), 4, 0)
        pygame.draw.line(window, pygame_colors['yellow'], draw_pos(self.center), draw_pos(self.arcs[0].cw), 1)
        pygame.draw.line(window, pygame_colors['cyan'], draw_pos(self.center), draw_pos(self.arcs[0].ccw), 1)
        self.visible = {}

    # Calculate whether you can see the hexes at rank.
    def calculate(self, rank=1):
        for x in range(len(self.cells[rank])):
            pos, vertices = self.cells[rank][x]
            type("%s"%x, draw_pos(pos))

        self.cells.append(setup_vertices(fov_perimeter(rank+1, self.center)))

        remaining = []
        for arc in self.arcs:
            remaining.extend(arc.process(rank))
        self.arcs = remaining

        for arc in self.arcs:
            pygame.draw.line(window, pygame_colors['yellow'], draw_pos(arc.center), draw_pos(arc.cw), 1)
            pygame.draw.circle(window, pygame_colors['yellow'], draw_pos(arc.cw), 2, 0)
            pygame.draw.line(window, pygame_colors['cyan'], draw_pos(arc.center), draw_pos(arc.ccw), 1)
            pygame.draw.circle(window, pygame_colors['cyan'], draw_pos(arc.ccw), 2, 0)
            pygame.draw.line(window, pygame_colors['red'], draw_pos(arc.cw), draw_pos(arc.ccw), 1)
#            for index in range(arc.start, arc.stop+1):
#                pos, vertices = self.cells[rank][index]
#                self.visible[pos] = True
                #if arc.stop+1 - arc.start > 10:
                    #exit("Rank: %s, Arc: %s" % (rank, arc.__dict__))
            # Set this cell as visible/seen.
  #              if index >= len(self.cells[rank]):
  #                  exit("Rank: %s, Arc Stop: %s"%(rank,arc.stop))
#                    exit(self.__dict__)
  #              pos, vertices = self.cells[rank][index]
 #               print "Rank %s, hex %s\nArc: %s" % (rank, index, arc.__dict__)
#                pygame.draw.circle(window, pygame_colors['magenta'], draw_pos(pos), 2, 0)

        if self.arcs and rank < 7:
            for arc in self.arcs:
                arc.expand(rank)

            self.calculate(rank+1)

class Arc:
    def __init__(self, parent, start, stop, cw, ccw):
        self.parent = parent
        self.center = self.parent.center
        self.start = start # Starting hexagon.
        self.stop = stop # Stop at this hexagon.
        self.cw = cw # Clockwise arm.
        self.ccw = ccw # Counterclockwise arm.

    def expand(self, rank):

#   // given a HexGrid, this expands the current arc out one radius unit,
#   // respecting the arc limits (r is presumed to be the existing radius)
#   void expandArc(HexGrid hg,int r) {
#      // we have to calculate the new indices of the next outer bubble.
#      // to accomodate partially-visible hexagons, we have to verify the
#      // starting and ending hexagon.
#      // Note that we switch calls to leftOfArc and rightOfArc.  This is
#      // because our y-coord increases downward

        # Which general face of the hex, and which position along 
        # that face.
        face = self.start / rank#(max(rank, 1))
        position = self.start % rank#(max(rank, 1))

#        if rank == 2:# and self.stop > 3:
#            exit(self.__dict__)
#            exit("Face: %s, Position: %s, Start: %s, Stop: %s" % (face, position, start, stop))

        # Limit maximum size of arcs.
#        if position == 0 and (face == 0 or face == 3):
#            start = face * (rank+1)
#        else:
#            start = face * (rank+1) + position + 1# - 1#+ 1

#        start = face * (rank+1) + position# + 1# - 1#+ 1
#        if position == 0:
#            start = face * (rank+1)
#        else:
        start = face * (rank+1) + position + rank % 2 + 1# + 1# + 1# + 4# + 1# - 1# + 1# - 1#+ 1

#        if face == 0 or face == 3:
#            start -= 1

        while start > 0:
            pos, vertices = self.parent.cells[rank+1][start-1]
            if arc_side(self.center, self.cw, vertices, RIGHT) is True:#False:#True:#False:
#                start += 1 
#            if arc_side(self.center, self.cw, vertices, RIGHT) is False:
                break
            start -= 1

#        if self.cw[1] <= self.center[1] and self.ccw[1] <= self.center[1]:
#            while (start > 0):
#                pos, vertices = self.parent.cells[rank+1][start-1]
#                if arc_side(self.center, self.cw, vertices, RIGHT) is False:
 #                   if pos not in self.parent.visible:
 #                       self.parent.visible[pos] = "+"
 #                   break
 #               start -= 1
 #       else:
 #           while start > (rank+1)*3:
 #               pos, vertices = self.parent.cells[rank+1][start-1]
 #               if arc_side(self.center, self.cw, vertices, RIGHT) is False:
 #                   if pos not in self.parent.visible:
 #                       self.parent.visible[pos] = "-"
 #                   break
 #               start -= 1

        face = self.stop / rank#(max(rank, 1))
        position = self.stop % rank#(max(rank, 1))

#        if position == 0 and (face == 0 or face == 3):
#            stop = face * (rank+1)
#        else:
#            stop = face * (rank+1) + position +1# + 1#- 1
 #       if position == 0:
 #           stop = face * (rank+1)
 #       else:
        stop = face * (rank+1) + position + rank % 2# + 1# - rank/4 + 1#+ 1#- 1# - rank# + 4#- rank#- 1# - 1# + 1#- 1

#        if face == 0 or face == 3:
#            stop -= 1

        while stop < rank+1 * 6 - 1:
            pos, vertices = self.parent.cells[rank+1][stop+1]
#            if arc_side(self.center, self.ccw, vertices, LEFT) is False:
            if arc_side(self.center, self.ccw, vertices, LEFT) is True:#RUE:#False:#False:
                break
            stop += 1

#        if self.cw[1] <= self.center[1] and self.ccw[1] <= self.center[1]:
#            while stop < (rank+1) * 3 - 1:
#                pos, vertices = self.parent.cells[rank+1][stop+1]
#                if arc_side(self.center, self.ccw, vertices, LEFT) is False:
#                    if pos not in self.parent.visible:
#                        self.parent.visible[pos] = "A"
#                    break
#                stop += 1
#        else:
#            while stop < (rank+1) * 6 - 1:
#                pos, vertices = self.parent.cells[rank+1][stop+1]
#                if arc_side(self.center, self.ccw, vertices, LEFT) is False:
#                    if pos not in self.parent.visible:
#                        self.parent.visible[pos] = "B"
#                    break
#                stop += 1

        self.start = start
        self.stop = stop
#        if rank == 1:# and self.stop > 3:
#            exit("Face: %s, Position: %s, Start: %s, Stop: %s" % (face, position, start, stop))
#            exit(self.__dict__)

    def process(self, rank):
        arcs = []
#        if rank == 2:
#            exit(self.__dict__)
        span = range(self.start, self.stop+1)
        for index in span:
        #    if index >= len(self.parent.cells[rank]):
        #        exit("Exceeded rank: %s, %s, %s" % (len(self.parent.cells[rank]), self.start, self.stop))
            pos, vertices = self.parent.cells[rank][index]
            tile = self.parent.map.get(pos)
            if tile is False:
                pygame.draw.circle(window, pygame_colors['yellow'], draw_pos(pos), 6, 0)
                self.contractCW(vertices)
                self.start += 1
                self.parent.visible[pos] = "red"
            else:
                self.parent.visible[pos] = "yellow"
                break

        for index in reversed(span):
            #if index >= len(self.parent.cells[rank]):#rank*6:
            #    exit("%s, %s" % (self.start, self.stop))
            pos, vertices = self.parent.cells[rank][index]
            tile = self.parent.map.get(pos)
            if tile is False:
                pygame.draw.circle(window, pygame_colors['cyan'], draw_pos(pos), 6, 0)
                self.contractCCW(vertices)
                self.stop -= 1
                self.parent.visible[pos] = "red"
            else:
                self.parent.visible[pos] = "cyan"
                break

        if self.empty() is True:
            return arcs
#        exit("this far")

#      // now, the arc has been appropriately contracted on both ends.
#      // We also have to run through interior points and split the arc
#      // if we find obstacles.
        for index in range(self.start+1, self.stop):
#        for index in range(self.start, self.stop+1):
            pos, vertices = self.parent.cells[rank][index]
            tile = self.parent.map.get(pos)
            if tile is not False:
                self.parent.visible[pos] = "magenta"
            else:
                pygame.draw.circle(window, pygame_colors['red'], draw_pos(pos), 6, 0)
                self.parent.visible[pos] = "!"
           # // split arc into two pieces; the first is our original arc
           # // and it stops just before this obstacle.  The second is the
           # // is a newly allocated arc for the rest of the original arc.
            #// We terminate this arc, and then call this method recursively
          #  // on the new arc, but only after contracting both away from
          #  // the obstacle separating them.  This may cause either to
          #  // become an empty arc.
                # TODO: Check whether chosen vertex matters?
                child = Arc(self.parent, index+1, self.stop, self.cw, self.ccw)
                child.contractCW(vertices)
                self.stop = index - 1
                self.contractCCW(vertices)
                if child.empty() is False:
                    arcs.extend(child.process(rank))

        if self.empty() is False:
            arcs.append(self)

        return arcs

    # Contract an arc in the CW direction.
    def contractCW(self, vertices):
        best_cw = self.cw
        for index in range(6):
            if turns(self.center, best_cw, vertices[index]) == LEFT:#>= STRAIGHT:#LEFT:#RIGHT:
#            if turns(self.center, best_cw, vertices[index]) <= STRAIGHT:#>= STRAIGHT:#LEFT:#RIGHT:
                best_cw = vertices[index]
        self.cw = best_cw

    # Contract an arc in the CCW direction.
    def contractCCW(self, vertices):
        best_ccw = self.ccw
        for index in range(6):
#            if turns(self.center, best_ccw, vertices[index]) >= STRAIGHT:#RIGHT:#LEFT:
            if turns(self.center, best_ccw, vertices[index]) == RIGHT:#< STRAIGHT:#RIGHT:#LEFT:
                best_ccw = vertices[index]
        self.ccw = best_ccw

    # Determine whether an arc is empty.
    def empty(self):
        if self.start > self.stop:
            return True
#        if turns(self.center, self.cw, self.ccw) != RIGHT:
        if turns(self.center, self.cw, self.ccw) == RIGHT:#!= LEFT:#== RIGHT:#!= LEFT:
#            exit("%s"%turns(self.center, self.cw, self.ccw))
#            pygame.draw.circle(window, pygame_colors['red'], draw_pos(self.center), 6, 0)
#            pygame.draw.circle(window, pygame_colors['green'], draw_pos(self.cw), 6, 0)
#            pygame.draw.circle(window, pygame_colors['blue'], draw_pos(self.ccw), 6, 0)
#            pygame.display.update()
#            while True is True:
#                pass
            return True
        return False

# Test code.
if __name__ == '__main__':
    # Generate map
    mapsize = 20
    map = {}
    for x in range(mapsize):
        for y in range(mapsize):
            map[(x,y)] = True

    # Set up random blocking columns
    import random
    for column in range(mapsize):
#        continue
        x = random.randint(0, mapsize-1)
        y = random.randint(0, mapsize-1)
        map[(x,y)] = False
        pygame.draw.circle(window, pygame_colors['grey'], draw_pos((x,y)), 12, 0)

    # Generate FOV map.
    center = (mapsize/2, mapsize/2)
    fov = FOV(center, map)
    fov.calculate()

    pygame.draw.circle(window, pygame_colors['magenta'], draw_pos(center), 6, 0)
    pygame.display.update()
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
                    pygame.draw.circle(window, pygame_colors[fov.visible.get((x,y))], draw_pos((x,y)), 2, 0)
            elif fov.visible.get((x,y)) is not None:
                sys.stdout.write(fov.visible.get((x,y)))
            elif map[(x,y)] is False:
                sys.stdout.write("x")
            else:
                sys.stdout.write("~")
        sys.stdout.write("\n")
print len(fov.arcs)

pygame.display.update()

while True is True:
    pass
#    for event in pygame.event.get():
#        if event.type == KEYDOWN:
#            f



