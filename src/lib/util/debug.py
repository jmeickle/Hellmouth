# Debugging and system logging functions.

import logging

logging.basicConfig(filename='debug.log',level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s',)

# TODO: Use this somewhere.
debug_frequency = {}

# TODO: Support setting level to info/warning
def DEBUG(message, level=logging.DEBUG):
    msg = message.__str__()
    hits = debug_frequency.get(msg, 0) + 1
    debug_frequency[msg] = hits
    logging.debug("%s:%s" % (hits, msg))

DEBUG('Imported debug.py and initialized logging.')