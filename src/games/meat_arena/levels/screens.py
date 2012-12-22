from src.lib.views.screens import Screen
from src.lib.data import screens

# TODO: Split this out later.
class StartScreen(Screen):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        Screen.__init__(self, window, x, y, start_x, start_y)

    def draw(self):
        self.border(" ")
        title = "<%s>%s</>" % ("red-black", "Welcome to the Arena!")
        spacing = self.width - len("Welcome to the Arena!") - len(self.player.location)
        heading = "%s%s%s" % (title, " "*spacing, self.player.location)
        self.cline(heading)
        self.cline("-"*(self.width))
        self.cline(screens.text["start-meat"])
        self.y_acc = self.BOTTOM
        self.cline("Press <green-black>Enter</> to continue. Press <green-black>'?'</> for help at any time.")
        return False
