import curses
# TODO: Move everything requiring re to text handling
import random
import re

from src.lib.util import debug
from src.lib.util.geometry.space import Point

class CursesLayer(object):
    """A renderable portion of a `CursesDisplay`."""

    def __init__(self, display, window):
        # self._window = None
        # self._dimensions = None
        # self._position = None

        self.display = display
        self.window = window

        # Disable blocking behavior
        # self.window.timeout(0)

    """Layer attribute properties."""

    @property
    def window(self):
        return self._window

    @window.setter
    def window(self, window):
        self._window = window
        try:
            self.dimensions = Point(*reversed(self.window.getmaxyx()))
            self.position = Point(*reversed(self.window.getbegyx()))
        except:
            curses.resetty()
            curses.endwin()
            raise

    @property
    def dimensions(self):
        return self._dimensions

    @dimensions.setter
    def dimensions(self, dimensions):
        self._dimensions = dimensions
        self.window.resize(*reversed(dimensions))

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position
        self.window.mvwin(*reversed(position))

    """Layer drawing methods."""

    def draw(self):
        self.window.erase()
        # for component in self.components:
        #     component.__draw__(self)
        self.window.refresh()

    def undrawable(self, coords):
        """Returns whether the given coordinates are undrawable."""
        x, y = coords
        # Negative screen coordinates.
        if x < 0 or y < 0:
            return True
        # Screen coordinates larger than the number of rows or columns.
        max_x, max_y = self.dimensions
        if x >= max_x or y >= max_y:
            return True
        return False

    def attr(self, color=None, attr=None):
        """Set up curses attributes on a string."""
        # TODO: Handle anything but basic colors
        if color:
            col = self.display.colors.get(color)
            if not col:
                fg, bg = color.split("-")
                fg = random.choice(self.display.colors[fg])
                bg = random.choice(self.display.colors[bg])
                col = self.display.pairs.get("{}-{}".format(fg, bg))
            return curses.color_pair(col)
        return 0

    # Rectangular character function.
    def rd(self, view, coords, glyph, col=None, attr=None, box=True):
        x, y = coords
        view_x, view_y = view.position

        draw_x = x + view_x
        draw_y = y + view_y
         # if box is True:
        #     draw_x += view.left
        #     draw_y += view.top
        #assert self.undrawable((draw_x, draw_y)) is False, "rd function tried to draw '%s' out of bounds: %s at %s." % (glyph, self.__dict__, (draw_x, draw_y))
        try: self.window.addch(draw_y, draw_x, glyph, self.attr(col, attr))
        except curses.error: pass

    # Rectangular string function.
    def rds(self, view, coords, string, col=None, attr=None, box=True):
        x, y = coords
        view_x, view_y = view.position

        draw_x = x + view_x
        draw_y = y + view_y
        # if box is True:
        #     draw_x += view.left
        #     draw_y += view.top
        #assert self.undrawable((draw_x, draw_y)) is False, "rds function tried to draw '%s' out of bounds: %s at %s." % (string, self.__dict__, (draw_x, draw_y))
        try: self.window.addstr(draw_y, draw_x, string, self.attr(col, attr))
        except curses.error: pass

    # Draw a line in rectangular coords - requires linebreaking.
    def rdl(self, view, pos, line, col=None, attr=None, indent=0):
        # Maximum number of chars we'll try to print in a line.
        try:
            max = view.width - pos[0]# - view.x_acc - pos[0]
        except:
            debug.die(view)

        if len(line) > max:
            list = re.split('(\W+)', line)
            string = ""

            for word in list:
                if len(word) + len(string) > max:
                    self.rds(view, pos, string, col, attr)
                    max = view.width - view.x_acc
                    pos = (view.x_acc, pos[1]+1)
                    view.y_acc += 1
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

        self.rds(view, pos, string, col, attr)
        return len(string)

    def hd(self, view, coords, glyph, col=None, attr=None, offset=None):
        """Draw a glyph/color/attribute at hexagonal coordinates projected on a
        rectangular space (with an optional rectangular offset)."""
        # The map coordinates of a target:
        t_x, t_y = coords
        # The map coordinates of the viewport's center:
        c_x, c_y = view.center
        # The window coordinates of the viewport's center:
        v_x, v_y = view.viewport_pos
        # The heading (in window coordinates) of the target's viewport offset:
        h_x, h_y = offset if offset else (0, 0)

        # Calculate distance from the viewport center:
        d_x = t_x - c_x
        d_y = t_y - c_y

        # Calculate window coordinates:
        draw_x = d_y + 2*(d_x+v_x) + h_x
        draw_y = d_y + v_y + h_y

        if not self.undrawable((draw_x, draw_y)):
            try:
                self.window.addch(draw_y, draw_x, glyph, self.attr(col, attr))
            except curses.error:
                pass

    # Draw a simple line; only relevant for text-y views.
    def line(self, view, string, col=None, attr=None, indent=0):
        pos = (view.x_acc, view.y_acc)
        self.rdl(view, pos, string, col, attr, indent)
        view.y_acc += 1

    # Print a line with multiple colors
    # TODO: Handle other attributes.
    def cline(self, view, string, col=None, attr=None, indent=0):
        x_position = 0
        curr_col = col
        substrs = re.split('(</*\w*-?\w*>)',string)
        for substr in substrs:
            # Figure out tags.
            if substr == '':
                continue;
            elif substr == '<br>':
                view.y_acc += 1
                x_position = 0
            elif substr == '</>':
                curr_col = col
            elif re.match('<.*>', substr):
                tag = re.split('<(.*)>', substr)[1]
                if tag is not None:
                    curr_col = tag
            else:
                #if len(string) > view.width+20:
                #    exit(substrs)
#                y_acc = view.y_acc
                pos = (x_position + view.x_acc, view.y_acc)
                length = self.rdl(view, pos, substr, curr_col, attr, indent)
                if view.x_acc + x_position + length <= view.width:
                    #x_position = 0
#                    view.y_acc += 1
                #else:
                    x_position += length
#                    if x_position == 80:
#                        exit("This was it")
             #   else:
#                    view.y_acc += 1
              #      x_position = view.x_acc
        # Only increment y at the end of the line.
        view.y_acc += 1

    # Simple border function (no margin, border 1, padding 1).
    def border(self, view, glyph):
        import itertools
        p_top, p_right, p_bottom, p_left = view.padding

        top = view.top - p_top - 1
        right = view.right + p_right + 1
        bottom = view.bottom + p_bottom + 1
        left = view.left - p_left - 1

        height = bottom - top + 1
        width = right - left + 1
        # exit([x for x in itertools.izip_longest(*map(range, view.border))])

        for t, r, b, l in itertools.izip_longest(*map(range, view.border)):
            # Top border
            if t is not None:
                self.rds(view, (left - t, top - t), "T"*(2*t + width))

            # Right border
            if r is not None:
                for y in xrange(2*r + height):
                    self.rd(view, (right + r, top - r + y), "R")

            # Bottom border
            if b is not None:
                self.rds(view, (left - b, bottom + b), "B"*(2*b + width))

            # Left border
            if l is not None:
                for y in xrange(2*l + height):
                    self.rd(view, (left - l, top - l + y), "L")

            # TODO: Handle diagonals.