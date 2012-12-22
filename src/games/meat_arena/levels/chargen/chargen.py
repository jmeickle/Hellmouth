from copy import copy
import curses

from src.lib.util.component import Component
from src.lib.views.view import View

# TODO: Make this not depend on game
from src.games.meat_arena.levels.chargen.lifepath import Lifepath

from src.lib.data.dialogue import chargen
from src.lib.data.lifepaths import eventdata

class Chargen(Component):
    def __init__(self, screen, player):
        Component.__init__(self)
        self.screen = screen
        self.player = player
        self.lifepath = self.player.lifepath

    def draw(self):
        if not self.children:
            self.spawn(ChargenScreen(self.screen, self.lifepath))
        #return False

# TODO: Chargen actually affects stats.
class Chargen(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)
        self.player = None
        self.lifepath = Lifepath()
        self.current = None
        self.toggle_events = False
        self.selected = 0
        self.selections = []
        self.max = len(self.lifepath.first)-1

    def scroll(self, amt):
        self.selected += amt

        if self.selected < 0:
            self.selected = 0

        if self.selected >= self.max:
            self.selected = self.max

    def next(self, choice=None):
        if choice is None:
            choice = self.current.choices[self.selected]

        if self.current is not None:
            self.current.choose(choice)
            self.current = self.current.child
            self.lifepath.events.append(self.current)
            current_player = copy(self.player)
            self.lifepath.players.append(current_player)
        else:
            self.lifepath.start(choice)
            self.current = self.lifepath.first
        # TODO: Handle appending inside of choose()
        self.reset_choices()


    def prev(self):
        if self.current.parent is not None:
            self.current.undo()
            self.current = self.current.parent
            self.lifepath.events.pop()
            self.reset_choices(True)
        else:
            self.current.undo()
            self.current = None
            self.lifepath.events.pop()
            self.lifepath.first = self.lifepath.skip
            self.reset_choices(True)

    def reset_choices(self, restore=False):
        # Reset selection:
        if restore is False:
            self.selections.append(self.selected)
            self.selected = 0
        else:
            self.selected = self.selections.pop()

        # Reset number of choices:
        if self.current is not None:
            if self.current.choices is not None:
                self.max = len(self.current.choices)-1
        else:
            self.max = len(self.lifepath.skip)-1

    def draw(self):
        # TODO: Don't calculate this each time, jeez!
        if self.current is not None:
            # Character pane:
            self.x_acc = 50
            self.y_acc = 4
            self.cline("Your character:")
            future = copy(self.player)#.character = self.lifepath.effects()
            self.lifepath.effects(future)
            future.recalculate()
            text = future.character_sheet(True)
            for line in text:
                self.cline(line)
                #self.cline("%s: %s" % (key, value))#: %s" % (stat, value))

        # Top part of the screen:
        self.x_acc = 0
        self.y_acc = 0

        # Triggers if we haven't started down a lifepath yet.
        # Prints initial text.
        if self.current is None:
            self.cline(chargen["initial"])
        # STUB: Triggers if an event brings a prompt with it.
        # Prints the prompt text.
        #elif self.current.prompt is not None:
        # Triggers if we're at a certain age in the lifepath.
        # Prints the text asking about the NEXT age category.
        elif self.current.age is not None:
            self.cline(chargen["age-%s" % (self.current.age+1)])
        # Triggers if we have a choice without an associated age (i.e., a final one.)
        # Prints a list of events in your lifepath.
        else:
            self.cline(chargen["final"])
            self.y_acc += 2
            level = self.y_acc
            self.cline("What you've told the stranger:")
            self.y_acc += 1
            # TODO: Duplicated code.
            for event in self.lifepath.events:
                # We only want events with short descriptions. If they take a certain number of years, list that.
                if event.short is not None:
                    string = "You %s" % event.short
                    if event.years is not None:
                        string += " "
                        if event.years == 1:
                            string += "(%s year)" % event.years
                        else:
                            string += "(%s years)" % event.years
                    self.cline(string+".")
            old = self.y_acc
            self.y_acc = level

        self.y_acc += 1
        # Print the text from the currently highlighted event.
        if self.current is None:
            self.line(self.lifepath.first[self.selected][1])
        else:
            if self.current.choices is not None:
               self.cline(eventdata.get(self.current.choices[self.selected], {'text': '<DEBUG: NO TEXT>'})['text'])

        # Bottom part of the screen:
        self.y_acc = self.height - 8
        y_save = self.y_acc

        # START HEXAGONS
        # Show choices in a pretty hexagon!
#        hex_size = 3
#        width = 1 + hex_size * 3 * 2
#        center = width / 2

#        self.x_acc = center
#        self.y_acc = hex_size*3

        def hex_reset(x):
            self.x_acc = center
            self.y_acc = y_acc+1 + hex_size*3
            #self.rds((center, y_acc), "X")
            if x >= len(dirs):
                dir = CC
            else:
                dir = dirs[x]
            self.x_acc += hex_size*(2*dir[0] + dir[1])
            self.y_acc += 2*hex_size*dir[1] - (1+(hex_size-1)/3)*dir[1]

        def hexagon(size, color=None):
            x, y = self.x_acc, self.y_acc
