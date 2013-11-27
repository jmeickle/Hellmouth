import curses
import re
from collections import deque
from random import choice

from src.lib.components.component import Component, override_defaults
from src.lib.util.color import Color
from src.lib.util.define import *
from src.lib.util import key

class View(Component):
    default_arguments = {

    }

    @override_defaults
    def __init__(self, x, y, start_x=0, start_y=0, **kwargs):
        super(View, self).__init__(**kwargs)
        self.x = x
        self.y = y
        self.start_x = start_x
        self.start_y = start_y

        # Set up drawing variables (redone each draw)
        self._reset()

    def get_window(self, window):
        return window.subwin(self.y, self.x, self.start_y, self.start_x)

    # Resets view-drawing-related variables. Run each draw.
    def _reset(self, margin=(0,0), border=(0,0), padding=(0,0)):
        # Box model.
        margin_x, margin_y = margin
        border_x, border_y = border
        padding_x, padding_y = padding

        edge_x = margin_x + border_x + padding_x
        edge_y = margin_y + border_y + padding_y

        self.TOP = edge_y
        self.LEFT = edge_x
        self.BOTTOM = self.y - edge_y - 1
        self.RIGHT = self.x - edge_x - 1

        # Available width/height.
        self.width = self.x - 2*edge_x
        assert self.width > 0, "Width was below 1 after box model: %s" % self.__dict__
        self.height = self.y -2*edge_y
        assert self.height > 0, "Height was below 1 after box model: %s" % self.__dict__

        # Some references based on width/height, to make placing a bit nicer

        # Cumulative x/y tracking.
        self.x_acc = 0
        self.y_acc = 0

    # Rectangular character function.
    def rd(self, pos, glyph, col=None, attr=None, box=True):
        x, y = pos
        draw_x = x
        draw_y = y
        if box is True:
            draw_x += self.LEFT
            draw_y += self.TOP
        #assert self.undrawable((draw_x, draw_y)) is False, "rd function tried to draw '%s' out of bounds: %s at %s." % (glyph, self.__dict__, (draw_x, draw_y))
        try: self.window.addch(draw_y, draw_x, glyph, Color.attr(col, attr))
        except curses.error: pass

    # Rectangular string function.
    def rds(self, pos, string, col=None, attr=None, box=True):
        x, y = pos
        draw_x = x
        draw_y = y
        if box is True:
            draw_x += self.LEFT
            draw_y += self.TOP
        #assert self.undrawable((draw_x, draw_y)) is False, "rds function tried to draw '%s' out of bounds: %s at %s." % (string, self.__dict__, (draw_x, draw_y))
        try: self.window.addstr(draw_y, draw_x, string, Color.attr(col, attr))
        except curses.error: pass

    # Draw a line in rectangular coords - requires linebreaking.
    def rdl(self, pos, line, col=None, attr=None, indent=0):
        # Maximum number of chars we'll try to print in a line.
        max = self.width - pos[0]# - self.x_acc - pos[0]

        if len(line) > max:
            list = re.split('(\W+)', line)
            string = ""

            for word in list:
                if len(word) + len(string) > max:
                    self.rds(pos, string, col, attr)
                    max = self.width - self.x_acc
                    pos = (self.x_acc, pos[1]+1)
                    self.y_acc += 1
                    string = " "*indent
                # Skip if:
                # 1: We're on the start of a line
                # 2: And the current to-print is nothing
                # 3: And we're trying to print a space
                if pos[0] == 0 and string == '' and word.isspace() is True:
                    continue
                string += word
        else:
            string = line

        self.rds(pos, string, col, attr)
        return len(string)

    # Draw a simple line; only relevant for text-y views.
    def line(self, string, col=None, attr=None, indent=0):
        pos = (self.x_acc, self.y_acc)
        self.rdl(pos, string, col, attr, indent)
        self.y_acc += 1

    # Print a line with multiple colors
    # TODO: Handle other attributes.
    def cline(self, string, col=None, attr=None, indent=0):
        x_position = 0
        curr_col = col
        substrs = re.split('(</*\w*-?\w*>)',string)
        for substr in substrs:
            # Figure out tags.
            if substr == '':
                continue;
            elif substr == '<br>':
                self.y_acc += 1
                x_position = 0
            elif substr == '</>':
                curr_col = col
            elif re.match('<.*>', substr):
                tag = re.split('<(.*)>', substr)[1]
                if tag is not None:
                    curr_col = tag
            else:
                #if len(string) > self.width+20:
                #    exit(substrs)
#                y_acc = self.y_acc
                pos = (x_position + self.x_acc, self.y_acc)
                length = self.rdl(pos, substr, curr_col, attr, indent)
                if self.x_acc + x_position + length <= self.width:
                    #x_position = 0
#                    self.y_acc += 1
                #else:
                    x_position += length
#                    if x_position == 80:
#                        exit("This was it")
             #   else:
#                    self.y_acc += 1
              #      x_position = self.x_acc
        # Only increment y at the end of the line.
        self.y_acc += 1

    # Simple border function (no margin, border 1, padding 1).
    def border(self, glyph):
        self.rds((0, 0), glyph*(self.x))
        while self.y_acc+1 < self.y:
            self.rd((0, self.y_acc), glyph)
            self.rd((self.x-1, self.y_acc), glyph)
            self.y_acc += 1
        self.rds((0, self.y_acc), glyph*(self.x))
        # Margin, border, padding. Re-calling _reset isn't harmful.
        self._reset((0,0), (1,1), (1,0))
