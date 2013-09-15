"""Define primitives for working with configurations of points.

This module expands the terminology guide in `src.lib.util.geometry.space` with
some definitions specific to shapes:

_vertex_: A point that acts as one of the shape's 'corners'.

_edge_: A line segment that connects two adjacent vertices.

_face_: A lower-dimension shape that acts as one of the shape's 'sides'. On a 
plane, this is equivalent to an edge. In a space, this is equivalent to an area.
"""

class Shape(object):
    """An abstract shape."""
    pass