#center
#                x = 2*pos[0] + pos[1]
#                y = pos[1]
            for offset in range(size+1):#/2+1):
                #f
                if offset == 0:
                    self.rd((x-size, y), "|", color)
                    self.rd((x+size, y), "|", color)
                elif offset <= size/3:
                    extra = 0#offset#size/3
                    self.rd((x-size, y-offset-extra), "|", color)
                    self.rd((x+size, y-offset-extra), "|", color)
                    self.rd((x-size, y+offset+extra), "|", color)
                    self.rd((x+size, y+offset+extra), "|", color)
                elif offset > 0:
                    self.rd((x+offset - size-size/3, y-offset), "/", color)
                    self.rd((x-offset + size+size/3, y+offset), "/", color)
                    self.rd((x-offset + size+size/3, y-offset), "\\", color)
                    self.rd((x+offset - size-size/3, y+offset), "\\", color)
            self.x_acc -= size-1

        # Draw the empty hexes.
        #for x in range(len(self.choices), 6):
        #    hex_reset(x)
        #    hexagon(hex_size, "cyan-black")

#        for x in range(len(self.choices)):
        # TODO: Split this off into its own function.
#            if x == self.selector.choice:
#                continue
#            hex_reset(x)
            #hexagon(hex_size)
#            string = self.lifepath.name(self.choices[x])
#            for word in re.split('\W', string):
#                self.line("%s" % word)

#                self.cline("<green-black>* %s</>" % choice)
#                 self.cline("<green-black>*</>")
#            else:
#                 self.line("*")

        # Draw the selected hex.
#        hex_reset(self.selector.choice)
#        hexagon(hex_size, "green-black")
#        string = self.lifepath.name(self.choices[self.selector.choice])
#        for word in re.split('\W', string):
#            self.cline("<green-black>%s</>" % word)

        # Restore to previous values.
#        self.x_acc = x_acc + width + 5
#        self.y_acc = y_acc + 5

        # END HEXAGONS

        # Print a list of choices for the initial skip.
        if self.current is None:
            # Start with just enough room to list everything and save where we started.
            for x in range(len(self.lifepath.skip)):
                if x == self.selected:
                    self.cline("<green-black>* %s</>" % self.lifepath.skip[x][0])
                else:
                    self.line("* %s" % self.lifepath.skip[x][0])
        # Prints a list of choices for the current event.
        elif self.current.choices is not None:
            for choice in self.current.choices:
                if self.current.choices[self.selected] == choice:
                    self.cline("<green-black>* %s</>" % choice)
                else:
                    self.line("* %s" % choice)
        # Prints the final choice: whether to start.
        else:
            self.y_acc = self.height-1
            self.cline("<red-black>Really use this lifepath? You can't change it once you've started the game.</>")

        # Go back up to where we started, but this time, to the right.
        self.y_acc = y_save
        self.x_acc = 25

        if self.toggle_events is True:
            self.x_acc = 0
            self.y_acc = self.height / 3
            self.cline("%s" % "-"*self.width)
            self.cline("Your life so far:")
            self.cline("")
            line = ""
            for event in self.lifepath.events:
                # We only want events with short descriptions. If they take a certain number of years, list that.
                if event.short is not None:
                    string = "%s" % event.short
                    if event.years is not None:
                        string += " "
                        if event.years == 1:
                            string += "(%s year)" % event.years
                        else:
                            string += "(%s years)" % event.years
                    line += string+" -> "
            line += "?\n"
            self.cline(line)
            self.y_acc += 4
            self.cline("%s" % "-"*self.width)

        # Don't draw anything else.
        return False

    # TODO: Duplicated code.
    def keyin(self, c):
        # Show a list of events so far.
        if c == ord('?'):
            if self.toggle_events is True:
                self.toggle_events = False
            else:
                self.toggle_events = True
            return False
        # Make the first choice, which uses a different system to
        # skip ahead several steps in the chargen system.
        if self.current is None:
            if c == curses.KEY_ENTER or c == ord('\n'):
                # TODO: Move this into lifepath code!
                # Each particular skip choice comes with a predetermined list of choices to make.
                choices = self.lifepath.skip[self.selected][2]
                # Everyone starts at Start.
                self.next('Start')
                # After that, follow the choices.
                for choice in choices:
                    self.next(choice)
            elif c == curses.KEY_UP:
                self.scroll(-1)
            elif c == curses.KEY_DOWN:
                self.scroll(1)
            else: return True
            return False
        # Choicely choosing the next choice from choices
        elif self.current.choices is not None:
            if c == curses.KEY_ENTER or c == ord('\n'):
                self.next()
            elif c == ord(' '):
                self.prev()
            elif c == curses.KEY_UP:
                self.scroll(-1)
            elif c == curses.KEY_DOWN:
                self.scroll(1)
            else: return True
            return False
        # Last stage: choosing whether to start the game or not.
        else:
            if c == curses.KEY_ENTER or c == ord('\n'):
                self.suicide()
            elif c == ord(' '):
                self.prev()
            else: return True
            return False

