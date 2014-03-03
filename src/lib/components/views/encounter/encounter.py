import curses

from collections import deque
from operator import itemgetter, attrgetter
from random import choice

from src.lib.core.kernel import kernel
from src.lib.agents.contexts.context import Context
from src.lib.components.views.view import View
from src.lib.components.views.screens.screen import Screen
from src.lib.components.input import Cursor, Scroller, SideScroller, Chooser, SideChooser, Tabber, TextPrompt, ListPrompt
from src.lib.components.views.encounter.log import LogPane

from src.lib.util.command import CommandRegistry as CMD
from src.lib.util.geometry.hexagon import Hexagon
from src.lib.util.geometry.space import Point
from src.lib.util import debug
from src.lib.util import text

from src.lib.data.skills import skill_list

class EncounterWindow(View):
    """Main tactical window class."""

    def __init__(self, level, **kwargs):
        super(EncounterWindow, self).__init__(**kwargs)
        self.level = level

    def ready(self):
        # TODO: Ick.
        kernel.output.display.layer("map", dimensions=(kernel.output.display.x, kernel.output.display.y), position=(0,0))
        kernel.output.display.layer("sidebar", dimensions=(kernel.output.display.x, kernel.output.display.y), position=(0,0))

        self.spawn(SidePane(layer="sidebar"))
        self.spawn(MainPane(layer="map"))

class MainPane(View):
    """Larger, left-hand pane."""

    def __init__(self, **kwargs):
        super(MainPane, self).__init__(**kwargs)

    def ready(self):
        self.spawn(Status())
        self.spawn(Place())
        self.spawn(MainMap())

class SidePane(View):
    """Smaller, right-hand pane."""

    def __init__(self, **kwargs):
        super(SidePane, self).__init__(**kwargs)

    def ready(self):
        self.spawn(Stats())
        self.spawn(LogPane())

# TODO: Make this a subclass of a Map view, to account for tactical/strategic/etc.
class MainMap(View):
    height = 24
    width = 45
    position = (0,0)
    
    def __init__(self, **kwargs):
        super(MainMap, self).__init__(**kwargs)
        self.viewport_pos = Point(int(self.y/2)-1, int(self.y/2)-1) # -1 to account for 0,0 start
        self.viewport_rank = kwargs.get("viewport_rank", 10)
        self.zoom = kwargs.get("zoom", 10)

    def get_focus(self):
        cursor = self.get_first_child(Cursor)
        return cursor.coords if cursor else self.get_controller().coords

    def keyin(self, c):
        # TODO: Allow multiple open children.
        if not self.children:
            if c == ord('I') or c == ord('i'):
                self.spawn(Inventory(x=self.width, y=self.height))
                return False

            elif c == ord('v'):
                if self.has_child(Cursor) is False:
                    cursor = self.spawn(Cursor(self.get_controller().coords))
                    cursor.spawn(Examine(x=self.width, y=2, start_x=0, start_y=self.BOTTOM-1))
                    return False
        if c == ord('G'):
            """Get all nearby items."""
            items = []
            for appearance, itemlist in self.get_controller().cell.get_items():
                items.extend(itemlist)
            if items:
                context = self.get_context(participants=items)
                event = chr(c)
                self.get_controller().process_event(event, context)
        elif c == ord('g'):
            """Get a specific item, via a Prompt."""
            cursor = self.get_first_child(Cursor)
            self.add_blocking_component(ListPrompt, x=self.width, y=self.height, choices=["one", "two", "three"], callback=cursor.suicide if cursor else self.suicide)
        elif c == ord('U'):
            terrain = self.get_controller().cell.get_terrain()
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
            self.spawn(TextPrompt(x=self.width, y=self.height))
        elif c == ord('D'):
            """Debugger."""
            self.add_blocking_component(Debugger, x=self.width, y=self.height)
        elif c == ord('7'):
            self.level.get_controller().do(Hexagon.NW)
        elif c == ord('4'):
            self.level.get_controller().do(Hexagon.CW)
        elif c == ord('1'):
            self.level.get_controller().do(Hexagon.SW)
        elif c == ord('9'):
            self.level.get_controller().do(Hexagon.NE)
        elif c == ord('6'):
            self.level.get_controller().do(Hexagon.CE)
        elif c == ord('3'):
            self.level.get_controller().do(Hexagon.SE)
        elif c == ord('5'):
            self.level.get_controller().end_turn()
        elif c == ord('>') or c == ord('<'):
            """Stairs."""
            terrain = self.get_controller().cell.get_terrain()
            if terrain:
                context = self.get_context(participants=terrain, domains=["Manipulation"])
                event = chr(c)
                self.get_controller().process_event(event, context)
        else: return True
        return False

    def get_glyph(self, map_obj, coords):
        """Return a glyph and color to display for a position."""
        cell = map_obj.cell(coords)

        # Prioritize displaying actors.
        if cell.actors:
            actor = cell.actors[0]
            glyph = actor.glyph
            color = actor.color
            # TODO: HACK
            if actor.get("Status", "Unconscious"):
                color += "-white"
            elif len(cell.actors) > 1:
                color += "-magenta"
            else:
                color += "-black"
            return glyph, color

        # Display items otherwise.
        if len(cell.items) == 1:
            return cell.items[0].glyph, cell.items[0].color
        elif len(cell.items) > 1:
            return '+', 'red-black'
        # Otherwise, display terrain if possible.
        elif cell.terrain is not None:
            return cell.terrain.glyph, cell.terrain.color
        else:
            return cell.map.floor

    def draw(self, display):
        map_obj = self.level.get_map()
        self.center = self.get_focus()

        # Draw the encounter map.
        for rank, index, coords in Hexagon.area(self.center, self.zoom):
            if map_obj.valid(coords) is not False:
                glyph, col = self.get_glyph(map_obj, coords)
            else:
                glyph = ','
                col = "red-black"
            display.hd(self, coords, glyph, col)

        # Draw highlights around the encounter map border.
        if len(self.get_controller().highlights) > 0:
            for highlight_id, highlight_obj in self.get_controller().highlights.items():
                if Hexagon.distance(self.center, highlight_obj.coords) > self.viewport_rank:
                    # TODO: Don't use Bresenham here, it flickers!
                    continue
                    cells = line(self.center, highlight_obj.coords, self.viewport_rank+2)
                    cell = cells.pop()
                    # TODO: Highlight color
                    glyph, col = "*", "green-black"
                    display.hd(self, cell, glyph, col)

