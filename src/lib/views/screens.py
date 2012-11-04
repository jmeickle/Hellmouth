# Basic full-screen classes and their methods.
import curses

from define import *
from text import *
from views.view import View

# Border, heading, body text.
class Screen(View):
    def __init__(self, window, header_left="", header_right="", body_text="", footer_text="", callback=None, arguments=None):
        View.__init__(self, window, TERM_X, TERM_Y)
        self.header_left = header_left
        self.header_right = header_right
        self.body_text = body_text
        self.footer_text = footer_text
        self.callback = callback
        self.arguments = arguments

    def before_draw(self):
        self.window.clear()

    # TODO: Function to make drawing headings a bit more generalizable
    def draw(self):
        self.border(" ")
        self.header()
        self.body()
        self.footer()
        return False

    def header(self):
        left = len(striptags(self.header_left))
        right = len(striptags(self.header_right))
        spacing = " " * (self.width - left - right)
        header_text = "%s%s%s" % (self.header_left, spacing, self.header_right)
        self.cline(header_text)
        self.cline("-"*self.width)

    def body(self):
        self.cline(self.body_text)

    def footer(self):
        y_acc = self.y_acc
        self.y_acc = self.BOTTOM
        self.cline(self.footer_text)
        self.y_acc = y_acc

    def keyin(self, c):
        if c == curses.KEY_ENTER or c == ord('\n'):
            self.do_callback()
            self.suicide()
        return False # Don't permit anything but continuing.

    def do_callback(self):
        if self.callback is not None:
            if self.arguments is not None:
                self.callback(self.arguments)
            else:
                self.callback()

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

