"""Debugging and system logging methods and decorators."""

import functools
import logging

logging.basicConfig(filename='debug.log',level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s',)

# Track how often a message has hit the debug log.
# TODO: Use this somewhere.
debug_frequency = {}

# TODO: Support setting level to info/warning
def log(message, **kwargs):
    """Send a message to the debug log."""
    level = kwargs.pop("level", logging.DEBUG)
    msg = message.__str__()
    if kwargs.pop("line", False):
        import inspect
        last_call = inspect.stack()[1]
        _, module, line, method, _, _ = last_call
        msg = "{}({}) in {}: {}".format(module.partition("src")[2], line, method, msg)
    hits = debug_frequency.get(msg, 0) + 1
    debug_frequency[msg] = hits
    logging.log(level, "%s:%s" % (hits, msg))

def die(message, **kwargs):
    """Send a message to the debug log and then assert."""
    kwargs.setdefault("level", logging.CRITICAL)
    log(message, **kwargs)
    assert False, "\n{}".format(message)

def lineno():
    """Returns the current line number."""
    return inspect.currentframe().f_back.f_lineno

def DEBUG(fn):
    """Decorator to log a method call to debug."""
    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        level=logging.DEBUG
        log("method: " + fn.__name__, level)
        log("args: " + str(args), level)
        log("kwargs: " + str(kwargs), level)
        result = fn(self, *args, **kwargs)
        log(result, level)
        return result
    return wrapper

log('Imported debug.py and initialized logging.')