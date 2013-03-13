from collections import deque

class Queue(object):
    queue = deque()

    @staticmethod
    def get_acting():
        if Queue.queue:
            return Queue.queue[0]

    @staticmethod
    def next():
        Queue.queue.rotate()

    @staticmethod
    def add(agent):
        Queue.queue.append(agent)

    @staticmethod
    def remove(agent):
        Queue.queue.remove(agent)