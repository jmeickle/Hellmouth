"""The kernel for Unicursal, a Python roguelike framework."""

import inspect

from src.lib.util.registry import RegistryFactory, RegistryDict, RegistryList

# Define a list-like container for storing registered services.
ServiceList = RegistryFactory("ServiceList", RegistryList)
# Define a dict-like container for service registration.
ServiceRegistry = RegistryFactory("ServiceRegistry", RegistryDict, container_class=ServiceList)

class Kernel(object):
    """The Kernel is a singleton that coordinates a Unicursal application. It is
    responsible for service registration and orchestration.
    """
    def __init__(self, **services):
        # Initialize the service registry.
        self.services = ServiceRegistry()
        # Register the provided services.
        self.register_services(**services)

    """Service registration methods."""

    def register_services(self, **services):
        """Register service instances to service names."""
        for service_name, service in services.items():
            self.services[service_name] += service
            service.kernel = self
            self.add_helpers(service)
            # TODO: add asserts back in
            # assert service_name not in self.services,\
            #     "Failed to register service %s at service name %s: service %s already registered there."\
            #     % (service, service_name, self.services[service_name]))

    def deregister_services(self, **services):
        """Deregister service instances from service names."""
        for service_name, service in services.items():
            self.services[service_name] -= service
            self.remove_helpers(service)
            del service.kernel
            # TODO: add asserts back in
            # assert hasattr(self, service_name),\
            #     "Failed to deregister service at service name %s: no service is registered there."\
            #     % (service, service_name, getattr(self, service_name))

            # registered = getattr(self, service_name)

            # if service:
            #     assert service == registered,\
            #         "Failed to deregister service %s at service name %s: a different service, %s, is registered there."\
            #         % (service, service_name, getattr(self, service_name))         

            # delattr(self, service_name)
            # service.remove_helpers(self)

    """Service helper methods."""

    def service(self, service_name):
        """Return the first service registered with a service name."""
        services = self.services[service_name]
        if services:
            return services[0]
        else:
            return None

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