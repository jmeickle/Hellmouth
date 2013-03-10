"""Defines a result object."""

import functools

class Result(object):
    def __init__(self, *args, **kwargs):
        self.results = []

    def describe(self):
        yield "%s called: %s.%s%s:\n" % (self.caller, self.method, self.domain, self.args)
        yield "\n"
        yield "Result: %s" % self.results

    def get_text(self):
        text = ""
        for line in self.describe():
            text += line
        return text

    """Result getter methods."""

    def get_outcome(self):
        """Get the overall outcome of this Result."""
        assert False, "Unimplemented!"

    def get_result(self):
        """Get a single result from this Result."""
        for result in self.results:
            return result

    def get_results(self):
        """Get all results in this Result."""
        return self.results

    """Result setter methods."""

    def add_result(self, result):
        if self.can_add_result():
            self.results.append(result)
            return True
        return False

    """Result helper methods."""

    def can_add_result(self):
        return True

# TODO: MultiResult?
class ActionResult(Result):
    def get_outcome(self):
        if not self.results:
            return False, "failure"
        else:
            for outcome, cause in self.results:
                if not outcome:
                    return outcome, cause
        return True, "success"

# TODO: Remove?
class CommandResult(ActionResult):
    pass

class SingleResult(Result):

    """Result getter methods."""

    def get_outcome(self):
        return self.results

    def get_results(self):
        return [self.results]

    """Result setter methods."""

    def add_result(self, result):
        if self.can_add_result():
            self.results = result
            return True
        return False

    """Result helper methods."""

    def can_add_result(self):
        if not self.results:
            return True
        return False

def accumulate_results(fn):
    """Decorator function for calls that accumulate results."""
    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        results = kwargs.pop('results', None)
        result = fn(self, *args, **kwargs)
        if results:
            results.update(result)
        return result
    return wrapper

def ignore_results(fn):
    """Decorator function for calls that ignore results so far."""
    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        results = kwargs.pop('results', None)
        return fn(self, *args, **kwargs)
    return wrapper

def single_results(fn):
    """Decorator function for methods that won't be called if there is a result already."""
    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        results = kwargs.pop('results', None)
        if not results:
            return fn(self, *args, **kwargs)
        elif results.can_update():
            result = fn(self, *args, **kwargs)
            results.update(result)
            return result
    return wrapper