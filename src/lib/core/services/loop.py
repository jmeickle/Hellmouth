"""A service that contains services that react to the kernel loop."""

from src.lib.core.kernel import kernel
from src.lib.core.services.service import Service

from src.lib.util import debug
from src.lib.util.registry import RegistryList

class LoopError(Exception):
    pass

class LoopService(RegistryList, Service):
    def run(self):
        """Run an instance of the main application loop."""
        # Allow services to react to the loop.
        for service in kernel.loop:
            debug.log("Acting service: {}".format(service))
            service.react()