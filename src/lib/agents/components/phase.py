class Phase(object):
    """Phases within in Action."""
    def __init__(self, name, *required_arguments, **options):
        self.name = name
        """The name of this Phase."""
        self.required_arguments = required_arguments
        """The arguments required by this Phase."""
        self.required = options.pop("required", True)
        """Whether this Phase is required for completion of later Phases."""
        self.rollback = options.pop("rollback", True)
        """Whether this Phase has a corresponding rollback Phase."""