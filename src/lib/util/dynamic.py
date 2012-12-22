# Dynamic programming functions.

import inspect

# Return the name of the current function.
def me():
    return inspect.stack()[1][3]

# Return the name of the calling function.
def caller():
    return inspect.stack()[2][3]
