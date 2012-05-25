from views.screens import Screen
from data import help

class HelpScreen(Screen):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        Screen.__init__(self, window, x, y, start_x, start_y)

    def draw(self):
        self.border(" ")
        title = "<%s>%s</>" % ("green-black", "Help!")
        spacing = self.width - len("Help!") - len(self.player.location)
        heading = "%s%s%s" % (title, " "*spacing, self.player.location)
        self.cline(heading)
        self.cline("-"*(self.width))
        self.cline(help.entry["commands"])
        self.y_acc = self.BOTTOM
        self.cline("Press <green-black>Enter</> to continue. Press <green-black>'?'</> for help at any time.")
        return False
