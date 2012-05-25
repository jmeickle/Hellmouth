from data import help
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
        self.cline("Press <green-black>Enter</> to continue. Press <green-black>'?'</> for help at any time.")
        return False
