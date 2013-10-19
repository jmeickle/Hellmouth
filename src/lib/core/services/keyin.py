"""A queue of keypresses."""

from Queue import Queue

from src.lib.core.services.service import ServiceMixin

class KeyinService(Queue, ServiceMixin):
    pass