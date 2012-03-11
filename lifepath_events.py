# Contains all lifepath events.
# 'age' (int)       : Age category the event fits into. Also broken up by comments.
# 'name' (str)      : Display name during character generation. Defaults to key name.
# 'text' (str)      : Display text during character generation.
# 'short' (str)     : Alternate short text during character dumps.
# 'effects' (dict)  : Dictionary of skill/advantage changes caused by the event.
# 'years' (int)     : Number of years the event takes duirng character generation.
# 'choices' (tuple) : Tuple of choices for progression from this lifepath.
eventdata = {
# Start of data
# Age 0: Parents (~-9 months old)
'Wizards' : {
    'age'     : 0,
    'text'    :  "I was a child of a mighty wizard.",
    'short'   : "Your parents were mighty wizards.",
    'effects' : {'MP': 1, 'IQ': 2, 'Magery': 1},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Wizards' : {
    'age'     : 0,
    'text'    :  "I was a child of a mighty wizard.",
    'short'   : "Your parents were mighty wizards.",
    'effects' : {'MP': 1, 'IQ': 2, 'Magery': 1},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Wizards' : {
    'age'     : 0,
    'text'    :  "I was a child of a mighty wizard.",
    'short'   : "Your parents were mighty wizards.",
    'effects' : {'MP': 1, 'IQ': 2, 'Magery': 1},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Wizards' : {
    'age'     : 0,
    'text'    :  "I was a child of a mighty wizard.",
    'short'   : "Your parents were mighty wizards.",
    'effects' : {'MP': 1, 'IQ': 2, 'Magery': 1},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
# Age 1: Birth (0 years old)

# Age 2: Early Childhood (~2 years old)

# Age 3: Childhood (~8 years old)

# Age 4: Teenager (~14 years old)

# Age 5: Young Adult (~20 years old)

# Age 6: Adult (>25 years old)

# Age 7: Middle Age (>40 years old)
# Not supported at this time
# Close of data
}
