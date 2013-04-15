# Basic full-screen classes and their methods.
import curses

from src.lib.util.define import *
from src.lib.util import key
from src.lib.util.text import *
from src.lib.components.input import *
from src.lib.components.views.view import View

# Border, heading, body text.
class Screen(View):
    def __init__(self, window, **args):
        View.__init__(self, window, TERM_X, TERM_Y)

        self.title = args.get("title", "")       
        self.header_left = args.get("header_left", "")
        self.header_right = args.get("header_right", "")
        self.body_text = args.get("body_text", "")
        self.footer_text = args.get("footer_text", "")
        self.callback = args.get("callback", self.suicide)
        self.arguments = args.get("arguments", None)

    def before_draw(self):
        self.window.clear()

    # Reasonable default color.
    def color(self):
            return "white-black"

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

# A basic menu screen. You have some options and must choose one of them.
class MenuScreen(Screen):
    def __init__(self, window, **args):
        Screen.__init__(self, window, **args)
        self.choices = args.get("choices", [])
        self.selector = Scroller(len(self.choices) - 1)
        self.spawn(self.selector)

    def color(self):
        return "green-black"

    def draw(self):
        self.border(" ")
        title = "<%s>%s</>" % (self.color(), self.title)
        padding = (self.width - len(self.title))/2
        heading = "%s%s%s" % (" "*padding, title, " "*padding)
        self.cline(heading)
        self.x_acc -= 2
        self.cline("-"*(self.x))
        self.x_acc += 2

        for x in range(len(self.choices)):
            module_name, module_info = self.choices[x]
            if x == self.selector.index:
                self.cline(module_info.name, "green-black")
            else:
                self.cline(module_info.name)
        return False

    def keyin(self, c):
        if c == curses.KEY_ENTER or c == ord('\n'):
            self.suicide()
            self.callback(self.choices[self.selector.index])
        # Don't permit anything but continuing.
        return False

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
        heading = "%s%s%s" % (title, " "*(self.width - len(self.title) - len(self.get_controller().location)), self.get_controller().location)
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

