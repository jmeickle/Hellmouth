from data import help
from data import screens
from views.screens import Screen

class HelpScreen(Screen):
    def __init__(self, window):
        Screen.__init__(self, window)

    # TODO: Header drawing should be nicer.
    def draw(self):
        self.border(" ")
        title = "Help!"
        heading = "<green-black>%s</>" % title
        self.cline(heading)
        self.cline("-"*(self.width))
        self.cline(help.entry["commands"])
        self.y_acc = self.BOTTOM
        self.cline(screens.footer_back)
        return False

    def keyin(self, c):
        if c == ord(' '):
            self.suicide()
        return False
