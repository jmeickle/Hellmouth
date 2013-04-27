import curses

from collections import deque
from operator import itemgetter, attrgetter
from random import choice

from src.lib.components.views.view import View
from src.lib.components.views.screens.screen import Screen
from src.lib.components.input import Cursor, Scroller, SideScroller, Chooser, SideChooser, Tabber, TextPrompt

from src.lib.agents.contexts.context import Context
from src.lib.util.command import CommandRegistry as CMD
from src.lib.util.define import *
from src.lib.util.debug import debug
from src.lib.util.hex import *
from src.lib.util import text
from src.lib.util.log import Log
from src.lib.util.mixin import DebugMixin

from src.lib.data.skills import skill_list


class EncounterWindow(View):
    """Main tactical window class."""
    def __init__(self, window, map_obj):
        self.map = map_obj
        super(EncounterWindow, self).__init__(window, TERM_X, TERM_Y)

    def ready(self):
        self.spawn(SidePane(self.screen))
        self.spawn(MainPane(self.screen))

# Larger, left-hand pane
class MainPane(View):
    def __init__(self, window):
        View.__init__(self, window, MAP_X, MAP_Y, MAP_START_X, MAP_START_Y)

    def ready(self):
        self.spawn(MainMap(self.screen, MAP_X, MAP_Y, MAP_START_X, MAP_START_Y))
        self.spawn(Status(self.screen, STATUS_X, STATUS_Y, STATUS_START_X, PANE_START_Y))
        self.spawn(Place(self.screen, STATUS_X+2, STATUS_Y, MAP_START_X, MAP_START_Y))

# Smaller, right-hand pane
class SidePane(View):
    def __init__(self, window):
        View.__init__(self, window, PANE_X, PANE_Y, PANE_START_X, PANE_START_Y)

    def ready(self):
        self.spawn(Stats(self.screen, PANE_X, STATS_Y, PANE_START_X, PANE_START_Y))
        self.spawn(LogViewer(self.screen, PANE_X, LOG_Y, PANE_START_X, LOG_START_Y))

# TODO: Make this a subclass of a Map view, to account for tactical/strategic/etc.
class MainMap(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)
        # -1 to account for 0,0 start
        self.viewport_pos = (int(y/2)-1, int(y/2)-1)
        self.viewport_rank = 10
        self.zoom = self.viewport_rank

        self.cursor = None

    def keyin(self, c):
        # TODO: Allow multiple open children.
        if not self.children:
            if c == ord('I') or c == ord('i'):
                self.spawn(Inventory(self.screen, self.width, self.height))
                return False

            elif c == ord('v'):
                if self.cursor is None:
                    self.cursor = self.spawn(Cursor(self.get_controller().pos))
                    self.cursor.spawn(Examine(self.screen, self.width, 2, 0, self.BOTTOM-1))
                    return False

        """Get items."""
        if c == ord('G'):
            items = []
            for appearance, itemlist in self.get_controller().cell().get_items():
                items.extend(itemlist)
            if items:
                context = self.get_context(participants=items)
                event = chr(c)
                self.get_controller().process_event(event, context)
