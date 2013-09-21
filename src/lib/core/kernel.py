"""The kernel for Unicursal, a Python roguelike framework."""

from src.lib.util.registry import RegistryContainerFactory, RegistryDict, RegistryList
from src.lib.core.services.loop import LoopService

class Kernel(object):
    def __init__(self):
        # Define a list-like container for service registration.
        ServiceList = RegistryContainerFactory("ServiceList", RegistryList)
        # Define a dict-like container for service name registration.
        ServiceNameRegistry = RegistryContainerFactory("ServiceNameRegistry", RegistryDict, container_class=ServiceList)
        # Populate the service name registry with a loop service.
        self.services = ServiceNameRegistry()
        self.register_services(loop=LoopService())

    """Execution management methods."""

    def loop(self):
        """Run the main application loop."""
        # Use the output service as a context manager.
        with self.service("output") as display:
            # Start the root Component's loop.
            root = self.service("root")
            while root.alive:
                # Allow registered services to react to the loop.
                for service in self.service("loop"):
                    service.loop()

            # Continue looping if necessary.
            if root.after_loop().get("relaunch"):
                # TODO: Reset kernel and services as needed
                return True

    """Service registration methods."""

    def register_services(self, **services):
        """Register service instances to service names."""
        for service_name, service in services.items():
            self.services[service_name] += service
            service.kernel = self
            service.add_helpers()
            # TODO: add asserts back in
            # assert service_name not in self.services,\
            #     "Failed to register service %s at service name %s: service %s already registered there."\
            #     % (service, service_name, self.services[service_name]))

    def deregister_services(self, **services):
        """Deregister service instances from service names."""
        for service_name, service in services.items():
            self.services[service_name] -= service
            service.remove_helpers()
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