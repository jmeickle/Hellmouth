"""Define the geometry of hexagons.

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

from src.lib.util.geometry.shape import Shape
from src.lib.util.geometry.space import *

class Hexagon(Shape):
    """Class for hexagonal shape."""

    # Number of faces
    faces = 6

    # No location
    ANYWHERE = None

    # Center
    CC = Point(0, 0)

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

    def __init__(self, pos):
        assert False, "Tried to instantiate an abstract Hexagon."

    def __repr__(self):
        return "<%s[%s]>" % (self.__class__.__name__, self.pos)

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
    def get_face_position_from_index(cls, rank, index):
        """Return the position on the nearest face, given a rank and an index into it."""
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
        return rank * 6 - 1

    """Hexagon point methods."""

    @classmethod
    def get_pole(cls, origin=CC, rank=1, heading=NW):
        """Return the hexagon at a rank from an origin along a heading."""
        return origin + rank * heading

    """Hexagon iteration methods."""

    @classmethod
    def perimeter(cls, origin=CC, rank=1, index=0, rotation=CW_TURN):
        """Yield indexes and points for hexagons starting at an index on a rank
        and continuing indefinitely along a rotation.
        """
        max_index = cls.get_max_index(rank)
        assert index <= max_index, "Rank %s: index %s greater than max index %s" % (rank, index, max_index)
        assert rotation in (CW_TURN, CCW_TURN), "Invalid rotation value: %s" % str(rotation)

        # Determine the starting face and the position along it.
        face = cls.get_face_from_index(rank, index)
        position = cls.get_face_position_from_index(rank, index)

        # Set the coordinates to the starting face's coordinates.
        coords = cls.get_pole(origin, rank, heading=cls.headings[face])

        # Rotate the starting face by one turn clockwise.
        face = cls.rotate_face(face, CW_TURN)

        # Update the coordinates if required by the position.
        if position > 0:
            # Rotate the starting face an additional turn clockwise in order to
            # point towards the next position along the face).
            position_face = cls.rotate_face(face, CW_TURN * 2)
            position_heading = cls.headings[position_face]

            # Update the coordinates.
            coords = cls.add(coords, cls.mult(position_heading, position))

        # Flip face direction and heading if rotating counterclockwise.
        if rotation == CCW_TURN:
            face = cls.rotate_face(face, 4)
            heading = cls.headings[face]

        # Yield the initial index and coordinates.
        yield index, coords

        while True:
            # Shift index and position in the direction of rotation.
            index += rotation
            position += rotation

            # Handle index and position rollover.
            if position < 0:
                face = cls.rotate_face(face, rotation)
                heading = cls.headings[face]
                position = rank
                if index < 0:
                    index = max_index
            elif position > rank:
                face = cls.rotate_face(face, rotation)
                heading = cls.headings[face]
                position = 0
                if index > max_index:
                    index = 0
            else:
                face = cls.rotate_face(face, rotation)
                heading = cls.headings[face]

            # Add the current heading to the coordinates.
            print "heading += %s" % cls.heading_names[heading]
            coords += heading

            # Yield the current index and coordinates.
            yield index, coords

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