# A single line of text at the bottom of the screen describing what your
# cursor is currently over.
# TODO: Update for FOV
class Examine(View):
    def __init__(self, **kwargs):
        super(Examine, self).__init__(**kwargs)

    def keyin(self, c):
        if c == curses.KEY_ENTER or c == ord('\n'):
            for parental_sibling in self.get_parental_siblings(SidePane):
                if not parental_sibling.has_child(CharacterSheet):
                    parental_sibling.spawn(CharacterSheet())
                    return False
                return True
        elif c == ord('a'):
            actors = self.level.get_map().actors(self.parent.coords)
            if actors:
                actor = actors[self.parent.selector.index]
                if actor:
                    context = self.get_context(domains=["Combat"], participants=[actor])
                    event = chr(c)
                    return self.get_controller().process_event(event, context)
        elif c == ord('t') or c == ord('C'):
            actors = self.level.get_map().actors(self.parent.coords)
            if actors:
                actor = actors[self.parent.selector.index]
                if actor:
                    context = self.get_context(domains=["Command"], participants=[actor])
                    event = chr(c)
                    return self.get_controller().process_event(event, context)
        else: return True
        return False

    def draw(self, display):
        coords = self.parent.coords
        cell = self.level.get_map().cell(coords)
        if not self.children:
            display.line(self, "Space: Exit. Enter: Inspect. */: Style.")
        else:
            display.line(self, "Space: Stop Inspecting. /*: Style.")

        if cell is not None:
            display.line(self, "Cursor: %s." % self.describe_contents(cell))
        else:
            display.line(self, "Cursor: There's... nothing. Nothing at all.")

    # TODO: Options for what to list.
    def describe_contents(self, cell):
        contents = []
        if cell.actors:
            for actor in cell.actors:
                contents.append("a %s" % actor.appearance())
        if cell.terrain:
            contents.append("a %s" % cell.terrain.name)
        if cell.items:
            for item in cell.items:
                contents.append(item.appearance())
        if not contents:
            contents.append("nothing of interest")
        return text.commas(contents)

