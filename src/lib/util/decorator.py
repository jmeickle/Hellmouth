"""Decorators not tied to a specific Unicursal module's functionality."""

class classproperty(property):
    """Extends the `@property` decorator to class methods."""
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()