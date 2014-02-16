"""Useful class pattern traits."""

from src.lib.util.trait import Trait

class Singleton(Trait):
    """A `Trait` that turns a class into a singleton."""
    _instance = None

    @Trait.include
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(cls, cls).__new__(cls, *args, **kwargs)
        return cls._instance