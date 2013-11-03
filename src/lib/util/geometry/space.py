"""Define primitives for working with space.

Basic terminology:

_metric space_: "In mathematics, a metric space is a set where a notion of 
distance (called a metric) between elements of the set is defined." (WP)

_coordinate_: A value that describes positioning within a metric space.

_point_: A sequence of coordinates that uniquely identifies a position in a 
metric space.

_dimension_: The number of coordinates required to specify a point within a 
given metric space.

_distance_: The value of a metric given two points in a metric space.

_plane_: A metric space with two dimensions.

_area_: A bounded region in a plane.

_space_: A metric space with three dimensions.

_volume_: A bounded region in a space.
"""

import numpy

class Point(tuple):
    """A `Point` is a sequence of coordinates that supports some vector-like
    operations that tuples do not, such as multiplication and pairwise addition.
    """

    __slots__ = []

    def __new__(cls, *args):
        """Override __new__ to permit initialization as `Point(x, y, z, ...)`."""
        return super(Point, cls).__new__(cls, args)

    def __add__(self, other):
        """Override addition to permit pairwise addition of `Point`s."""
        assert isinstance(other, Point), "Attempted to add a non-`Point` {} to a `Point` {}.".format(other, self)
        assert len(self) == len(other), "Attempted pairwise addition of `Point`s with different lengths."
        return Point(tuple(s+o for s, o in zip(self, other)))

    def __sub__(self, other):
        """Override subtraction to permit pairwise subtraction of `Point`s."""
        assert isinstance(other, Point), "Attempted to subtract a non-`Point` {} from a `Point` {}.".format(other, self)
        assert len(self) == len(other), "Attempted pairwise subtraction of `Point`s with different lengths."
        return Point(tuple(s-o for s, o in zip(self, other)))

    def __repr__(self):
        """Display `Point`s as `<Point(x, y, z, ...)>`."""
        return "<%s%s>" % (self.__class__.__name__, tuple(self))

    @property
    def x(self):
        """Return this `Point`'s first coordinate."""
        return self[0]

    @property
    def y(self):
        """Return this `Point`'s second coordinate."""
        return self[1]

    @property
    def z(self):
        """Return this `Point`'s third coordinate."""
        return self[2]

class NumpyPoint(numpy.ndarray):
    """`NumpyPoint`s are a convenience subclass around Numpy arrays.

    The ndarray override code is lifted from this scipy tutorial:

        http://docs.scipy.org/doc/numpy/user/basics.subclassing.html
    """

    def __new__(cls, *args):
        """Return a `NumpyPoint` initialized from the sequence of provided arguments."""
        return numpy.asarray(numpy.array(args)).reshape((len(args), 1)).view(cls)

    def __eq__(self, other):
        return numpy.array_equal(self, other)

    def __ne__(self, other):
        return not numpy.array_equal(self, other)

    def __repr__(self):
        """Display `NumpyPoint`s as `<NumpyPoint(x, y, z, ...)>`."""
        return "<%s%s>" % (self.__class__.__name__, self.coordinates)

    @property
    def coordinates(self):
        """Return all of this `NumpyPoint`'s coordinates as a tuple."""
        return tuple(self.flat)

    @property
    def x(self):
        """Return this `NumpyPoint`'s first coordinate."""
        return self[0]

    @property
    def y(self):
        """Return this `NumpyPoint`'s second coordinate."""
        return self[1]

    @property
    def z(self):
        """Return this `NumpyPoint`'s third coordinate."""
        return self[2]

# Constants for rotations and turns.
CCW_TURN = -1
NO_TURN = 0
CW_TURN = 1