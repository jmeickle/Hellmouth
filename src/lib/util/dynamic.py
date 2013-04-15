"""Dynamic programming functions."""

import inspect

def me():
    """Return the name of the current function."""
    return inspect.stack()[1][3]

def caller():
    """Return the name of the calling function."""
    return inspect.stack()[2][3]