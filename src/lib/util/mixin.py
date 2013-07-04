"""Defines a minimal base class for Mixins."""

"""Usage note: if a Mixin has a prefix like "Un", retain the capitalization of
the prefixed Mixin. For example, `StoreMixin` should become `UnStoreMixin`.
This permits more convenient references between these classes.
"""

import abc

class Mixin(object):
    """Minimal base class for Python multiple inheritance using Mixins."""
    __metaclass__ = abc.ABCMeta

class DebugMixin(Mixin):
    """Debug Mixin, checked against when enabling debug-only functionality."""
    pass