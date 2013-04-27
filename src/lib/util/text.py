"""Text manipulation methods."""

# TODO: Rewrite this heavily...
from src.lib.util.define import *

import re

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
        str += list[x]

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