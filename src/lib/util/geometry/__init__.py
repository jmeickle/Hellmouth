"""Defines primitives for working with space."""

import numpy as np

class Point(np.ndarray):
    """Points are a convenience subclass around Numpy arrays.

    The ndarray override code is lifted from this scipy tutorial:

        http://docs.scipy.org/doc/numpy/user/basics.subclassing.html
    """

    def __new__(cls, *args):
        """Return a Point initialized from the sequence of provided arguments."""
        return np.asarray(np.array(args)).view(cls)

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

# Constants for rotation and turns.
CCW_TURN = -1
NO_TURN = 0
CW_TURN = 1

# Export the Point class and constants.
__all__ = ["Point", "CCW_TURN", "NO_TURN", "CW_TURN"]