"""Debugging and system logging functions."""

import functools
import logging

logging.basicConfig(filename='debug.log',level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s',)

# Track how often a message has hit the debug log.
# TODO: Use this somewhere.
debug_frequency = {}

# TODO: Support setting level to info/warning
def debug(message, level=logging.DEBUG):
    msg = message.__str__()
    hits = debug_frequency.get(msg, 0) + 1
    debug_frequency[msg] = hits
    logging.debug("%s:%s" % (hits, msg))

def DEBUG(fn):
    """Decorator to log a method call to debug."""
    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        level=logging.DEBUG
        debug("method: " + fn.__name__, level)
        debug("args: " + str(args), level)
        debug("kwargs: " + str(kwargs), level)
        result = fn(self, *args, **kwargs)
        debug(result, level)
        return result
    return wrapper

debug('Imported debug.py and initialized logging.')