"""The kernel for Unicursal, a Python roguelike framework."""

import inspect

from src.lib.core.services.service import Service

from src.lib.util.pattern import Singleton
from src.lib.util.registry import RegistryFactory, RegistryDict, RegistryList
from src.lib.util.trait import Traitable, Trait

# Define a list-like container for storing registered services.
ServiceList = RegistryFactory("ServiceList", RegistryList)
# Define a dict-like container for service registration.
ServiceRegistry = RegistryFactory("ServiceRegistry", RegistryDict, container_class=ServiceList)

class KernelError(Exception):
    pass

@Trait.use(Singleton)
class Kernel(object):
    """The Kernel is a singleton that coordinates a Unicursal application. It is
    responsible for service registration and orchestration.
    """
    __metaclass__ = Traitable

    def __setattr__(self, name, value):
        if not isinstance(value, Service):
            raise KernelError("Attempted to set a non-service ({}) as an attribute ({}) on the kernel.".format(value, name))
        else:
            self.add_helpers(value)
            super(Kernel, self).__setattr__(name, value)

    """Service helper methods."""

    @staticmethod
    def helper(f):
        """Mark as a Kernel helper method."""
        f.__helper__ = True
        return f

    def add_helpers(self, service):
        """Add a service's helper functions to the Kernel."""
        for name, member in inspect.getmembers(service):
            if name[0] != "_" and getattr(member, "__helper__", False):
                setattr(self, name, getattr(member, "im_func", member).__get__(self, Kernel))

    def remove_helpers(self, service):
        """Remove a service's helper functions from the Kernel."""
        for name, member in inspect.getmembers(service):
            if name[0] != "_" and getattr(member, "__helper__", False):
                delattr(self, name)