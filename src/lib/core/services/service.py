"""Services registered to the kernel."""

class ServiceMixin(object):
    """Mixin for classes that are registered to the kernel as a service."""

    def __init__(self, *args, **kwargs):
        self.kernel = None
        super(ServiceMixin, self).__init__(*args, **kwargs)

    def __repr__(self):
        """Display as `<ClassName>` when printed."""
        return "<{0}>".format(self.__class__.__name__)