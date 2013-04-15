"""A simple singleton logger, based on collections.deque."""

from collections import deque

class Log(object):
    events = deque()

    @classmethod
    def add(cls, event):
        cls.events.append(event)

    @classmethod
    def length(cls):
        return len(cls.events)