#        elif c == ord('g'):
#            self.get_controller().command()
#            return False
        elif c == ord('U'):
            terrain = self.get_controller().cell().get_terrain()
            if terrain:
                context = self.get_context(participants=terrain, domains=["Manipulation"])
                event = chr(c)
                self.get_controller().process_event(event, context)
        elif c == ord('}'):
            """Zoom."""
            self.zoom = 2
            self.inherit()
        elif c == ord('{'):
            self.zoom = self.viewport_rank
            self.inherit()
        elif c == ord('N'):
            """Notepad."""
            self.spawn(TextPrompt(self.screen, self.width, self.height))
        elif c == ord('D'):
            """Debugger."""
            self.spawn(Debugger(self.screen, self.width, self.height))
        elif c == ord('7'):
            self.map.get_controller().do(NW)
        elif c == ord('4'):
            self.map.get_controller().do(CW)
        elif c == ord('1'):
            self.map.get_controller().do(SW)
        elif c == ord('9'):
            self.map.get_controller().do(NE)
        elif c == ord('6'):
            self.map.get_controller().do(CE)
        elif c == ord('3'):
            self.map.get_controller().do(SE)
        elif c == ord('5'):
            self.map.get_controller().end_turn()
        elif c == ord('>') or c == ord('<'):
            """Stairs."""
            terrain = self.get_controller().cell().get_terrain()
            if terrain:
                context = self.get_context(participants=terrain, domains=["Manipulation"])
                event = chr(c)
                self.get_controller().process_event(event, context)
        else: return True
        return False

    # Hex character function, for maps only.
    def hd(self, pos, glyph, col=None, attr=None):
        # Three sets of coords are involved:
        x, y = pos
        c_x, c_y = self.center
        v_x, v_y = self.viewport_pos

        # Offsets from the viewport center
        off_x = x - c_x
        off_y = y - c_y

        draw_x = off_y + 2*(off_x+v_x)
        draw_y = off_y + v_y

        # TODO: Log this somewhere useful but don't assert on it.
        assert self.undrawable((draw_x, draw_y)) is False, "hd function tried to draw out of bounds: %s at %s." % (self.__dict__, (draw_x, draw_y))
        try: self.window.addch(draw_y, draw_x, glyph, self.attr(col, attr))
        except curses.error: pass

    # Draw to offset hexes, i.e., the 'blank' ones.
    def offset_hd(self, pos, dir, glyph, col=None, attr=None):
        # Four sets of coords are involved:
        x, y = pos
        c_x, c_y = self.center
        v_x, v_y = self.viewport_pos
        d_x, d_y = dir

        # Offsets from the viewport center
        off_x = x - c_x
        off_y = y - c_y

        draw_x = off_y + 2*(off_x+v_x) + d_x
        draw_y = off_y + v_y + d_y

        # TODO: Log this somewhere useful but don't assert on it.
        assert self.undrawable((draw_x, draw_y)) is False, "offset hd function tried to draw out of bounds: %s at %s." % (self.__dict__, (draw_x, draw_y))
        try: self.window.addch(draw_y, draw_x, glyph, self.attr(col, attr))
        except curses.error: pass

    # Accepts viewport_rank offsets to figure out what part of the map is visible.
    def get_glyph(self, pos, subpositions=False):
        return self.map.cell(pos).draw(subpositions)

    def draw(self):
        self.center = self.cursor.pos if self.cursor else self.get_controller().pos

        cells = area(self.center, self.zoom)
        for cell in cells:
            if self.map.valid(cell) is not False:
                glyph, col, subposition = self.get_glyph(cell)
            else:
                glyph = ','
                col = "red-black"
            # HACK: Multiple-zoom-level system.
            if self.zoom == self.viewport_rank:
                self.hd(cell, glyph, col)
            else:
                diff = sub(cell, self.center)
                pos = add(self.center, mult(diff, 4))
                # HACK: Move this into some generalized hex border function.
                faces = {NW: ("/", WW), NE : ("\\", EE), CE : ("|", EE), SE : ("/", EE), SW: ("\\",  WW), CW: ("|", WW)}
                for dir in dirs:
                    point = add(pos, dir)
                    self.hd(point, ".", "white-black")
                    face, offset = faces[dir]
                    self.offset_hd(point, offset, face, "white-black")
                    # NOTE: Interesting effect!
                    #self.hd(add(pos, mult(dir, 2)), faces[dir], "white-black")
                for glyph, col, subposition in self.get_glyph(cell, True):
                    self.hd(add(pos, subposition), glyph, col)

        if len(self.get_controller().highlights) > 0:
            for highlight_id, highlight_obj in self.get_controller().highlights.items():
                if dist(self.center, highlight_obj.pos) > self.viewport_rank:
                    # TODO: Don't use Bresenham here, it flickers!
                    cells = line(self.center, highlight_obj.pos, self.viewport_rank+2)
                    cell = cells.pop()
                    # TODO: Highlight color
                    glyph, col = "*", "green-black"
                    self.hd(cell, glyph, col)

# A single line of text at the bottom of the screen describing what your
# cursor is currently over.
# TODO: Update for FOV
class Examine(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)

    def keyin(self, c):
        if c == curses.KEY_ENTER or c == ord('\n'):
            if not self.children:
                # TODO: Character sheet takes place of stats screen
