# Basic full-screen classes and their methods.

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
    def draw(self, display):
        display.border(self, " ")
        self.header(display)
        self.body(display)
        self.footer(display)

    def header(self, display):
        left = len(striptags(self.header_left))
        right = len(striptags(self.header_right))
        spacing = " " * (self.width - left - right)
        header_text = "%s%s%s" % (self.header_left, spacing, self.header_right)
        display.cline(self, header_text)
        display.cline(self, "-"*self.width)

    def body(self, display):
        display.cline(self, self.body_text)

    def footer(self, display):
        y_acc = self.y_acc
        self.y_acc = self.bottom
        display.cline(self, self.footer_text)
        self.y_acc = y_acc

    def process(self, command):
        if command("cancel", "confirm"):
            self.callback()
            command.done()

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

    def draw(self, layer):
        layer.border(self, "!")
        title = "<%s>%s</>" % (self.color(), self.title)
        padding = (self.width - len(self.title))/2
        heading = "%s%s%s" % (" "*padding, title, " "*padding)
        layer.cline(self, heading)
        self.x_acc -= 2
        layer.cline(self, "-"*(self.x))
        self.x_acc += 2

        self.y_acc = 5
        self.x_acc = 5

        for index, choice in enumerate(self.choices):
            if index == self.selector.index:
                layer.cline(self, self.choice_formatter(choice), "green-black")
            else:
                layer.cline(self, self.choice_formatter(choice))

    def process(self, command):
        if command("confirm", "cancel"):
            self.callback(self.choices[self.selector.index])
            self.suicide()
            command.done()

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

    def draw(self, display):
        display.border(self, " ")
        title = "<%s>%s</>" % (self.color(), self.title)
        heading = "%s%s%s" % (title, " "*(self.width - len(self.title) - len(self.get_controller().location)), self.get_controller().location)
        display.cline(self, heading)
        self.x_acc -= 2
        display.cline(self, "-"*(self.x))
        self.x_acc += 2

    def process(self, command):
        # Since this is a 'forced' dialogue screen, you must press enter.
        if command("confirm"):
            self.selector.choose()
            self.suicide()
            command.done()