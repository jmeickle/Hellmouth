from views.screens import Screen

class HelpScreen(Screen):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        Screen.__init__(self, window, x, y, start_x, start_y)

    def draw(self):
        import help
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

entry = {
"start-meat" : "\
As the daze of the teleport spell fades away, you realize that you are not \
where you - nor anyone - would want to be. Towering walls of meat glisten in \
the dim bioluminescent light. A side of beef sloughs off the nearest one as \
you watch. The scent of <red-black>blood</> is heavy in the air, and your boots sink into \
the ground-beef ominously.\
<br>\
<br>\
This is a grisly, gristly place. You must escape.",

"commands" : "\
Commands: \
<br>\
<br>\
<green-black>Enter</> can mean activate, confirm, or accept, whereas \
<green-black>Space</> means cancel or go back.\
<br>\
<br>\
You can move your character with the <green-black>hex keys</> on your number \
pad. These keys are also used for navigating hexagonal menus.\
<br>\
<br>\
The <green-black>arrow keys</> are used to scroll lists and navigate \
rectangular menus. You can usually use these keys even while taking actions \
with your character.\
<br>\
<br>\
Press <green-black>'v'</> to view your surroundings. You can press \
<green-black>Enter</> while viewing a creature to see its character sheet.\
<br>\
<br>\
Press <red-black>'Ctrl+q'</> at any time to quit the game. (There is no prompt!)",
}
