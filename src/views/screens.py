# Basic full-screen classes and their methods.
import curses

from define import *
from views.view import View

# Border, heading, body text.
class Screen(View):
    def __init__(self, window):
        View.__init__(self, window, TERM_X, TERM_Y)
        self.title = "Debug Title"

    def before_draw(self):
        self.window.clear()

    # TODO: Function to make drawing headings a bit more generalizable
    def draw(self):
        self.border("#")
        heading = "%s%s%s" % (self.title, " "*(self.width - len(self.title) - len(self.player.location) - 1), self.player.location)
        self.cline(heading)
        self.cline("-"*self.width)
        return False

    def keyin(self, c):
        if c == curses.KEY_ENTER or c == ord('\n'):
            self.suicide()
        return False # Don't permit anything but continuing.

# A basic 'forced' dialogue screen. You may get some options, but must continue forward.
class DialogueScreen(Screen):
    def __init__(self, window, choices=None, callback=None):
        Screen.__init__(self, window)
        self.speaker = None
        self.choices = choices
        self.callback = callback
        if self.callback is None:
            self.callback = self.suicide
        self.selector = Selector(self, choices)

    # The color to use for the speaker.
    def color(self):
        if self.speaker is not None:
            return self.speaker.dialogue_color()
        else:
            return "white-black"

    def draw(self):
        self.border(" ")
        title = "<%s>%s</>" % (self.color(), self.title)
        heading = "%s%s%s" % (title, " "*(self.width - len(self.title) - len(self.player.location)), self.player.location)
        self.cline(heading)
        self.x_acc -= 2
        self.cline("-"*(self.x))
        self.x_acc += 2
#        self.y_acc += 1
#        self.rds((0, self.y_acc), "-"*(self.x), None, None, False)
#        self.cline("-"*(self.width))
        return False

    # Since this is a 'forced' dialogue screen, you must press enter.
    def keyin(self, c):
        if c == curses.KEY_ENTER or c == ord('\n'):
            self.selector.choose()
        else:
            dir = key.hexkeys(c)
            if dir == CC:
                self.selector.jump(6)
            elif dir is not None:
                self.selector.jump(rotation[dir])

        return False # Don't permit anything but continuing.

