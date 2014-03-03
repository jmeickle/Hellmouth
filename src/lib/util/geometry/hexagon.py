"""Define the geometry of hexagons and hexagonal grids.

This module expands the terminology guides in `src.lib.util.geometry.space`
and `src.lib.util.geometry.shape` with some definitions specific to hexagons:

_heading_: One of the six cardinal hexagonal directions. These are represented
as the points at a distance of 1 from the coordinate system's origin (0, 0):

       NW    NE
         /  \
     CW | CC | CE
         \  /
       SW    SE

_rank_: The 'radius' of a set of hexagons. Given a set of hexagons and an origin
within it, the rank is the greatest distance observed.

_pole_: Given an origin, rank, and heading, the hexagon that would be reached by
traveling along a heading until reaching that rank.

_index_: Given an origin, rank, heading, and rotation, an enumeration of the
order in which hexagons at that rank are visited.
"""
#                               vertex 1
#           /.\                  / \
# y-axis   / . \                /   \
#   \\    /  .  \              /     \
#   ||   /   .   \ (3,-3)     /       \  edge 1
#    \\ /    .    *          /         \
#     \\     .     \        /           \
#     ||     .      \      /             \
#    / \\    .       \    /               \
#   /   \\   .        \  /                 \
#  /.   ||   .       (2,-4)                 \ vertex 2
#  |  .  \\  .    .    ||                   |
#  |    . \\ .  .      ||                   | 
#  |      .||..        ||                   |  edge 2
# ===========O========(0,3)=======O=========|==
#  |       (0,0)       ||       (0,6)       |  x-axis
#  |      .  .\\.      ||                   |
#  |    .    . \\ .    ||                   |
#  |  .      .  ||  .  ||                   |
#  |.        .  \\    (2,2)                 |
#  \     *   .   \\    /\                   / vertex 3
#   \ (-2,2) .   ||   /  \                 /
#    \       .   \\  /    \               /
#     \      .    \\/      \             /
#      \     .    ||        \           /
#       \    .    \\         \         /   edge 3
#        \   .   / \\         \       /
#         \  .  /  ||          \     /
#          \ . /   \\           \   /
#           \./     \\           \ /

from src.lib.util import debug
from src.lib.util.geometry.shape import Shape
from src.lib.util.geometry.space import Point, CCW_TURN, NO_TURN, CW_TURN
from src.lib.util.math import signum

