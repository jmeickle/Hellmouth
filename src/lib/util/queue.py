"""A simple singleton queue, based on collections.deque."""

from collections import deque

class Queue(object):
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
    def remove(agent):
        Queue.queue.remove(agent)