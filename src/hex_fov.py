from hex import *

# Constants for turns function.
LEFT = 1
RIGHT = -1
STRAIGHT = 0

# Generate the vertices for a hexagon.
def setup_vertices(cells):
    hexagons = []
    for cell in cells:
        vertices = []
        for x in range(6):
            vertex = mult(add(dirs[x%6], dirs[(x+1)%6]), .5)
            vertices.append(add(cell, vertex))
        hexagons.append((cell, vertices))
    return hexagons

# Determine which side a point is on.
def turns(pos1, pos2, pos3):
    cross = (pos2[0]-pos1[0]) * (pos3[1]-pos1[1]) - (pos3[0]-pos1[0]) * (pos2[1]-pos1[1])
    if cross > 0:
        return LEFT
    elif abs(cross) < .01:
        return STRAIGHT
    else:
        return RIGHT

# TODO: Determine whether a hexagon is intersected by a line from pos1 to pos2.
#def intersects(cell, pos1, pos2):

#    vertex = vertex()
#    for dir in dirs:
#    mult(dir, vertex)
#    = add(cell, 
#    first = turns(pos1, pos2)

#   // returns true if this hexagon intersects the line passing through
#   // the given two points.
#   public boolean intersects(double x0,double y0,double x1,double y1) {
#      int side1,i,j;
#      side1 = turns(x0,y0,x1,y1,x[0],y[0]);
#      if (side1==STRAIGHT) return true;
#      for (i=1;i<6;i++) {
#         j = turns(x0,y0,x1,y1,x[i],y[i]);
#         if (j==STRAIGHT || j!=side1) return true;
#      }
#      return false;
#   }

# Returns whether a cell is to a given side of an arc.
def arc_side(center, arc, vertices, side):
    for i in range(6):
        if turns(center, arc, vertices[i]) == side:
            return True
    return False

#   2
# 3 /\ 1
#  |  |
# 4 \/ 0
#    5

class FOV:
    def __init__(self, center, map):
        self.center = center
        self.map = map
        self.cells = [setup_vertices([self.center])]
        self.cells.append(setup_vertices(fov_perimeter(1, self.center)))
        vertices = self.cells[0][0][1]
        self.arcs = []
        self.arcs.append(Arc(self, 0, 1, vertices[1], vertices[0]))
#        self.arcs.append(Arc(self, 0, 1, vertices[3], vertices[1]))
#        self.arcs.append(Arc(self, 1, 2, vertices[1], vertices[3]))
#        self.arcs.append(Arc(self, 2, 3, vertices[1], vertices[0]))
        self.visible = {}

    # Calculate whether you can see the hexes at rank.
    def calculate(self, rank=1):
        for arc in self.arcs:
            for index in range(arc.start, arc.stop+1):
                # Set this cell as visible/seen.
                pos, vertices = self.cells[rank][index]
                if pos not in self.visible:
                    self.visible[pos] = True

        self.cells.append(setup_vertices(fov_perimeter(rank+1, self.center)))

        remaining_arcs = []
        for arc in self.arcs:
            arc.expand(rank-1)
            remaining_arcs.extend(arc.process(rank))

        if remaining_arcs and rank < 10:
            self.arcs = remaining_arcs
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
        face = self.start / (max(rank, 1))
        position = self.start % (max(rank, 1))

        # Limit maximum size of arcs.
        if position == 0 and (face == 0 or face == 3):
            start = face * (rank+1)
        else:
            start = face * (rank+1) + position + 1

        if self.cw[1] <= self.center[1] and self.ccw[1] <= self.center[1]:
            while (start > 0):
                pos, vertices = self.parent.cells[rank+1][start-1]
                if arc_side(self.center, self.cw, vertices, RIGHT) is False:
 #                   if pos not in self.parent.visible:
 #                       self.parent.visible[pos] = "+"
                    break
                start -= 1
        else:
            while start > (rank+1)*3:
                pos, vertices = self.parent.cells[rank+1][start-1]
                if arc_side(self.center, self.cw, vertices, RIGHT) is False:
 #                   if pos not in self.parent.visible:
 #                       self.parent.visible[pos] = "-"
                    break
                start -= 1

        face = self.stop / (max(rank, 1))
        position = self.stop % (max(rank, 1))

        if position == 0 and (face == 0 or face == 3):
            stop = face * (rank+1)
        else:
            stop = face * (rank+1) + position - 1

        if self.cw[1] <= self.center[1] and self.ccw[1] <= self.center[1]:
            while stop < (rank+1) * 3 - 1:
                pos, vertices = self.parent.cells[rank+1][stop+1]
                if arc_side(self.center, self.ccw, vertices, LEFT) is False:
