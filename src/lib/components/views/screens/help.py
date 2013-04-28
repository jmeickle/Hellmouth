from src.lib.data import help, screens
from src.lib.components.component import override_defaults
from src.lib.components.views.screens.screen import Screen

class HelpScreen(Screen):
    @override_defaults
    def __init__(self, **kwargs):
        super(HelpScreen, self).__init__(**kwargs)

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

    def keyin(self, c):
        if c == ord('\n'):
            self.suicide()
            return False
        return True