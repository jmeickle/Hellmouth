from src.lib.data import help
from src.lib.data import screens
from src.lib.components.views.screens.screen import Screen

class HelpScreen(Screen):
    def __init__(self, window):
        Screen.__init__(self, window)
        self.prompt = True

    # TODO: Header drawing should be nicer.
    def draw(self):
        self.border(" ")
        title = "Help!"
        heading = "<green-black>%s</>" % title
        self.cline(heading)
        self.cline("-"*(self.width))
        self.cline(help.entry["commands"])
        self.y_acc = self.BOTTOM
        self.cline(screens.footer)#_back)
        return False

    def keyin(self, c):
        if c == ord('\n'):
            self.suicide()
        return False
