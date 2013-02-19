from collections import deque

class Log:
    events = deque()

    @classmethod
    def add(cls, event):
        cls.events.append(event)

    @classmethod
    def length(cls):
        return len(cls.events)