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
        # List of cell ranks; list of cells in a rank; tuple of pos, vertices.
        self.cells = [setup_vertices([self.center])]
        self.cells.append(setup_vertices(fov_perimeter(1, self.center)))
        vertices = self.cells[0][0][1]
        # Starting arcs.
        self.arcs = []
        self.arcs.append(Arc(self, 0, 1, (vertices[0][0], self.center[1]), (self.center[0], vertices[2][1])))
#        self.arcs.append(Arc(self, 2, 3, (self.center[0], vertices[2][1]), (vertices[3][0], self.center[1])))
#        self.arcs.append(Arc(self, 0, 1, (vertices[0][0], self.center[1]), (self.center[0], vertices[2][1])))
#      alist = new Arc(0,hc.x[0],hc.cy,1,hc.cx,hc.y[2]);
#      alist.next = new Arc(2,hc.cx,hc.y[2],3,hc.x[3],hc.cy);
#      alist.next.next = new Arc(3,hc.x[3],hc.cy,4,hc.cx,hc.y[5]);
#      alist.next.next.next = new Arc(5,hc.cx,hc.y[5],6,hc.x[0],hc.cy);

#        self.arcs.append(Arc(self, 0, 1, (1,0), (0,1)))
#vertices[0], vertices[1]))
#        self.arcs.append(Arc(self, 0, 1, vertices[1], vertices[0]))
#        self.arcs.append(Arc(self, 0, 1, vertices[3], vertices[1]))
#        self.arcs.append(Arc(self, 1, 2, vertices[1], vertices[3]))
#        self.arcs.append(Arc(self, 2, 3, vertices[1], vertices[0]))
        # Visible cells.
        self.visible = {}

    # Calculate the next set of arcs.
    def calculate(self, rank=1):
        # Generate the vertices for the next rank.
        self.cells.append(setup_vertices(fov_perimeter(rank+1, self.center)))

        # All hexes at the current rank are marked as visible.
        for arc in self.arcs:
            for index in range(arc.start, arc.stop+1):
                pos, vertices = self.cells[rank][index]
                if pos not in self.visible:
                    self.visible[pos] = True

#        self.cells.append(setup_vertices(fov_perimeter(rank+1, self.center)))
        remaining_arcs = []
        for arc in self.arcs:
            remaining_arcs.extend(arc.split(rank))
        self.arcs = remaining_arcs

        for arc in self.arcs:
            arc.expand(rank)

        # Debug.
        if self.arcs and rank < 10:
            self.calculate(rank+1)

class Arc:
    def __init__(self, parent, start, stop, cw, ccw):
        self.parent = parent # Parent hexagon
        self.center = self.parent.center # Point the arc is centered at
        self.start = start # Starting hexagon index.
        self.stop = stop # Stopping hexagon index.
        self.cw = cw # Clockwise arm.
        self.ccw = ccw # Counterclockwise arm.

    def expand(self, rank):
        # Which general face of the hex.
        face = self.start / rank #(max(rank, 1))
        # Which position along that face.
        position = self.start % rank #(max(rank, 1))

        # Limit maximum size of arcs.
        if position == 0 and (face == 0 or face == 3):
            start = face * (rank+1)
        else:
            start = face * (rank+1) + position + 1

        if self.ccw[1] <= self.center[1] and self.cw[1] <= self.center[1]:
            while (start > 0):
                pos, vertices = self.parent.cells[rank+1][start-1]
                if arc_side(self.center, self.cw, vertices, RIGHT) is False:
                    break
                start -= 1
        else:
            while start > (rank+1)*3:
                pos, vertices = self.parent.cells[rank+1][start-1]
                if arc_side(self.center, self.cw, vertices, RIGHT) is False:
                    break
                start -= 1

        face = self.stop / rank
        position = self.stop % rank

        if position == 0 and (face == 0 or face == 3):
            stop = face * (rank+1)
        else:
            stop = face * (rank+1) + position - 1

        if self.ccw[1] <= self.center[1] and self.cw[1] <= self.center[1]:
            while stop < (rank+1) * 3:
                if stop >= len(self.parent.cells[rank+1]):
                    exit("%s" % stop)
                pos, vertices = self.parent.cells[rank+1][stop+1]
                if arc_side(self.center, self.ccw, vertices, LEFT) is False:
                    break
                stop += 1
        else:
            while stop < (rank+1) * 6:
                pos, vertices = self.parent.cells[rank+1][stop+1]
                if arc_side(self.center, self.ccw, vertices, LEFT) is False:
                    break
                stop += 1

        self.start = start
        self.stop = stop

    def split(self, rank):
        arcs = []
        while self.start <= self.stop:
