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
'Mundane Parents' : {
    'age'     : 0,
    'text'    : "My parents were regular people like yourself.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
# Age 1: Infant (0 years old)
'Mundane Infant' : {
    'age'     : 1,
    'text'    : "My birth was only as exciting as they normally tend to be.",
    'effects' : {},
    'years'   : 2,
    'choices' : ('', '', '', '', '', ''),
},
'Dark Omen' : {
    'age'     : 1,
    'text'    : "Dark omens troubled the day of my birth.",
    'effects' : {},
    'years'   : 2,
    'choices' : ('', '', '', '', '', ''),
},
'Strange Omen' : {
    'age'     : 1,
    'text'    : "Eerie signs were seen on the day of my birth.",
    'effects' : {},
    'years'   : 2,
    'choices' : ('', '', '', '', '', ''),
},
'Holy Day' : {
    'age'     : 1,
    'text'    : "I was born on a holy day!",
    'effects' : {},
    'years'   : 2,
    'choices' : ('', '', '', '', '', ''),
},
'Bloody Infant' : {
    'age'     : 1,
    'text'    : "I was born on the battlefield.",
    'effects' : {},
    'years'   : 2,
    'choices' : ('', '', '', '', '', ''),
},
'Immediate Adoption' : {
    'age'     : 1,
    'text'    : "I was given up right after birth - unwanted by my own mother.",
    'effects' : {},
    'years'   : 2,
    'choices' : ('', '', '', '', '', ''),
},
# Age 2: Young Child (~2 years old)
'Mundane Young Child' : {
    'age'     : 2,
    'text'    : "My early years were uneventful.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
# Age 3: Child (~8 years old)
'Mundane Child' : {
    'age'     : 3,
    'text'    : "I had an uneventful childhood.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
# Age 4: Teen (~14 years old)
'Mundane Teen' : {
    'age'     : 4,
    'text'    :  "My years as a teenager were tumultuous - but who isn't that true of?",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
# Age 5: Young Adult (~20 years old)
'Mundane Young Adult' : {
    'age'     : 5,
    'text'    : "My life was quiet as I grew into adulthood.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
# Age 6: Adult (>25 years old)
'Mundane Adult' : {
    'age'     : 6,
    'text'    :  "As an adult, little troubled me.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
# Not supported at this time:
# Age 7: Middle Age (>40 years old)
# Close of data
}
