"""A service that contacts other services during the event loop."""

from src.lib.core.services.service import ServiceMixin
from src.lib.util.registry import RegistryList

class LoopService(RegistryList, ServiceMixin):
    pass