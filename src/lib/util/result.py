"""Defines a result object."""

import functools

class Result(object):
    def __init__(self, *args, **kwargs):
        self.results = []

    def update(self, result):
        self.results.append(result)
        return True

    def describe(self):
        yield "%s called: %s.%s%s:\n" % (self.caller, self.method, self.domain, self.args)
        yield "\n"
        yield "Result: %s" % self.results

    def get_text(self):
        text = ""
        for line in self.describe():
            text += line
        return text

    def get_result(self):
        if not self.results:
            return False

    def get_values(self):
        return self.results

class ActionResult(Result):
    pass

class CommandResult(Result):
    def __init__(self, *args, **kwargs):
        self.results = []

    def update(self, result):
        self.results.append(result)

    def get_result(self):
        if not self.results:
            return "failure", False
        else:
            for method, result in self.results:
                if not result:
                    return method, result
        return "success", True

class SingleResult(Result):
    def update(self, result):
        if not self.results:
            self.results = result
            return True
        return False

    def can_update(self):
        if not self.results:
            return True
        return False

    def get_result(self):
        return self.results

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