"""A service that contacts other services during the event loop."""

from src.lib.core.kernel import Kernel
from src.lib.core.services.service import Service
from src.lib.util.registry import RegistryList

class LoopService(RegistryList):
    @Kernel.helper
    def loop(kernel):
        """Run the main application loop."""
        # Use the output service as a context manager.
        with kernel.service("output") as display:
            # Start the root Component's loop.
            root = kernel.service("root")
            while root.alive:
                # Allow registered services to react to the loop.
                for service in kernel.service("loop"):
                    if hasattr(service, "loop"):
                        service.loop()

            # Continue looping if necessary.
            if root.after_loop().get("relaunch"):
                # TODO: Reset kernel and services as needed
                return True