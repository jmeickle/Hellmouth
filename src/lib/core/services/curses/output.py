import curses

from src.lib.core.services.service import ServiceMixin

class CursesOutputService(ServiceMixin):
    """Service providing curses output. Used as a context manager."""
    def __init__(self):
        self.color = True

        self.display = None
        self.mode = False

    """Curses context management methods."""

    def __enter__(self):
        """Start displaying using curses."""
        # If there isn't a stored curses display, initialize curses and set one.
        if not self.display:
            self.set_display()

        # # Save the current "shell" terminal mode.
        # curses.def_shell_mode() 

        # Restore the previous "program" terminal mode if possible. Otherwise, set it.
        # curses.reset_prog_mode() if self.mode else self.set_mode()
        self.set_mode()

        # Return the curses display.
        return self.display

    def __exit__(self, exception_type, exception_val, trace):
        """Stop displaying using curses."""
        # Save the current "program" terminal mode.
        # curses.def_prog_mode()
        # self.mode = True

        # Restore the previous "shell" terminal mode.
        # curses.reset_shell_mode()

        # Mode unset
        self.unset_mode()

        # End curses
        curses.endwin()

        # Print the stack trace if an exception occurred.
        # if exception_type:
        #     print str(trace)#.print_exc()

    """Curses helper methods."""

    def set_display(self):
        """Initialize curses and configure the returned display."""
        # assert curses.isendwin(), "Tried to initialize curses when already initialized."
        assert not self.display, "Tried to set the curses display when already set."

        # Initialize curses.
        self.display = curses.initscr() 

        # Initialize colors.
        if self.color:
            curses.start_color()
            from src.lib.util.color import Color

        # Enable the display's interpretation of special keys.
        self.display.keypad(1) 

    def set_mode(self):
        """Set the terminal mode."""
        # turns on cbreak mode
        # turns off echo
        # enables the terminal keypad
        # initializes colors if the terminal has color support.
        curses.raw() # Use raw input mode. / # curses.cbreak() # Disable keyboard buffering
        curses.noecho() # Disable key echoing.
        curses.curs_set(0) # Disable cursor visibility.

    def unset_mode(self):
        """Unset the terminal mode."""
        # restores cooked mode
        # turns on echo
        # disables the terminal keypad.
        curses.nocbreak() # Return to "cooked" input mode.
        curses.echo() # Enable key echoing.
        curses.curs_set(1) # Enable cursor visibility.

    # def reset(self):
    #     """Deinitialize curses."""
    #     assert not curses.isendwin(), "Tried to deinitialize curses when not already initialized."
    #     assert self.display, "Tried to delete the curses display when not already set."        
    #     curses.endwin()
    #     del self.display