class Stats(View):
    height = 24
    width = 35
    position = (45, 0)

    def __init__(self, **kwargs):
        super(Stats, self).__init__(**kwargs)

    def draw(self, display):
        # Col 1: Skeleton/Paperdoll
        self.y_acc = 1
        for line in self.get_controller().values("Body", "get_paperdoll"):
            display.cline(self, line)

        # Show the chosen weapon/attack option combination.
        weapon, wielding_mode = self.get_controller().call("Combat", "get_view_data").get_result()

        # Wielding mode, for now:
        #  0      1        2      3      4      5       6,     7
        # trait, name, damage, d.type, reach, parry, min ST, hands
        trait, attack_name, damage, damage_type, reach_def, parry, min_st, hands = wielding_mode
        trait_level = self.get_controller().trait(trait)
        # HACK: Should ask the item to display a shorter appearance.
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

        display.cline(self, "(/*) %s" % (appearance))

        color = "white-black"
        if self.get_controller().base_skills.get(trait) is None:
            color = "red-black"

        display.cline(self, "     %s, <%s>%s-%s</>" % (manipulator.type, color, trait, trait_level))

        selector = ""
        weapons = [w for w in self.get_controller().values("Combat", "get_weapons")]
        if len(weapons) > 1:
            selector = "(+-) "
        display.cline(self, "%5s%s %s %s %s" % (selector, attack_name, self.get_controller().damage(damage, False), damage_type, reach))

        # Col 2: Combat information
        self.x_acc += 12
        self.y_acc = 0

        # Place header
        display.line(self, "%s" % (self.get_controller().appearance()))
        display.line(self, "%s" % "-"*20)
#        self.y_acc += 1

        self.statline(display, 'HP')
        self.statline(display, 'MP')
        self.statline(display, 'FP')
        display.line(self, "")
        self.statline(display, 'Block')
        self.statline(display, 'Dodge')
        self.statline(display, 'Parry')

        # Col 3: Stats
        self.x_acc += 14
        self.y_acc = 2

        self.statline(display, "ST")
        self.statline(display, "DX")
        self.statline(display, "IQ")
        self.statline(display, "HT")
        display.line(self, "")
        self.statline(display, "Will")
        self.statline(display, "Perception")
        display.line(self, "")
        self.statline(display, "Move")
        self.statline(display, "Speed")

        # Don't delete! Probably will reuse this for a 'health' screen.
        #display.line(self, "Wounds:")
        #for loc in sorted(self.get_controller().body.locs.items()):
        #    display.line(self, "%6s: %s" % (loc[0], loc[1].wounds))

    # Print a line like 'Dodge: 15' using stat()
    # TODO: Print colors, *s, etc. for more info.
    def statline(self, display, stat):
        # Always use the shortest label here.
        label = labels.get(stat)[0]
        value = self.get_controller().stat(stat)
        if value is None:
            value = "n/a"

        # These particular stats actually have two stats to display.
        if stat in ["HP", "FP", "MP"]:
            display.line(self, "%s: %3d/%2d" % (label, value, self.get_controller().stat("Max"+stat)))
        else:
            display.line(self, "%s: %s" % (label, value))

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

class Status(View):
    """Displays status effects, like hunger or pain."""

    def __init__(self, **kwargs):
        View.__init__(self, **kwargs)

    def draw(self, display):
        for text, color in self.get_controller().values("Status", "get_view_data", self):
            debug.log("text: %s, color: %s" % (text, color))
            display.line(self, text, color)
        return True

class Place(View):
    """Displays information about the current level and map."""

    def __init__(self, **kwargs):
        super(Place, self).__init__(**kwargs)

    def draw(self, display):
        display.line(self, self.level.name, "green-black")
        display.line(self, self.level.get_map().name)

