"""Provides functionality for Agents to contain other Agents (typically items) inside of themselves."""

from src.lib.agents.components.component import Component

from src.lib.util import debug
from src.lib.util.registry import RegistryFactory, RegistryDict, RegistryList
from src.lib.util.result import accumulate_results, ignore_results
from src.lib.util.trait import Trait

"""Components."""

class Containing(Component):
    """Allows an Agent to contain other Agents inside of itself."""
    commands = []

    def __init__(self, owner):
        self.contents = {}
        self.owner = owner

    """Content getter methods."""

    @accumulate_results
    def get_contents(self):
        """Yield keyed lists of Agents inside the Container."""
        for key, itemlist in self.contents.items():
            yield ((key, itemlist))

    @accumulate_results
    def get_list(self):
        """Yield a flat list of Agents inside the Container."""
        for itemlist in self.contents.values():
            for item in itemlist:
                yield item

    """Content setter methods."""

    def add_contents(self, agent):
        """Add an Agent to a keyed list in this Container."""
        matches = self.contents.get(agent.appearance(), [])

        # This covers only the case of that exact item already being in container.
        if agent in matches: debug.die("Tried to add agent %s to container %s." % (agent, self))

        matches.append(agent)
        self.contents[agent.appearance()] = matches

        return True

    def remove_contents(self, agent):
        """Remove an Agent from a keyed list in this Container."""
        matches = self.contents.get(agent.appearance(), [])

        # This covers only the case of that exact item already being in container.
        if agent not in matches: debug.die("Tried to remove agent %s from container %s." % (agent, self))

        matches.remove(agent)
        if matches:
            self.contents[agent.appearance()] = matches
        else:
            del self.contents[agent.appearance()]

        return True

    """Content utility methods."""

    def count_contents(self):
        """Return the number of Agents inside this Container."""
        return len([agent for agent in self.get_list()])

"""Traits."""

class ContainerException(Exception):
    """An exception raised while using an `Agent` as a `Container`."""
    pass

class CouldNotContainException(ContainerException):
    """An exception raised when a `Container` tries to add something it could not contain."""
    pass

class CanNotContainException(ContainerException):
    """An exception raised when a `Container` tries to add something it cannot currently contain."""
    pass

class DoesNotContainException(ContainerException):
    """An exception raised when a `Container` tries to remove something it does not currently contain."""
    pass

# A registry for the contents of a Container.
ContentRegistry = RegistryFactory("ContentRegistry", RegistryList)

class Container(Trait):
    """Provides methods to manage contents."""
    contents_class = ContentRegistry

    @Trait.include
    def __init__(self, *args, **kwargs):
        """Set self's contents."""
        Trait.super(Container, self).__init__(*args, **kwargs)
        self.contents = kwargs.pop("contents", [])

    @property
    def contents(self):
        return self._contents

    @contents.setter
    def contents(self, values):
        self._contents = self.contents_class(values) if values is not None else contents_class()

    """Content validation methods."""

    def could_contain(self, other):
        """Return whether self could contain other."""
        return True

    def can_contain(self, other):
        """Return whether self can currently contain other."""
        return True

    def does_contain(self, other):
        """Return whether self currently contains other."""
        return other in self.contents

    """Content modification methods."""

# A registry for sections within a SectionedContainer.
SectionRegistry = RegistryFactory("SectionRegistry", RegistryList)

# A registry for the contents of sections within a SectionedContainer.
SectionContentRegistry = RegistryFactory("SectionContentRegistry", RegistryDict, container_class=RegistryList)

class SectionedContainer(Container):
    contents_class = SectionContentRegistry

    @Trait.include
    def __init__(self, *args, **kwargs):
        """Set self's contents."""
        self.sections = kwargs.pop("sections")
        Trait.super(SectionedContainer, self).__init__(*args, **kwargs)

    @property
    def sections(self):
        return self._sections

    @sections.setter
    def sections(self, values):
        self._sections = SectionRegistry()

    # TODO: Test whether this works
    @Container.contents.setter
    def contents(self, values):
        self._contents = self.contents_class()
        for value in values:
            section = self.choose_section(value)
            if not section in self.sections:
                raise CouldNotContainException, "There was no appropriate section for that content."
            self._contents[section] += value
