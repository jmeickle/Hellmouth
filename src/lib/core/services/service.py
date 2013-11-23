"""Services registered to the kernel."""

from src.lib.util.trait import Trait

class Service(Trait):
    """Provides methods to classes that are registered as kernel services."""

    def __init__(self, *args, **kwargs):
        self.kernel = None
        Trait.super(Service, self).__init__(*args, **kwargs)

    def __repr__(self):
        """Display as `<ClassName>` when printed."""
        return "<{0}>".format(self.__class__.__name__)