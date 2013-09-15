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

class Point(numpy.ndarray):
    """Points are a convenience subclass around Numpy arrays.

    The ndarray override code is lifted from this scipy tutorial:

        http://docs.scipy.org/doc/numpy/user/basics.subclassing.html
    """

    def __new__(cls, *args):
        """Return a Point initialized from the sequence of provided arguments."""
        return numpy.asarray(numpy.array(args)).view(cls)

    def __eq__(self, other):
        return numpy.array_equal(self, other)

    def __ne__(self, other):
        return not numpy.array_equal(self, other)

    @property
    def x(self):
        """Return the first coordinate."""
        return self[0]

    @property
    def y(self):
        """Return the second coordinate."""
        return self[1]

    @property
    def z(self):
        """Return the third coordinate."""
        return self[2]

# Constants for rotations and turns.
CCW_TURN = -1
NO_TURN = 0
CW_TURN = 1