class Hexagon(Shape):
    """Class for hexagonal shape."""

    # Basic definitions
    faces = 6
    vertices = 6

    # Hexagonal grid points

    # No location
    ANYWHERE = None

    # Center
    CC = Point(0, 0)

    # Hexagonal grid headings

    # Northwest
    NW = Point(0, -1)
    # Northeast
    NE = Point(1, -1)
    # East
    CE = Point(1, 0)
    # Southeast
    SE = Point(0, 1)
    # Southwest
    SW = Point(-1, 1)
    # West
    CW = Point(-1, 0)

    # List of headings
    headings = [NW, NE, CE, SE, SW, CW]
    heading_names = {
        NW: "Northwest",
        NE: "Northeast",
        CE: "East",
        SE: "Southeast",
        SW: "Southwest",
        CW: "West"
    }

    # TODO: The right place for this is probably a HexKeyboardLayout class or something.
    command_headings = {
        "move northwest": NW,
        "move west": CW,
        "move southwest": SW,
        "move northeast": NE,
        "move east": CE,
        "move southeast": SE,
        "wait": CC
    }

    # Offset directions, for rendering.

    # North
    NN = Point(0, -1)
    # "Half" east
    EE = Point(1, 0)
    # South
    SS = Point(0, 1)
    # "Half" west
    WW = Point(-1, 0)

    # List of offsets
    offsets = [NN, EE, SS, WW]

    def __init__(self, pos):
        assert False, "Tried to instantiate an abstract Hexagon."

    def __repr__(self):
        return "<%s[%s]>" % (self.__class__.__name__, self.pos)

    """Hexagon coordinate methods."""

    @classmethod
    def distance(cls, coords_1, coords_2):
        """Return the distance between two hexagonal coordinates."""
        dx = coords_1.x - coords_2.x
        dy = coords_1.y - coords_2.y
        return max(abs(dx), abs(dy)) if signum(dx) != signum(dy) else abs(dx) + abs(dy)

    """Hexagon face methods."""

    @classmethod
    def get_face_from_heading(cls, heading):
        """Return the face associated with a heading."""
        return headings.index(heading)

    @classmethod
    def get_face_from_index(cls, rank, index):
        """Return the nearest face, given a rank and an index into it."""
        return index / rank

    @classmethod
    def get_position_from_index(cls, rank, index):
        """Return the counterclockwise position along the nearest face, given a rank and an index into it."""
        return index % rank

    @classmethod
    def rotate_face(cls, face, rotation):
        """Return a face rotated from a starting face."""
        return (face + rotation) % 6

    """Hexagon heading methods."""

    @classmethod
    def get_heading_from_face(cls, face):
        """Return the heading associated with a face."""
        return headings[face]

    # @classmethod
    # def rotate_heading(heading, rotation):
    #     """Return a heading rotated from a starting heading."""
    #     # Can't rotate CC, ANYWHERE, etc.
    #     if heading not in headings:
    #         return heading
    #     else:
    #         face = Hexagon.get_face(heading)

    #         Hexagon.rotate_face(face, rotation)

    #         rotation[heading]

    # end = (start+turns) % 6
    # return dirs[end]

    # def flip_heading(heading):
    #     """Convenience method to rotate a heading 180 degrees (3 rotations)."""
    #     return Hexagon.rotate_heading(heading, 3)

    """Hexagon index methods."""

    @classmethod
    def get_max_index(cls, rank):
        """Return the maximum index for a rank."""
        return rank * 6 - 1 if rank > 0 else 0

    """Hexagon point methods."""

    @classmethod
    def get_pole(cls, origin=CC, rank=1, heading=NW):
        """Return the hexagon at a rank from an origin along a heading."""
        return origin + rank * heading

    """Hexagon iteration methods."""

    @classmethod
    def perimeter(cls, origin=CC, rank=1):
        if rank == 0:
            yield 0, origin
            return

        index = 0
        coords = cls.get_pole(origin, rank)
        heading = cls.CE

        for heading in cls.headings[2:] + cls.headings[:2]:
            for i in range(rank):
                yield index, coords
                index += 1
                coords += heading

    @classmethod
    def area(cls, origin=CC, max_rank=1):
        """Yield rank, index, and coordinates for hexagons out to a maximum rank
        around an origin.
        """
        assert isinstance(origin, Point), "Tried to start an area from a non-Point: {}".format(origin)
        for rank in xrange(max_rank+1):
            for index, coords in cls.perimeter(origin=origin, rank=rank):
                yield rank, index, coords

    # def get_vertices(self):
    #     """Return the vertices of a cls."""
    #     for offset in vertex_positions:
    #         yield cls.add(self.pos6, offset)

class HexagonalSpace(object):
    """A plane tessellated with hexagons."""
    # The number of coordinates required to specify a position in this space.
    dimension = 2
    # Hexagons regularly tessellate a plane.
    regular = True

    def __init__(self):
        pass

class Hexagon_Test:
    def setUp(self):
        self.hexagon = Hexagon

    def tearDown(self):
        del self.hexagon

    def cycle_test(self):
        import itertools

        def cycle_test_cases():
            print "Origin, rank 1, index 0, clockwise"
            test1 = list(enumerate(Hexagon.headings))
            yield test1, Hexagon.cycle()

            print "Origin, rank 1, index 0, counterclockwise"
            test2 = [test1[-i] for i in xrange(6)]
            yield test2, Hexagon.cycle(rotation=CCW_TURN)

            # STUB: Non-origin, rank 5, index 6, clockwise

            # STUB: Origin, rank 5, index 13, counterclockwise

        for test in cycle_test_cases():
            for expected, observed in itertools.izip(*test):
                print "    ", expected, observed
                assert expected == observed