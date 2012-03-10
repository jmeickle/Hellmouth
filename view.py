class Component():

    def __init__(self, window, x=0, y=0):
        self.window = window
        self.x = x
        self.y = y

class MainMap(Component):
    def __init__(self, window, x, y):
        Component.__init__(self, window, x, y)
        self.map = None
        self.actors = []

    def add(self, actor):
        self.actors.append(actor)

    def draw(self):
        for actor in self.actors:
            self.window.addch(actor.y, actor.x, actor.glyph)
#class MiniMap(Component):

#class Stats:
#    def 
