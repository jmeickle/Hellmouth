"""Debugging and system logging methods and decorators."""

import functools
import inspect
import logging

logging.basicConfig(filename='debug.log',level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s',)

# Track how often a message has hit the debug log.
# TODO: Use this somewhere.
debug_frequency = {}

def describe_call(skip_calls=1):
    """Given a number of calls on the stack to skip, return a previous call's
    module, method, and line number.
    """
    call = inspect.stack()[skip_calls+1]
    _, module, line, method, _, _ = call
    return module.rpartition("src")[2], method, line

# TODO: Support setting level to info/warning
def log(message, **kwargs):
    """Send a message to the debug log."""
    level = kwargs.pop("level", logging.DEBUG)
    msg = message.__str__()
    if kwargs.pop("line", True):
        module, method, line = describe_call(1)
        msg = "{}({}) in {}: {}".format(module, line, method, msg)
    hits = debug_frequency.get(msg, 0) + 1
    debug_frequency[msg] = hits
    logging.log(level, "%s:%s" % (hits, msg))

def die(message, **kwargs):
    """Send a message to the debug log and then assert."""
    kwargs.setdefault("level", logging.CRITICAL)
    log(message, **kwargs)
    assert False, "\n{}".format(message)

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