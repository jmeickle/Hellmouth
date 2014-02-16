"""A pure Python implementation of a trait-like mechanism for class composition."""

import collections
import functools
import inspect
import itertools
import types

from src.lib.util import debug
from src.lib.util.decorator import classproperty
from src.lib.util.registry import RegistryFactory, RegistryDict, RegistryList

class TraitError(Exception):
    """An error related to `Trait`s."""
    pass

# A registry for the Trait-composed attributes in a Traitable class.
TraitAttributeRegistry = RegistryFactory("TraitAttributeRegistry", RegistryDict)

# A registry for the Traits in a Traitable class.
TraitRegistry = RegistryFactory("TraitRegistry", RegistryList)

class Trait(object):
    """A `Trait` is a reusable unit of behavior that is applied to classes via
    composition rather than inheritance. Composition and inheritance are orthogonal:
    a `Trait` may be defined using inheritance, a subclass may be defined using
    composition, and a composed class may be inherited from.

    An example `Trait` definition:

    ```
        class Undead(Trait):
            # Attributes are composed into the class:
            strength = 2 

            # Decorated magic methods are too:
            @Trait.include
            def __init__(self):
                print "Boo!"

            # Other magic methods are not composed:
            def __repr__(self):
                return "A g-g-g-ghost!"

            # Class methods are composed into the class:
            def damage(self):
                return 23

            # Unless excluded with a decorator:
            @Trait.exclude
            def debug(self):
                assert 1 is 1, "Critical math error detected."

            # Properties are composed the same way that class methods are:
            @property
            def holiness(self):
                return "Unholy"

            # Static methods are never composed:
            @staticmethod
            def get_weaknesses():
                return ["holy water", "crosses", "chainsaws"]
    ```
    """

    @staticmethod
    def use(*traits):
        """Class decorator to indicate which traits a class should be composed with."""
        def wrapper(traitable):
            name = traitable.__name__
            bases = traitable.__bases__
            attributes = dict(traitable.__dict__) # __dict__ is normally a proxy.
            return Traitable(name, bases, attributes, traits)
        return wrapper

    def exclude(method):
        """Method decorator to indicate that a `Trait` method is non-composable.
        This is typically only used for complex base class definitions or debugging.
        """
        method.__composable__ = False
        return method

    # We have to exclude this method too, of course!
    exclude = staticmethod(exclude(exclude))

    @staticmethod
    def include(method):
        """Method decorator to indicate that a `Trait` method is composable. This
        is typically only required for magic methods.
        """
        method.__composable__ = True
        return method

    @staticmethod

    @classproperty
    @classmethod
    def __attributes__(cls):
        """Yield the composable attributes of a `Trait`."""
        for name, attribute in inspect.getmembers(cls):
            # Static methods are never composable:
            if isinstance(attribute, types.FunctionType):
                continue
            # Methods are composable unless they've been decorated with @Trait.exclude
            # or are magic methods not decorated with @Trait.include.
            if getattr(attribute, '__composable__', not name.startswith("__")):
                # Collect functions instead of unbound methods.
                # TODO: This probably fails with decorators?
                if hasattr(attribute, "im_func"):
                    attribute = attribute.im_func
                yield name, attribute

    @classmethod
    @exclude.__func__ # Necessary because Trait.exclude is still a staticmethod object here.
    def super(trait, cls, instance):
        """Return a proxy object that delegates method calls to a `Trait`, letting
        a `Traitable` class or instance bypass restrictions on calling another
        class's methods.

        When the provided class is a `Traitable`, the calls will use the provided
        `Trait`'s method:

        ```
            @Trait.use(Ghostly)
            class Ghost(Monster):
                def __init__(self, place_of_death):
                    self.haunt(place_of_death)
                    # Calls Ghostly.__init__(self):
                    Ghostly.super(Ghost, self).__init__()   
                    self.rattle_chains()
        ```

        When the provided class is a `Trait`, this method is similar to super()
        but uses the `Trait`'s MRO instead of the `Traitable`'s:

        ```
            class Ghostly(Undead):
                @Trait.include
                def __init__(self, spooky=True):
                    # Calls Undead.__init__(self):
                    Trait.super(Ghostly, self).__init__()
                    self.spooky = spooky
        ```
        """
        if issubclass(cls, Trait):
            return TraitSuperProxy(cls, instance)
        else:
            return TraitableSuperProxy(trait, cls, instance)