#                    if pos not in self.parent.visible:
#                        self.parent.visible[pos] = "A"
                    break
                stop += 1
        else:
            while stop < (rank+1) * 6 - 1:
                pos, vertices = self.parent.cells[rank+1][stop+1]
                if arc_side(self.center, self.ccw, vertices, LEFT) is False:
#                    if pos not in self.parent.visible:
#                        self.parent.visible[pos] = "B"
                    break
                stop += 1
        self.start = start
        self.stop = stop

    def process(self, rank):
        arcs = []

        for index in range(self.start, self.stop+1):
            if index >= len(self.parent.cells[rank]):
                exit("%s, %s, %s" % (len(self.parent.cells[rank]), self.start, self.stop))
            pos, vertices = self.parent.cells[rank][index]
            tile = self.parent.map.get(pos)
            if tile is False:
                self.contractCW(vertices)
                self.parent.visible[pos] = "/"
            else:
                break

        for index in reversed(range(self.start, self.stop+1)):
            #if index >= len(self.parent.cells[rank]):#rank*6:
            #    exit("%s, %s" % (self.start, self.stop))
            pos, vertices = self.parent.cells[rank][index]
            tile = self.parent.map.get(pos)
            if tile is False:
                self.contractCCW(vertices)
                self.parent.visible[pos] = "\\"
            else:
                break

        if self.empty():
            return arcs
      
#      // now, the arc has been appropriately contracted on both ends.
#      // We also have to run through interior points and split the arc
#      // if we find obstacles.
        for index in range(self.start+1, self.stop):
            pos, vertices = self.parent.cells[rank][index]
            tile = self.parent.map.get(pos)
            if tile is False:
                self.parent.visible[pos] = "!"
           # // split arc into two pieces; the first is our original arc
           # // and it stops just before this obstacle.  The second is the
           # // is a newly allocated arc for the rest of the original arc.
            #// We terminate this arc, and then call this method recursively
          #  // on the new arc, but only after contracting both away from
          #  // the obstacle separating them.  This may cause either to
          #  // become an empty arc.
                # TODO: Check whether chosen vertex matters?
                child = Arc(self.parent, index+1, self.stop, vertices[0], self.ccw)
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
            if turns(self.center, best_cw, vertices[index]) == RIGHT:
                best_cw = vertices[index]
        self.cw = best_cw

    # Contract an arc in the CCW direction.
    def contractCCW(self, vertices):
        best_ccw = self.ccw
        for index in range(6):
            if turns(self.center, best_ccw, vertices[index]) == LEFT:
                best_ccw = vertices[index]
        self.cw = best_ccw

    # Determine whether an arc is empty.
    def empty(self):
        if turns(self.center, self.cw, self.ccw) != RIGHT:
            return True
        if self.start > self.stop:
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
    for column in range(mapsize/2):
        x = random.randint(0, mapsize-1)
        y = random.randint(0, mapsize-1)
        map[(x,y)] = False

    # Generate FOV map.
    center = (mapsize/2, mapsize/2)
    fov = FOV(center, map)
    fov.calculate()

    import sys
    for y in range(mapsize):
        sys.stdout.write(" " * y)
        for x in range(mapsize):
            sys.stdout.write(" ")
            if center == (x,y):
                sys.stdout.write("@")
            elif fov.visible.get((x,y)) is True:
                if map[(x,y)] is False:
                    sys.stdout.write("T")
                else:
                    sys.stdout.write(".")
            elif fov.visible.get((x,y)) is not None:
                sys.stdout.write(fov.visible.get((x,y)))
            elif map[(x,y)] is False:
                sys.stdout.write("x")
            else:
                sys.stdout.write("~")
        sys.stdout.write("\n")
print len(fov.arcs)
