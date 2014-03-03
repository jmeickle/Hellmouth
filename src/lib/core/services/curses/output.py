from src.lib.core.services.service import Service

from src.lib.util import debug

class CursesOutputService(Service):
    """Service providing curses output. Used as a context manager."""
    def __init__(self, display):
        # TODO: Handle multiple displays.
        self.display = display

    def __enter__(self):
        """Tell the display to start using curses."""
        self.display.save_mode()
        self.display.set_mode()

    def __exit__(self, exception_type, exception_val, trace):
        """Tell the display to stop using curses."""
        debug.log("{}: {}".format(exception_type, exception_val))
        self.display.reset_mode()
        del self.display

    def react(self):
        self.display.draw()