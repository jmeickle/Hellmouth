from collections import deque

class Log:
    events = deque()

def add(event):
    Log.events.append(event)

def length():
    return len(Log.events)

def events():
    return Log.events
