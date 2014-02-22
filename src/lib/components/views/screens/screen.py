# Basic full-screen classes and their methods.
import curses

from src.lib.util.define import *
from src.lib.util.text import *

from src.lib.components.input import *
from src.lib.components.views.view import View

# Border, heading, body text.
class Screen(View):
    default_arguments = {
        "x" : TERM_X,
        "y" : TERM_Y
    }

    @override_defaults
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

        self.title = kwargs.get("title", "")
        self.header_left = kwargs.get("header_left", "")
        self.header_right = kwargs.get("header_right", "")
        self.body_text = kwargs.get("body_text", "")
        self.footer_text = kwargs.get("footer_text", "")
        self.callback = kwargs.get("callback", self.suicide)
        self.arguments = kwargs.get("arguments", None)

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
        else: return True
        return False

    def do_callback(self):
        if self.callback is not None:
            if self.arguments is not None:
                self.callback(self.arguments)
            else:
                self.callback()

# A basic menu screen. You have some options and must choose one of them.
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.choices = kwargs.get("choices", [])
        self.choice_formatter = kwargs.get("choice_formatter", lambda choice: choice)

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

        for index, choice in enumerate(self.choices):
            if index == self.selector.index:
                self.cline(self.choice_formatter(choice), "green-black")
            else:
                self.cline(self.choice_formatter(choice))

    def keyin(self, c):
        if c == curses.KEY_ENTER or c == ord('\n'):
            self.suicide()
            self.callback(self.choices[self.selector.index])
        else: return True
        return False

# A basic 'forced' dialogue screen. You may get some options, but must continue forward.
class DialogueScreen(Screen):
    def __init__(self, **kwargs):
        super(DialogueScreen, self).__init__(**kwargs)
        self.speaker = None
        self.choices = kwargs.pop("choices", [])
        self.callback = kwargs.pop("callback", self.suicide)
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

    # Since this is a 'forced' dialogue screen, you must press enter.
    def keyin(self, c):
        if c == curses.KEY_ENTER or c == ord('\n'):
            self.selector.choose()
        return False