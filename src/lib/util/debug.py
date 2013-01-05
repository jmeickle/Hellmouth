# Debugging and system logging functions.

import logging

logging.basicConfig(filename='hellmouth.log',level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s',)

# TODO: Use this somewhere.
debug_frequency = {}

# TODO: Support setting level to info/warning
def DEBUG(message, level=logging.DEBUG):
    hits = debug_frequency.get(message, 0) + 1
    debug_frequency[message] = hits
    logging.debug("%s:%s" % (hits, message))

DEBUG('Imported debug.py and initialized logging.')