class Inventory(View):
    """Displays information about held, worn, and carried items."""

    def __init__(self, **kwargs):
        super(Inventory, self).__init__(**kwargs)

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
        self.ground = [ground for ground in self.level.get_controller().cell.get_items()]

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
    def before_draw(self, display):
        self.refresh()

    def draw(self, display):
        self.window.clear()
        self.border("#")
        self.render()

    def render(self):
        display.cline(self, "Inventory")
        self.y_acc += 1
        if not self.inventory:
            display.cline(self, "No items")
        else:
            for x in range(len(self.inventory)):
                agent = self.inventory[x]
                string = agent.appearance()

                # Highlight tab, if present.
                if self.tabs.get_choice() == "Inventory" and self.selection.get_choice() == agent:
                    string = text.highlight(string)
                display.cline(self, string)

        self.y_acc += 1

        # Print what's on the ground, too.

        # if len(self.ground) > 0:
        #     display.cline(self, "Ground:")
        #     self.y_acc += 1
        #     for x in range(len(self.ground)):
        #         appearance, items = self.ground[x]
        #         if len(items) > 1:
        #             string = "%d %ss" % (len(items), appearance)
        #         else:
        #             string = appearance

        #         if self.tabs.choice() == "Ground" and x == self.selection.index:
        #             string = text.highlight(string)

        #         display.cline(self, string)

        self.y_acc = 0
        self.x_acc += 20

        display.cline(self, "Equipped")
        self.y_acc += 1

        for agent in self.wielded:
            display.cline(self, agent.appearance())

        for agent in self.equipment:
            display.cline(self, agent.appearance())

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
        #         display.cline(self, "%-11s <green-black>%s</a>" % (colon, equipped))
        #     else:
        #         display.cline(self, "%-11s %s" % (colon, equipped))

        self.x_acc = 0
        self.y_acc = self.BOTTOM - 2

        if self.commands.choices:
            display.cline(self, "Available commands:")
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
            display.cline(self, "  %s." % text.commas(commands))

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
    """Display information about an inspected Actor."""
    # TODO: a general InformationSidebar class, polymorphic on what is being viewed

    def __init__(self, **kwargs):
        super(CharacterSheet, self).__init__(**kwargs)
        self.actor = None
        self.text = []

    def ready(self):
        self.scroller = self.spawn(Scroller())
        self.sidescroller = self.spawn(SideScroller())

    def keyin(self, c):
        if c == ord(' '):
            self.suicide()
        else: return True
        return False

    # TODO: Fix this.
    def draw(self, display):
        sibling = self.get_first_parental_sibling(MainPane)
        cursor = sibling.get_first_descendent(Cursor)
        if not cursor:
            self.suicide()
            return True
        self.window.clear()
        self.border("#")

        cell = self.map.cell(cursor.coords)
        actors = cell.actors if cell else None

        # Abort early if no actor.
        if not actors:
            display.cline(self, "There's nothing interesting here.")
            return True

        self.actor = actors[cursor.selector.index]

        if len(actors) > 1:
            scroller = "<green-black>"
        else:
            scroller = "<red-black>"

        display.cline(self, '%s(+-)</> %s' % (scroller, self.actor.appearance()))
        display.cline(self, "-"*self.width)

        self.text = text.wrap_string(self.actor.get_view_data(self), self.width)
        self.scroller.resize(len(self.text)-self.height + 2) # To account for the possibility of hidden lines

        offset = 0

        if self.scroller.index > 0:
            display.cline(self, '[...]')
            offset += 1

        maxlines = self.height - self.y_acc

        # TODO: Generalize this.
        for x in range(maxlines):
            if self.y_acc+1 == self.height and self.scroller.index < self.scroller.max:
                display.cline(self, '[...]')
                break;

            index = self.scroller.index + x + offset
            line = self.text[index]
            display.cline(self, line)
#        return False # Block further drawing if we drew.

# TODO: Add a minimap.
#class MiniMap(View):

# TODO: Add a health screen.
#class Health(View):

class Debugger(View):
    """Displays debugging information."""

    def __init__(self, **kwargs):
        super(Debugger, self).__init__(**kwargs)
        self.choices = kwargs["choices"]

    def ready(self):
        self.tabber = self.spawn(Tabber(self.choices))

    def draw(self, display):
        self.window.clear()
        self.border("/")

        self.y_acc = -1
        choice = self.tabber.get_choice()
        choice_list = " ".join(["[%s]" % c for c in self.tabber.choices])
        display.cline(self, "Debug Window")
        display.cline(self, text.highlight_substr(choice_list, choice))

        display.cline(self, "")

        # TODO: Scrolling queue page
        if choice == "Queue":
            for actor in self.parent.game.level.queue.get_view_data():
                display.cline(self, actor)
                if self.y_acc >= self.BOTTOM:
                    break
        elif choice == "Views":
            root = [ancestor for ancestor in self.get_ancestors()].pop()
            view_tree = root.get_view_data(self)
            def print_node(node, indents, indent_size):
                parent, children = node
                node_text = "*%s" % parent
                if self == parent:
                    node_text = text.highlight(node_text)
                display.cline(self, "%s" % (" " * indents * indent_size) + node_text)

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