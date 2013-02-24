"""Defines a result object."""

class Result(object):
    def __init__(self, caller, domain, operation, method, args):
        self.results = []
        self.caller = caller
        self.domain = domain
        self.operation = operation
        self.method = method
        self.args = args

    def update(self, result):
        self.results.extend(result)

    def describe(self):
        yield "%s called: %s.%s%s:\n" % (self.caller, self.method, self.domain, self.args)
        yield "\n"
        yield "Result: %s" % self.results

    def get_text(self):
        text = ""
        for line in self.describe():
            text += line
        return text

    def parse(self):
        if not self.results:
            return False
        #exit(self.get_text())

class CommandResult(Result):
    def __init__(self, caller, command, scope):
        self.results = []
        self.caller = caller
        self.command = command
        self.scope = scope

    def update(self, result):
        self.results.append(result)

    def parse(self):
        if not self.results:
            return "failure", False
        else:
            for method, result in self.results:
                if not result:
                    return method, result
        return "success", True