#                child = self.spawn(CharacterSheet(self.screen, PANE_X, STATS_Y, PANE_START_X, PANE_START_Y))
                child = self.spawn(CharacterSheet(self.screen, PANE_X, PANE_Y, PANE_START_X, PANE_START_Y))
        elif c == ord('a'):
            actors = self.map.actors(self.parent.pos)
            if actors:
                actor = actors[self.parent.selector.index]
                if actor:
                    context = self.get_context(domains=["Combat"], participants=[actor])
                    event = chr(c)
                    return self.get_controller().process_event(event, context)
        elif c == ord('t') or c == ord('C'):
            actors = self.map.actors(self.parent.pos)
            if actors:
                actor = actors[self.parent.selector.index]
                if actor:
                    context = self.get_context(domains=["Command"], participants=[actor])
                    event = chr(c)
                    return self.get_controller().process_event(event, context)
        return True

    def draw(self):
        pos = self.parent.pos
        cell = self.map.cell(pos)
        if not self.children:
            self.line("Space: Exit. Enter: Inspect. */: Style.")
        else:
            self.line("Space: Stop Inspecting. /*: Style.")
        if cell is not None:
            string = cell.contents()
            self.line("Cursor: %s." % string)
        else:
            self.line("Cursor: There's... nothing. Nothing at all.")

class Stats(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)

    def draw(self):
        # Col 1: Skeleton/Paperdoll
        self.y_acc = 1
        for line in self.get_controller().values("Body", "get_paperdoll"):
            self.cline(line)

        # Show the chosen weapon/attack option combination.
        weapon, wielding_mode = self.get_controller().call("Combat", "get_view_data").get_result()
        # Wielding mode, for now:
        #  0      1        2      3      4      5       6,     7
        # trait, name, damage, d.type, reach, parry, min ST, hands
        trait, attack_name, damage, damage_type, reach_def, parry, min_st, hands = wielding_mode
        trait_level = self.get_controller().trait(trait)
        appearance = weapon.appearance()[:20]
        manipulator = weapon.call("Wielded", "get_manipulator").get_result()

        reach = []
        for distance in reach_def:
            if distance == 0:
                reach.append("C")
            else:
                reach.append("%s" % distance)
        try:
            reach = "(%s)" % ",".join(reach)
        except TypeError:
            exit("reach: %s" % reach)

        # HACK: Should ask the item to display a shorter appearance.
        self.cline("(/*) %s" % (appearance))

        color = "white-black"
        if self.get_controller().base_skills.get(trait) is None:
            color = "red-black"

        self.cline("     %s, <%s>%s-%s</>" % (manipulator.type, color, trait, trait_level))

        selector = ""
        weapons = [w for w in self.get_controller().values("Combat", "get_weapons")]
        if len(weapons) > 1:
            selector = "(+-) "
        self.cline("%5s%s %s %s %s" % (selector, attack_name, self.get_controller().damage(damage, False), damage_type, reach))

        # Col 2: Combat information
        self.x_acc += 12
        self.y_acc = 0

        # Place header
        self.line("%s" % (self.get_controller().appearance()))
        self.line("%s" % "-"*20)
#        self.y_acc += 1

        self.statline('HP')
        self.statline('MP')
        self.statline('FP')
        self.line("")
        self.statline('Block')
        self.statline('Dodge')
        self.statline('Parry')

        # Col 3: Stats
        self.x_acc += 14
        self.y_acc = 2

        self.statline("ST")
        self.statline("DX")
        self.statline("IQ")
        self.statline("HT")
        self.line("")
        self.statline("Will")
        self.statline("Perception")
        self.line("")
        self.statline("Move")
        self.statline("Speed")

        # Don't delete! Probably will reuse this for a 'health' screen.
        #self.line("Wounds:")
        #for loc in sorted(self.get_controller().body.locs.items()):
        #    self.line("%6s: %s" % (loc[0], loc[1].wounds))

    # Print a line like 'Dodge: 15' using stat()
    # TODO: Print colors, *s, etc. for more info.
    def statline(self, stat):
        # Always use the shortest label here.
        label = labels.get(stat)[0]
        value = self.get_controller().stat(stat)
        if value is None:
            value = "n/a"

        # These particular stats actually have two stats to display.
        if stat in ["HP", "FP", "MP"]:
            self.line("%s: %3d/%2d" % (label, value, self.get_controller().stat("Max"+stat)))
        else:
            self.line("%s: %s" % (label, value))

    def keyin(self, c):
        if c == ord("+"):
            weapon = self.get_controller().call("Combat", "get_active_weapon").get_result()
            weapon.call("Wielded", "set_wielding_mode", 1)
        elif c == ord("-"):
            weapon = self.get_controller().call("Combat", "get_active_weapon").get_result()
            weapon.call("Wielded", "set_wielding_mode", -1)
        elif c == ord("*"):
            self.get_controller().call("Combat", "set_active_weapon", 1)
        elif c == ord("/"):
            self.get_controller().call("Combat", "set_active_weapon", -1)
        else:
            return True
        return False