#for index in range(self.start, self.stop+1):
#            if index >= len(self.parent.cells[rank]):
#                exit("%s, %s, %s" % (len(self.parent.cells[rank]), self.start, self.stop))
            pos, vertices = self.parent.cells[rank][self.start]
            clear = self.parent.map.get(pos)
            if clear is True:
                self.parent.visible[pos] = True
                break
            else:
                self.contractCW(vertices)
#                self.parent.visible[pos] = "o"
                self.start += 1

        while self.stop >= self.start:
            pos, vertices = self.parent.cells[rank][self.stop]
            clear = self.parent.map.get(pos)
            if clear is True:
                self.parent.visible[pos] = True
                break
            else:
                self.contractCCW(vertices)
#                self.parent.visible[pos] = "e"
                self.stop -= 1

        # Arc doesn't contain anything; abort.
        if self.is_empty() is True:
            return arcs

#        exit()
        # Handle an obstacle that splits an arc in two (or more).      
        for index in range(self.start+1, self.stop):
            pos, vertices = self.parent.cells[rank][index]
            clear = self.parent.map.get(pos)
            if clear is True:
                continue
            else:
                # Create a child.
#                self.parent.visible[pos] = "!"
                child = Arc(self.parent, index+1, self.stop, vertices[0], self.ccw)
                self.stop = index - 1
                child.contractCW(vertices)
                self.contractCCW(vertices)
                # Return the arcs potentially split off from our child.
                if child.is_empty() is False:
                    arcs.extend(child.split(rank))

        # Return ourself too if we're not empty.
        if self.is_empty() is False:
            arcs.append(self)

        return arcs

    # Contract an arc in the CW direction.
    def contractCW(self, vertices):
        best_cw = self.cw
        for index in range(6):
            if turns(self.center, best_cw, vertices[index]) == RIGHT:
                best_cw = vertices[index]
        self.cw = best_cw
        arclist[(self, self.cw)] = True

    # Contract an arc in the CCW direction.
    def contractCCW(self, vertices):
        best_ccw = self.ccw
        for index in range(6):
            if turns(self.center, best_ccw, vertices[index]) == LEFT:
                best_ccw = vertices[index]
        self.cw = best_ccw
        arclist[(self, self.ccw)] = True

    # Determine whether an arc is empty.
    def is_empty(self):
        return False
        if self.start > self.stop:
            return True
        if turns(self.center, self.cw, self.ccw) != RIGHT:
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
    fov.calculate(1)

    import sys
    for y in range(mapsize):
        sys.stdout.write(" " * y)
        for x in range(mapsize):
            sys.stdout.write(" ")
            if center == (x,y):
                sys.stdout.write("@")
            elif fov.visible.get((x,y)) is True:
                # Visible and blocks something.
                if map[(x,y)] is False:
                    sys.stdout.write("!")
                # Visible and clear.
                else:
                    sys.stdout.write(".")
            # Visible, but...
            elif fov.visible.get((x,y)) is not None:
                sys.stdout.write(fov.visible.get((x,y)))
            # Not visible.
            else:
                if map[(x,y)] is False:
                    sys.stdout.write(",")
                else:
                    sys.stdout.write(" ")
        sys.stdout.write("\n")
