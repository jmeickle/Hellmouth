"""Services registered to the kernel."""

class ServiceMixin(object):
    """Mixin for classes that are registered to the kernel as a service."""
    helpers = []

    def __init__(self, *args, **kwargs):
        self.kernel = None
        super(ServiceMixin, self).__init__(*args, **kwargs)

    def __repr__(self):
        """Display as `<ClassName>` when printed."""
        return "<{0}>".format(self.__class__.__name__)

    def add_helpers(self):
        """Add helper functions to the kernel."""
        pass

    def remove_helpers(self):
        """Remove helper functions from the kernel."""
        pass

    def loop(self):
        pass

    @classmethod
    def helper(cls, f, **options):
        cls.helpers.append(f)
        return f