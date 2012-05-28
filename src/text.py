import re

# Strip tags out of a string. Used to calculate the length of strings with tags.
def striptags(string):
    return re.sub('(<.*?>)', '', string)
