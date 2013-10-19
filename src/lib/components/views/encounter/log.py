from src.lib.components.component import override_defaults
from src.lib.components.input import Scroller
from src.lib.components.views.view import View

from src.lib.util.define import *
# TODO: Use kernel service.
from src.lib.util.log import Log
from src.lib.util import text

class LogPane(View):
    default_arguments = {
        "x" : PANE_X,
        "y" : LOG_Y,
        "start_x" : PANE_START_X,
        "start_y" : LOG_START_Y
    }

    @override_defaults
    def __init__(self, **kwargs):
        super(LogPane, self).__init__(**kwargs)
        self.autoscroll = True
        self.events = 0
        self.shrink = 0

    # Spawn a scroller and add the log to the map.
    def ready(self):
        self.scroller = self.spawn(Scroller(Log.length() - self.height))

    def before_draw(self):
        if Log.length() > self.events:
            max_scroll = max(0, Log.length() - self.height)
            self.scroller.resize(max_scroll)
            if self.autoscroll is True:
                self.scroller.scroll(Log.length() - self.events)
            self.events = Log.length()

    def draw(self):
        # Start from the bottom:
        self.x_acc = 2
        self.y_acc = self.height
        index = self.scroller.max

        if self.scroller.index != self.scroller.max:
            self.y_acc -=1
            self.line("[...]")
            self.y_acc -=1
            index += 1

        everything = True
        # TODO: Don't use raw events
        for event in reversed(Log.events):
            index -= 1
            if index >= self.scroller.index:
                continue
            if self.logline(event) is False:
                self.y_acc = self.shrink
                self.line("[...]")
                everything = False
                break;

        if everything is False:
            self.x_acc = 0
            self.y_acc = self.shrink
            # TODO: Fix this, it's buggy!
            proportion = float(self.scroller.index) / (1+self.scroller.max)
            position = int(proportion * (self.height - self.y_acc - 1))

            self.line("^")
            for x in range(self.height - self.y_acc - 1):
                if x+1 == position:
                    self.cline("<green-black>@</>")
                else:
                    self.line("|")
            self.line("v")

    def logline(self, event):
        lines = text.wrap_string([event], self.width - self.x_acc)

        # Move up by that much to offset what the line function would do.
        self.y_acc -= len(lines)

        # Couldn't fit it all.
        if self.y_acc - self.shrink < 1 and self.scroller.index != self.scroller.min:
            return False;

        # Otherwise, display the line(s):
        for line in lines:
            self.cline(line[0].capitalize() + line[1:])

        # Since we're moving in reverse.
        self.y_acc -= len(lines)

    # TODO: Fix tabbing only work when [...] or more logs.
    def keyin(self, c):
        if c == ord("\t"): # Tab
            if self.shrink > 0:
                self.shrink -= 5
            else:
                self.shrink += 5