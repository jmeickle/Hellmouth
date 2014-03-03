from src.lib.data import help, screens
from src.lib.components.views.screens.screen import Screen

class HelpScreen(Screen):
    def __init__(self, **kwargs):
        super(HelpScreen, self).__init__(**kwargs)

    # TODO: Header drawing should be nicer.
    def draw(self, display):
        display.border(self, " ")
        title = "Help!"
        heading = "<green-black>%s</>" % title
        display.cline(self, heading)
        display.cline(self, "-"*(self.width))
        display.cline(self, help.entry["commands"])
        self.y_acc = self.bottom
        display.cline(self, screens.footer)

    def keyin(self, c):
        if c == ord('\n'):
            self.suicide()
            return False
        return True