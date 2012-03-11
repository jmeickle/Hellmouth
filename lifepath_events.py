# Contains all lifepath events.
# 'name' (str)      : Display name during character generation. Defaults to key name.
# 'text' (str)      : Display text during character generation.
# 'short' (str)     : Alternate short text during character dumps.
# 'effects' (dict)  : Dictionary of skill/advantage changes caused by the event.
# 'years' (int)     : Number of years the event takes duirng character generation.
# 'age' (int)       : Age category the event fits into.
# 'choices' (tuple) : Tuple of choices for progression from this lifepath.
eventdata = {
# Start of data
'Wizards' : {
    'name': "Wizards",
    'text' : "Your parents were mighty wizards.",
    'effects' : {'HP':5, 'ST':1},
    'choices': ('Warriors', 'Hugs', 'Drugs'),
},
'Warriors' : {
    'text' : "Your parents were fearsome warriors.",},
'Hugs' : {
    'text' : "You embraced the path of hugs.",},
'Drugs' : {
    'text' : "You embraced the path of drugs.",},
'Warriors' : {
    'text' : "Your parents were fearsome warriors.",},
# Close of data
}