# TODO: Implement this
class Status(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)

    def draw(self):
        for text, color in self.get_controller().values("Status", "get_view_data", self):
            debug("text: %s, color: %s" % (text, color))
            self.line(text, color)
        return True

class Place(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)

    def draw(self):
        self.line(self.map.level.name, "green-black")
        if self.map.name:
            self.line(self.map.name)

class LogViewer(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)
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

class Inventory(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)

    def ready(self):
        self.context = None
        self.tabs = self.spawn(Tabber())
        self.selection = self.spawn(Chooser())
        self.commands = self.spawn(SideChooser())

    def active_tabs(self):
        yield "Inventory"
        yield "Equipment"
        if self.ground:
            yield "Ground"

    # TODO: Fire this on events that require a refresh.
    def refresh(self):
        self.inventory = [item for item in self.get_controller().values("Container", "get_list")]
        self.wielded = [wielded for wielded in self.get_controller().values("Manipulation", "get_wielded")]
        self.equipment = [equipment for equipment in self.get_controller().values("Equipment", "get_worn")]
        self.ground = [ground for ground in self.map.get_controller().cell().get_items()]

        self.tabs.set_choices([choice for choice in self.active_tabs()])

        if self.tabs.get_choice() == "Inventory":
            self.selection.set_choices(self.inventory)
        elif self.tabs.get_choice() == "Equipment":
            self.selection.set_choices(self.wielded + self.equipment)
        elif self.tabs.get_choice() == "Ground":
            self.selection.set_choices(self.ground)

        self.context = self.get_context()

        participant = None

        if self.tabs.get_choice() == "Inventory" and self.inventory:
            participant = self.inventory[self.selection.index]
        elif self.tabs.get_choice() == "Equipment" and self.equipment:
            participant = self.equipment[self.selection.index]
        elif self.tabs.get_choice() == "Ground" and self.ground:
            participant = self.ground[self.selection.index]

        if participant:
            self.context.set_participant(participant)

        self.commands.set_choices([command for command in self.context.get_commands()])

    # Stored here for convenience.
    def before_draw(self):
        self.refresh()

    def draw(self):
        self.window.clear()
        self.border("#")
        self.render()

    def render(self):
        self.cline("Inventory")
        self.y_acc += 1
        if not self.inventory:
            self.cline("No items")
        else:
            for x in range(len(self.inventory)):
                agent = self.inventory[x]
                string = agent.appearance()

                # Highlight tab, if present.
                if self.tabs.get_choice() == "Inventory" and self.selection.get_choice() == agent:
                    string = text.highlight(string)
                self.cline(string)

        self.y_acc += 1

        # Print what's on the ground, too.

        # if len(self.ground) > 0:
        #     self.cline("Ground:")
        #     self.y_acc += 1
        #     for x in range(len(self.ground)):
        #         appearance, items = self.ground[x]
        #         if len(items) > 1:
        #             string = "%d %ss" % (len(items), appearance)
        #         else:
        #             string = appearance

        #         if self.tabs.choice() == "Ground" and x == self.selection.index:
        #             string = text.highlight(string)

        #         self.cline(string)

        self.y_acc = 0
        self.x_acc += 20

        self.cline("Equipped")
        self.y_acc += 1

        for agent in self.wielded:
            self.cline(agent.appearance())

        for agent in self.equipment:
            self.cline(agent.appearance())

        # for x in range(len(self.parts)):
        #     part = self.parts[x]
        #     equipped = ""
        #     for appearance, items in part.readied.items():
        #         for item in items: # Ick. Definitely need to move this printing!
        #             if item.is_wielded():
        #                 equipped += "%s" % appearance # (wielded)
        #             else:
        #                 equipped += "%s" % appearance # (readied)
        #     for appearance, items in part.held.items():
        #         for item in items:
        #             if not item.is_wielded():
        #                 equipped += "%s" % appearance # (held)
        #     for appearance, items in part.worn.items():
        #         for item in items:
        #             equipped += "%s" % appearance # (worn)

        #     # If we don't have a string yet:
        #     if not equipped:
        #         continue

        #     colon = "%s:" % part.appearance()

        #     # Highlights.
        #     if self.tabs.index == 1 and x == self.selection.index:
        #         self.cline("%-11s <green-black>%s</a>" % (colon, equipped))
        #     else:
        #         self.cline("%-11s %s" % (colon, equipped))

        self.x_acc = 0
        self.y_acc = self.BOTTOM - 2

        if self.commands.choices:
            self.cline("Available commands:")
            commands = []
            chosen_class, chosen_arguments = self.commands.get_choice()
            for command_class, command_arguments in self.commands.choices:
                string = command_class.get_desc(short=True)
                for event in command_class.get_events():
                    pos = text.first(event, string)
                    if pos is not None:
                        replacement = "(%s)" % string[pos]
                        if command_class == chosen_class:
                            replacement = text.highlight(replacement)
                        string = string[:pos] + replacement + string[pos+1:]
                commands.append(string)
            self.cline("  %s." % text.commas(commands))

    def event(self, e):
        if self.context:
            return self.get_controller().process_event(e, self.context)
        return True

    def keyin(self, c):
        if c == ord(' '):
            self.suicide()
