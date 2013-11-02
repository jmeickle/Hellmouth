"""An implementation of traits in pure Python.

TODO: Handle conflict resolution during composition.
"""

from abc import ABCMeta
import functools
import inspect
import itertools

from src.lib.util.decorator import classproperty
from src.lib.util.registry import RegistryFactory, RegistryDict, RegistryList

# A registry for the Trait-composed attributes in a Traitable class.
TraitAttributeRegistry = RegistryFactory("TraitAttributeRegistry", RegistryDict)

# A registry for the Traits in a Traitable class.
TraitRegistry = RegistryFactory("TraitRegistry", RegistryList)

class Trait(object):
    """A `Trait` is a reusable unit of behavior that is applied to classes via
    composition rather than inheritance. Composition and inheritance are orthogonal:
    a `Trait` may be defined using inheritance, a subclass may be defined using
    composition, and a composed class may be inherited from.

    Here are some examples of `Trait` composition:

    ```
        class Undead(Trait):
            # Becomes an attribute:
            strength = 2 

            # Becomes a method, but only because it is decorated:
            @composable
            def __init__(self):
                print "Wait, stop being spooky for a moment!"
                # Call a method from the instance's `Traitable` class:
                Traitable.super(Undead, self).__init__()
                print "OK, I'm back to being Undead!"

            # Does not become a method:
            def __repr__(self):
                return "A g-g-g-ghost!"

            # Becomes a method:
            def damage(self):
                return 23

            # Becomes a property:
            @property
            def holiness(self):
                return "Unholy"
    ```
    """

    def __new__(cls, traitable, traits):
        """Given a Traitable and a set of Traits, return a Trait-indexed dictionary
        of attribute names and values."""
        # TODO: Try to make this a little nicer to use.
        assert traits, "Tried to call Trait() with no provided Traits."

        attributes = {}
        attribute_names = set()

        for trait in sorted(traits):
            trait_attributes = dict(trait.__attributes__)
            overlap = trait_attributes.viewkeys() & attribute_names
            if not overlap:
                attributes[trait] = trait_attributes
                attribute_names.update(trait_attributes)
            else:
                assert False, "Conflict occurred during composition:\n  Composed attributes: {}\n  Trait attributes: {}\n  Overlap: {}".format(attributes, trait_attributes, overlap)
        return attributes

    @classproperty
    @classmethod
    def __attributes__(cls):
        """Yield the composable attributes of a `Trait`."""
        for name, attribute in inspect.getmembers(cls):
            # Skip magic methods unless they've been decorated with @composable.
            if not name.startswith("__") or hasattr(attribute, '__composable__'):
                # Collect functions instead of unbound methods.
                if hasattr(attribute, "im_func"):
                    attribute = attribute.im_func
                yield name, attribute

def composable(method):
    """Decorator to define a `Trait` method as composable. Typically only required
    for magic methods.
    """
    # TODO: Set on `method`, not `wrapper`?
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        return method(*args, **kwargs)
    wrapper.__composable__ = True
    return wrapper

class Traitable(ABCMeta):
    """An abstract base class that modifies the class definition process to allow
    for composition using `Traits`.

    To mark a class as `Traitable`, set its `__metaclass__` like so:

    ```
        from src.lib.util.trait import Traitable

        class Actor(object):
            __metaclass__ = Traitable
    ```
    """

    def __new__(meta, name, bases, attributes, trait_attributes={}):
        """Construct and return a new class."""
        assert not attributes or not trait_attributes, "Provided both attributes {} and trait attributes {} when creating a new Traitable class.".format(attributes, trait_attributes)

        # If this `Traitable` is being composed, flatten the dict of trait attributes.
        if trait_attributes:
            # This works because `return x or y` returns `y` if `x` is `None`.
            attributes = reduce(lambda x, y: x.update(y) or x, trait_attributes.values())

        # Create a new Traitable class.
        cls = type.__new__(meta, name, bases, attributes)

        # The new class keeps a record of which traits it was composed with.
        cls.__traits__ = TraitRegistry(*trait_attributes.keys())

        # It also keeps a record of the attributes that were provided by those traits.
        cls.__traitattributes__ = TraitAttributeRegistry({name: trait for name in attributes.keys() for trait, attributes in trait_attributes.items()})

        return cls

    def __init__(cls, name, bases, attributes, trait_attributes={}):
        """Initialize the new class via type()."""
        super(Traitable, cls).__init__(name, bases, attributes)

    def __or__(traitable, traits):
        """Override the `|` (bitwise OR) operator to compose a new `Traitable` class
        from an existing one and a set of `Trait`s.

        There are several ways to compose a new `Traitable` class:

        ```
            # UndeadActor is an unmodified subclass of Actor, except for any
            attributes composed from Undead:
            UndeadActor = Actor|{Undead}

            # Defining and instantiating the composed class in one line requires
            # parentheses due to operator precedence:
            undead_actor = (Actor|{Undead})(...)

            # Subclassing the composed class works as expected, even if the composition
            # takes place inside of the class definition:
            class Zombie(Actor|{Undead}):
                def __init__(self, ...):
                    print "Braaaaains!"
                    super(Zombie, self).__init__(...)

            # Trait composition can be combined with multiple inheritance:
            class ZombieBread(Actor|{Undead}, Item|{Edible}):
                def __init__(self, ...):
                    print "Graaaaains!"
                    super(ZombieBread, self).__init__(...)
        ```
        """
        assert isinstance(traits, set), "Tried to compose using a non-set: {}".format(traits)

        # TODO: Idempotency in defining composed Traitables.
        # TODO: This shouldn't be in Trait.__new__
        trait_attributes = Trait(traitable, traits)
        # TODO: Move this into a helper method.
        composed_name = "{trait_names}{traitable_name}".format(trait_names="".join([trait.__name__ for trait in traits]), traitable_name=traitable.__name__)
        return Traitable(composed_name, (traitable,), {}, trait_attributes)

    @staticmethod
    def super(trait, instance):
        """Given a `Trait` and a `Traitable` instance, return a proxy object that
        delegates method calls to the most recently inherited `Traitable` class
        that was composed using that `Trait`.

        In other words, this is the composition equivalent of the normal `super()`
        behavior. It lets a `Trait` define methods that refer to `Traitable` methods
        that would otherwise be overriden by composition.
        """ 
        # TODO: Support a given Trait showing up more than once in the MRO.
        # TODO: Support non-__init__ calls via a proxy class
        # TODO: Confirm support for multiple inheritance.
        for cls in instance.__class__.__mro__:
            if isinstance(cls, Traitable) and trait == cls.__traitattributes__.get('__init__'):
                return super(cls, instance)