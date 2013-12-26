"""Text manipulation methods."""

# TODO: Rewrite this heavily...
from src.lib.util.define import *

import re
import functools

def affix(prefix="", suffix=""):
    """Decorator to add prefixes or suffixes to a string."""
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            return prefix + fn(*args, **kwargs) + suffix
        return wrapper
    return decorator

def indent(fn):
    """Decorator to handle indenting lines of text."""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        kwargs.setdefault("indenter", Indenter())
        result = fn(*args, **kwargs)
        if isinstance(result, basestring):
            try:
                result = kwargs["indenter"].get_indent() + result
            except AttributeError:
                exit("indent failed: {}".format(kwargs))
        else:
            result = [kwargs["indenter"].get_indent() + line for line in result]
        if kwargs["indenter"].wrap_depth > 0:
            kwargs["indenter"].unindent().wrap_depth -= 1
        return result
    return wrapper

def join(string):
    """Decorator to join the results of a function by a string."""
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            return string.join(fn(*args, **kwargs))
        return wrapper
    return decorator

def first(character, string):
    """Return the position of the first occurence of a character in a string."""
    for i in xrange(len(string)):
        if string[i] == character:
            return i

def replace(pattern, replacement, string):
    return re.sub(pattern, replacement, string)

# Strip tags out of a string. Used to calculate the length of strings with tags.
def striptags(string):
    return re.sub('(<.*?>)', '', string)

# Return a string with appropriate punctuation.
def commas(list, capitalize=False):
    str = ""
    spacer = " "

    for x in range(len(list)):
        if len(list) > 2 and x > 0:
            str += ","
        if len(list) > 1 and x == len(list)-1:
            str += spacer + "and"
        if x > 0:
            str += spacer
        try:
            str += list[x]
        except TypeError:
            exit([str, list, x])

    if capitalize is True:
        str = str.capitalize()
    return str

# TODO: This is duplicated code from rdl
def wrap_string(text, width, indent=1):
    list = []
    for line in text:
        if len(line) > width:
            string = ""
            words = re.split('(\s+)', line)

            for word in words:
                if len(word) + len(string) > width:
                    list.append(string)
                    string = " "*indent
                if string.isspace() is True and word.isspace() is True:
                    continue
                string += word
        else:
            string = line
        list.append(string)
    return list

# DEBUG: Print dictionaries a bit more nicely.
def print_dict(name, dict):
    print "--%s--" % name
    for k,v in dict.items():
        print "| %s: %s" % (k,v)
    print "--%s--" % ("-" * len(name))

def tag(string, tag):
    """Wrap a string with a tag."""
    return "<%s>%s</>" % (tag, string)

def highlight(string, fg=HIGHLIGHT, bg=BACKGROUND):
    """Highlight a string."""
    return tag(string, fg+"-"+bg)

def highlight_range(string, start=0, stop=0, fg=HIGHLIGHT, bg=BACKGROUND):
    """Convenience function for highlighting a range within a string."""
    return string[0:start] + highlight(string[start:stop], fg, bg) + string[stop:len(string)]

def highlight_substr(string, substr, fg=HIGHLIGHT, bg=BACKGROUND):
    """Convenience function for highlighting a substring within a string."""
    match = re.search(substr, string)
    return highlight_range(string, *match.span(), fg=fg, bg=bg) if match else string

# TODO: Rewrite this...
# def highlight_substrs(string, substr, fg=HIGHLIGHT, bg=BACKGROUND, match_limit=None):
#     """Convenience function for highlighting substrings within a string."""
#     matches = re.finditer("substr", string)
#     highlights = []
#     for match in matches:
#         if match_limit and match_limit > 0:
#             match_limit -= 1
#         highlights.append(match.span())
#     return highlight_range(string, *highlights)

def highlight_first(string, fg=HIGHLIGHT, bg=BACKGROUND):
    """Convenience function to highlight the first letter of a string."""
    return highlight(string[0]) + string[1:]

class Indenter(object):
    def __init__(self, level=0, pattern=" ", width=3, left="", right="", left_partials=True):
        self.indent_levels = [level]
        self.wrap_depth = 0

        self.pattern = pattern
        self.width = width
        self.left = left
        self.right = right
        self.left_partials = left_partials

    def indent(self, levels=1):
        if levels <= 0: debug.die("Tried to indent 0 or fewer levels.")
        self.indent_levels.append(levels)
        return self

    def unindent(self, levels=1):
        self.indent_levels = self.indent_levels[:-levels]
        if not self.indent_levels: debug.die("Tried to indent 0 or fewer levels.")
        return self

    def get_indent_level(self):
        return sum(self.indent_levels)

    def get_indent(self):
        indent_level = self.get_indent_level()
        if indent_level <= 0:
            return ""

        width = indent_level * self.width - len(self.left) - len(self.right)

        if width < 0:
            debug.die('Not enough room to generate an indent like: "%s" + "%s" * ~%i + "%s"' % (self.left, self.pattern, width / len(self.pattern), self.right))

        complete_patterns = width / len(self.pattern)
        remaining_width = width % len(self.pattern)

        return self.left + (self.pattern[:remaining_width] if self.left_partials else "") + (self.pattern * complete_patterns) + (self.pattern[:-remaining_width] if not self.left_partials else "") + self.right

    def wrap_indent(self, levels=1):
        self.indent(levels)
        self.wrap_depth += 1
        return self

def repr_instance(instance, **kwargs):
    return "<%s at %s>" % (instance.__class__.__name__, hex(id(instance)))

def repr_function(function, **kwargs):
    try:
        return "%s.%s()" % ((repr_instance(function.im_self) if hasattr(function, "im_self") else "<unbound>"), \
            (function.__name__ if hasattr(function, "__name__") else function.__class__.__name__))
    except AttributeError:
        debug.die(dir(function))

@affix(prefix="---", suffix="---")
def repr_header(instance, **kwargs):
    return repr_instance(instance, **kwargs)

def repr_arguments(pos_args, kw_args, **kwargs):
    return ["args[%d]: %s" % (i, repr(pos_args[i])) for i in range(len(pos_args))] + ["kwargs[%s]: %s" % (repr(k), repr(v)) for k,v in kw_args.items()]

#@indent
# def repr_called(caller, called, *args, **kwargs):
#     result = repr_callable(caller, called)
#     result += "("
#     result += ", ".join(args)
#     result += ", ".join(["%s=%s" % (repr(k), repr(v)) for k,v in kwargs.items()])
#     result += ")"
#     return result