#         # Hack.
#         elif c == ord('d'):
#             if self.selection.index == 0:
#                 self.get_controller().drop(self.selected())
#             else:
#                 self.get_controller()._drop(self.selected())
#         elif c == ord('e'):
#             self.get_controller().equip(self.selected())#, self.get_controller().body.locs.get(self.get_controller().body.primary_slot))
#         elif c == ord('u'):
#             # This is also a hack.
#             self.get_controller()._unequip(self.selected())
# #        else: return True
#         elif c == ord('G') or c == ord('g'):
#             self.get_controller().get_all()
#             return False
        return False

class CharacterSheet(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)
        self.actor = None
        self.text = []

    def ready(self):
        self.scroller = self.spawn(Scroller())
        self.sidescroller = self.spawn(SideScroller())

    def keyin(self, c):
        if c == ord(' '):
            self.suicide()
        else:
            return True
        return False

    def draw(self):
        self.border("#")
        pos = self.cursor.pos
        actors = self.map.actors(pos)

        # Abort early if no actor.
        if not actors:
            self.cline("There's nothing interesting here.")
            return False

        self.actor = actors[self.cursor.selector.index]

        if len(actors) > 1:
            scroller = "<green-black>"
        else:
            scroller = "<red-black>"

        self.cline('%s(+-)</> %s' % (scroller, self.actor.appearance()))
        self.cline("-"*self.width)

        self.text = text.wrap_string(self.actor.get_view_data(self), self.width)
        self.scroller.resize(len(self.text)-self.height + 2) # To account for the possibility of hidden lines

        offset = 0

        if self.scroller.index > 0:
            self.cline('[...]')
            offset += 1

        maxlines = self.height - self.y_acc

        # TODO: Generalize this.
        for x in range(maxlines):
            if self.y_acc+1 == self.height and self.scroller.index < self.scroller.max:
                self.cline('[...]')
                break;

            index = self.scroller.index + x + offset
            line = self.text[index]
            self.cline(line)
        return False # Block further drawing if we drew.

# TODO: Add a minimap.
#class MiniMap(View):

# TODO: Add a health screen.
#class Health(View):

# Debugging prompt.
class Debugger(View, DebugMixin):
    # 45, 24
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)
        self.choices = ["Queue", "Views"]

    def ready(self):
        self.tabber = self.spawn(Tabber(self.choices))

    def draw(self):
        self.window.clear()
        self.border("/")

        self.y_acc = -1
        choice = self.tabber.get_choice()
        choice_list = " ".join(["[%s]" % c for c in self.tabber.choices])
        self.cline("Debug Window")
        self.cline(text.highlight_substr(choice_list, choice))

        self.cline("")

        # TODO: Scrolling queue page
        if choice == "Queue":
            for actor in self.map.level.queue.get_view_data():
                self.cline(actor)
                if self.y_acc >= self.BOTTOM:
                    break
        elif choice == "Views":
            root = self.get_ancestors()[0]
            view_tree = root.get_view_data(self)
            def print_node(node, indents, indent_size):
                parent, children = node
                node_text = "*%s" % parent
                if self == parent:
                    node_text = text.highlight(node_text)
                self.cline("%s" % (" " * indents * indent_size) + node_text)

                for child in children:
                    print_node(child, indents+1, indent_size)
                    if self.y_acc >= self.BOTTOM:
                        break

            print_node(view_tree, indents=0, indent_size=2)

    def keyin(self, c):
        if c == ord(' '):
            self.suicide()
            return False
        return True