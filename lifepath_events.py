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
'Start' : {
    'age'     : 0,
    'text'    : "Starting point of character generation, before any details are determined.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('Mundane Infant', 'Dark Omen', 'Strange Omen', 'Holy Day', 'Bloody Birth', 'Immediate Adoption'),
#    'choices' : ('Mundane Parents', 'Mundane Infant', 'Mundane Young Child', 'Mundane Child', 'Mundane Young Adult', 'Mundane Adult'),
},
# Age 0: Parents (~-9 months old)
'Mundane Parents' : {
    'age'     : 0,
    'text'    : "My parents were regular people like yourself.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('Mundane Infant', '', '', '', '', ''),
},
# Age 1: Infant (0 years old)
'Mundane Infant' : {
    'age'     : 1,
    'text'    : "My birth was exciting for my parents, but few others.",
    'effects' : {},
    'years'   : 2,
    'choices' : ('Mundane Young Child', '', '', '', '', ''),
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
    'text'    : "I was born on a holy day.",
    'effects' : {},
    'years'   : 2,
    'choices' : ('', '', '', '', '', ''),
},
'Bloody Birth' : {
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
    'choices' : ('Church Young Child', '', '', '', '', ''),
},
# FORK: Who raised you? ('Immediate Adoption')
'Church Young Child' : {
    'age'     : 2,
    'text'    : "My early years were uneventful.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
# Age 2: Young Child (~2 years old)
'Mundane Young Child' : {
    'age'     : 2,
    'text'    : "My early years were uneventful.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('Mundane Child', '', '', '', '', ''),
},
'Rich Young Child' : {
    'age'     : 2,
    'text'    : "I spent my early years swaddled in cloth-of-gold.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Poor Young Child' : {
    'age'     : 2,
    'text'    : "Even as an infant, I was deprived of what I needed in life.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Stolen Young Child' : {
    'age'     : 2,
    'text'    : "I was stolen away from my parents.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Orphaned Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth, my parents were brutally killed.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Odd Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
# FORK: Did you stay with who raised you? ('Immediate Adoption')
'Church Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
# FORK: What were you stolen by? ('Stolen Young Child')
'Changeling Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Cultist Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
# FORK: What killed your parents? ('Young Child')
'Pirate Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Bandit Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Wolf Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
# FORK: What kind of odd behaviors? ('Odd Young Child')
'Magical Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Bookish Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
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
    'choices' : ('Mundane Teen', '', '', '', '', ''),
},
'Rich Child' : {
    'age'     : 3,
    'text'    : "Fortune smiled upon me as a young child.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Poor Child' : {
    'age'     : 3,
    'text'    : "Fortune spat upon me as a young child.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Enlisted Child' : {
    'age'     : 3,
    'text'    : "I had an uneventful childhood.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Wild Child' : {
    'age'     : 3,
    'text'    : "Separated from the civilization of my birth, my upbringing was unusual indeed.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Odd Child' : {
    'age'     : 3,
    'text'    : "Even the few friends I had as a child considered me to be queer.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
# FORK: Who were you raised by? ('Immediate Adoption', enlisted or rescued)
# FORK: How were you wild? ('Wild Child')
# FORK: How were you odd? ('Odd Child')

# Age 4: Teen (~14 years old)
'Mundane Teen' : {
    'age'     : 4,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'effects' : {},
    'years'   : 1,
    'choices' : ('Mundane Young Adult', '', '', '', '', ''),
},
'Dedicated Teen' : {
    'age'     : 4,
    'text'    : "I turned my efforts to labor from a young age, and I learned much from my experiences.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Scoundrel Teen' : {
    'age'     : 4,
    'text'    : "I turned my efforts to sin from a young age, and I learned much from my experiences.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Enlisted Teen' : {
    'age'     : 4,
    'text'    :  "My years as a teenager were tumultuous - but who isn't that true of?",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Wild Teen' : {
    'age'     : 4,
    'text'    :  "My years as a teenager were tumultuous - but who isn't that true of?",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Odd Teen' : {
    'age'     : 4,
    'text'    :  "My years as a teenager were tumultuous - but who isn't that true of?",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
# FORK: How were you trained? ('Immediate Adoption', rescued, or enlisted)
# FORK: How were you wild? ('Wild Teen')
# FORK: How were you odd? ('Odd Teen')

# Age 5: Young Adult (~20 years old)
'Mundane Young Adult' : {
    'age'     : 5,
    'text'    : "My life was quiet as I grew into adulthood.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('Mundane Adult', '', '', '', '', ''),
},
'Rich Young Adult' : {
    'age'     : 5,
    'text'    : "My life was quiet as I grew into adulthood.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Poor Young Adult' : {
    'age'     : 5,
    'text'    : "My life was quiet as I grew into adulthood.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Enlisted Young Adult' : {
    'age'     : 5,
    'text'    : "My life was quiet as I grew into adulthood.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Wild Young Adult' : {
    'age'     : 5,
    'text'    : "My life was quiet as I grew into adulthood.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Odd Young Adult' : {
    'age'     : 5,
    'text'    : "My life was quiet as I grew into adulthood.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
# FORK: How were you trained? ('Immediate Adoption', rescued, or enlisted)
# FORK: How were you wild? ('Wild Young Adult')
# FORK: How were you odd? ('Odd Young Adult')

# Age 6: Adult (>25 years old)
'Mundane Adult' : {
    'age'     : 6,
    'text'    :  "As an adult, little troubled me.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('Demonslayer', '', '', '', '', ''),
},
'Rich Adult' : {
    'age'     : 6,
    'text'    :  "As an adult, little troubled me.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Poor Adult' : {
    'age'     : 6,
    'text'    :  "As an adult, little troubled me.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Enlisted Adult' : {
    'age'     : 6,
    'text'    :  "As an adult, little troubled me.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Wild Adult' : {
    'age'     : 6,
    'text'    :  "As an adult, little troubled me.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Odd Adult' : {
    'age'     : 6,
    'text'    :  "As an adult, little troubled me.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
# FORK: How were you trained? ('Immediate Adoption', rescued, or enlisted)
# FORK: How were you wild? ('Wild Adult')
# FORK: How were you odd? ('Odd Adult')

# FORK: How did you get into demon-slaying?
'Demonslayer' : {
    'age'     : 6,
    'text'    :  "In time, though, I was forced into a life on the road, slaying demons wherever I went.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('Reluctant Demonslayer', 'Vengeful Demonslayer', 'Zealous Demonslayer', 'Violent Demonslayer', 'Curious Demonslayer', 'Corrupt Demonslayer'),
},
'Reluctant Demonslayer' : {
    'age'     : 6,
    'text'    :  "I did not want to, but against the forces of darkness, what choice did I have?",
    'effects' : {},
    'years'   : 1,
    'choices' : ('End', '', '', '', '', ''),
},
'Vengeful Demonslayer' : {
    'age'     : 6,
    'text'    :  "I have seen too much bloodshed. I need to destroy the fiends before they hurt anyone else.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('End', '', '', '', '', ''),
},
'Zealous Demonslayer' : {
    'age'     : 6,
    'text'    :  "I don't regret leaving my life behind me. God himself called me to this task, and I will listen and obey.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('End', '', '', '', '', ''),
},
'Violent Demonslayer' : {
    'age'     : 6,
    'text'    :  "I plan to slay every one of those abominations. Even if they won't stay dead, I'll kill them until they get the picture.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('End', '', '', '', '', ''),
},
'Curious Demonslayer' : {
    'age'     : 6,
    'text'    :  "I didn't truly believe they existed - not at first - but now I have to learn more about them.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('End', '', '', '', '', ''),
},
'Corrupt Demonslayer' : {
    'age'     : 6,
    'text'    :  "The forces of darkness have vast... vast power. Power you wouldn't believe. It has to be studied.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('End', '', '', '', '', ''),
},
# End character generation.
'End' : {
    'age'     : -1,
    'text'    :  "Your character is ready to go.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
# Not supported at this time:
# Age 7: Middle Age (>40 years old)
# Close of data
}

def recurse(tree, eventname, depth):
    event = tree.get(eventname)
#    print "%s%s:" % (depth * 3 * " ", eventname),
#    print "%s%s" % ((depth+2) * 2 * " ", event["text"])
    print "%s%s:" % (depth * 3 * " ", eventname),
    print event["text"]

    for choice in event["choices"]:
        if choice != '':
            recurse(tree, choice, depth+1)

    # Print the last 
#    if more is False:
#            print "%s%s:" % (depth * 3 * " ", eventname),
#            print event["text"]

    if depth == 1:
        print "\n",

if __name__ == "__main__":

# Print all event names
#    for k, v in eventdata.iteritems():
#        print k

# Print a tree
    recurse(eventdata, "Start", 0)
