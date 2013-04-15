"""Mathematical helper methods."""

def signum(int, zero=False):
    """Return the sign of a number."""
    if int < 0:
        return -1
    elif int == 0 and zero is True:
        return 0
    else:
        return 1