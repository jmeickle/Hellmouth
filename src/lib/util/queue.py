"""A simple singleton queue, based on collections.deque."""

from collections import deque

class QueueMetaclass(type):
    def __repr__(self):
        return "\n".join(Queue.get_view_data())

class Queue(object):
    __metaclass__ = QueueMetaclass
    queue = deque()

    @staticmethod
    def get_acting():
        if Queue.queue:
            return Queue.queue[0]

    @staticmethod
    def get_all_controlled():
        for actor in Queue.queue:
            if actor.controlled:
                yield actor

    @staticmethod
    def get_next_controlled():
        for actor in Queue.queue:
            if actor.controlled:
                return actor

    @staticmethod
    def next():
        Queue.queue.rotate()

    @staticmethod
    def add(agent):
        Queue.queue.append(agent)

    @staticmethod
    def addleft(agent):
        Queue.queue.appendleft(agent)

    @staticmethod
    def remove(agent):
        Queue.queue.remove(agent)

    @staticmethod
    def clear():
        Queue.queue = deque()

    @staticmethod
    def get_view_data():
        for index in range(len(Queue.queue)):
            yield "%s: %s" % (index, Queue.queue[index])