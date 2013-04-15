"""Operating system interface helper methods."""

import os
import errno

def makedir(path):
    """Make a path, raising any exceptions except the path already existing."""
    # TODO: Handle os.pardir
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def folders(path=".", pattern=None):
    """Get a list of directories inside of a path"""
    for filename in os.listdir(path):
        if os.path.isdir(path + "/" + filename):
            yield filename