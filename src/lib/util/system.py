# Helper functions for interfacing with the OS.

import os
import errno

# TODO: Handle os.pardir
def makedir(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

# Get a list of directories inside of a path
def folders(path=".", pattern=None):
    for filename in os.listdir(path):
        if os.path.isdir(path + "/" + filename):
            yield filename