class Traitable(type):
    """A metaclass that modifies the class definition process to allow
    for composition using `Trait`s.

    To mark a class as `Traitable`, set its `__metaclass__` like so:

    ```
        class Monster(object):
            __metaclass__ = Traitable
    ```
    """

    def __new__(meta, name, bases, attributes, traits=tuple()):
        """Compose a new class and return it."""
        if traits:
            # Track trait attributes.
            trait_attributes = collections.defaultdict(list)
            for trait in traits:
                for attr_name, attr_value in trait.__attributes__:
                    trait_attributes[attr_name].append((trait, attr_value))

            # Determine whether any trait attributes are provided by multiple traits.
            overlap = dict(itertools.ifilter(lambda trait_attribute: len(trait_attribute[1]) > 1, trait_attributes.items()))

            # Determine whether any overlapping trait attributes have been left
            # unresolved by the class. If so, raise an exception.
            conflicts = list(itertools.ifilter(lambda trait_attribute: trait_attribute not in attributes, overlap))
            if conflicts:
                def print_conflicts(conflicts):
                    for conflict in conflicts:
                        yield conflict, ", ".join([t.__name__ for t, a in trait_attributes[conflict]])

                conflict_sources = "\n".join(["{}: {}".format(conflict, t) for conflict, t in print_conflicts(conflicts)])
                raise TraitError("Conflicts occurred during Traitable composition:\nClass: {}\nTraits: {}\nConflicts:\n{}".format(name, ", ".join(trait.__name__ for trait in traits), conflict_sources))

            # Update attributes.
            for attr_name, attr_traits in trait_attributes.items():
                if not attr_name in attributes:                
                    assert len(attr_traits) == 1, "Ended up with multiple traits providing this attribute."
                    attr_trait, attr_value = attr_traits[0]
                    attributes[attr_name] = attr_value

        # Create a new Traitable class.
        try:
            cls = type.__new__(meta, name, bases, attributes)
        except TypeError as e:
            def metaclasses(classes):
                return ["{}: {}".format(cls, cls.__metaclass__ if hasattr(cls, "__metaclass__") else "(no metaclass)") for cls in classes]

            message =  "\n".join([str(_) for _ in (
                "Metaclass: {}".format(meta),
                "Metaclass MRO:" + "\n  ".join([""] + metaclasses(meta.__mro__)),
                "Bases:" + "\n  ".join([""] + metaclasses(bases)),
                "Error message:\n  {}".format(e)
            )])

            raise TraitError("Failed to create a Traitable class ({}):\n".format(name) + message)

        # TODO: Reimplement TraitRegistry and TraitAttributeRegistry.
        # # The new class keeps a record of which traits it was composed with.
        # cls.__traits__ = TraitRegistry(*trait_attributes.keys())

        # # It also keeps a record of the attributes that were provided by those traits.
        # def unroll(ta):
        #     for trait, trait_attrs in trait_attributes.items():
        #         for trait_attr in trait_attrs:
        #             yield trait_attr, trait
        # cls.__traitattributes__ = TraitAttributeRegistry(unroll(trait_attributes))

        return cls

    def __init__(cls, name, bases, attributes, trait_attributes={}):
        """Initialize the new class via type()."""
        super(Traitable, cls).__init__(name, bases, attributes)

    # TODO: Find a way to reimplement this that works nicely with inheritance.
    # @staticmethod
    # def super(trait, instance):
    #     """Given a `Trait` class and a `Traitable` instance, return a proxy object
    #     that delegates method calls to the most recently inherited `Traitable` class
    #     that was composed using that `Trait`. Used like:

    #         Traitable.super(trait, self).__init__()

    #     In other words, this is the composition equivalent of the normal `super()`
    #     behavior. It lets a `Trait` define methods that refer to `Traitable` methods
    #     that would otherwise be overriden by composition.
    #     """ 
    #     # TODO: Support a given Trait showing up more than once in the MRO.
    #     # TODO: Confirm support for multiple inheritance.
    #     return TraitableSuperProxy(trait, instance)

# TODO: Inheritance? Generalized proxy class?
class TraitableSuperProxy(object):
    """A proxy class that lets a `Traitable` call a provided `Trait`'s method."""
    __slots__ = ["trait", "cls", "instance"]

    def __new__(base, trait, cls, instance):
        """Return a new proxy object."""
        proxy = object.__new__(base)
        proxy.trait = trait
        proxy.cls = cls
        proxy.instance = instance
        return proxy

    def __getattribute__(self, name):
        trait = object.__getattribute__(self, "trait")
        cls = object.__getattribute__(self, "cls")
        instance = object.__getattribute__(self, "instance")
        return getattr(trait, name).__get__(instance, trait)

class TraitSuperProxy(object):
    """A proxy class that lets a `Traitable` call a provided `Trait`'s method
    using that `Trait`'s MRO instead of its own.
    """
    __slots__ = ["cls", "instance"]

    def __new__(base, cls, instance):
        proxy = object.__new__(base)
        proxy.cls = cls
        proxy.instance = instance
        return proxy

    def __getattribute__(self, name):
        cls = object.__getattribute__(self, "cls")
        instance = object.__getattribute__(self, "instance")
        return getattr(super(cls, cls), name).__get__(instance, cls)