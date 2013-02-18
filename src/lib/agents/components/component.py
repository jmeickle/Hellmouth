"""A Component is a combination of state and functionality possessed by an Agent."""

class Component(object):
    dependencies = []
    """Mark a Component as having a dependency on another Component."""