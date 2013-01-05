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