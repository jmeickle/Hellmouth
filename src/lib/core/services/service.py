"""Services registered to the kernel."""

class Service(object):
    """Provides methods to classes that are registered as kernel services."""

    def __repr__(self):
        """Display as `<ClassName>` when printed."""
        return "<{0}>".format(self.__class__.__name__)

    def react(self):
        """React to the kernel loop."""
        pass