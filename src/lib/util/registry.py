"""Defines registry container classes."""

from src.lib.util.o_dict import OrderedDict

class RegistryContainerMixin(object):
    """A mixin that defines a class as a registry container."""
    container_class = None

    @property
    def container(self):
        """Return a new instance of this registry container's container class."""
        return self.container_class()

    @container.setter
    def container(self, value):
        """Set this registry container's container class, if possible."""
        assert not any(self), "Tried to change the container class of a RegistryDict with existing contents: %s" % self
        self.container_class = value

# TODO: RegistrySet.
# class RegistrySet(RegistryContainerMixin, set):
#     pass

class RegistryList(RegistryContainerMixin, list):
    """A list of entries in a registry."""
    def __init__(self, *args):
        """Set this Registry's container class and then instantiate it with the remaining arguments."""
        list.__init__(self, args)

    def __repr__(self):
        """Display as `Classname[value, ...]` when printed."""        
        return self.__class__.__name__ + list.__repr__(self)

    def __iadd__(self, other):
        """Override `+=` to append an entry to a RegistryList."""
        # Check via type() rather than isinstance() so that subclasses of
        # a RegistryList will be appended as an instance rather than combined
        # element-wise.
        if type(self) == type(other):
            # TODO: Fix logic here to prevent dupes.
            self.extend(other)
        else:
            self.append(other)
        return self

    def __isub__(self, other):
        """Override `-=` to safely remove an entry from a RegistryList."""
        # Check via type() rather than isinstance() so that subclasses of
        # a RegistryList will be checked for removal as an instance rather than
        # filtered out element-wise.
        if type(self) == type(other):
            for entry in other:
                self -= entry
            return self
        else:
            try:
                self.remove(other)
            finally:
                return self

class RegistryDict(RegistryContainerMixin, OrderedDict):
    """An ordered dictionary that stores values in instances of a container class."""
    def __init__(self, *args, **kwargs):
        """Set this Registry's container class and then instantiate it with the remaining arguments."""
        OrderedDict.__init__(self, *args, **kwargs)

    def __repr__(self):
        """Display as `Classname{'key': value, ...}` when printed."""
        return self.__class__.__name__ + "{" + ", ".join(["'{0}': {1}".format(*x) for x in self.items()]) + "}"

    def __setitem__(self, key, val):
        # Check via type() rather than isinstance() so that subclasses of the
        # container class will be wrapped.
        if self.container_class and type(val) != self.container_class:
            val = self.container_class(val)
        OrderedDict.__setitem__(self, key, val)

    def __missing__(self, key):
        """Return a new instance of this RegistryDict's container class when a missing key is used to index into it."""
        return self.container

def RegistryContainerFactory(name, cls, **attributes):
    return type(name, (cls,), attributes)