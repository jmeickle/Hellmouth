# TODO: Move test code to lifepath.py

# String to show for skipping to a point and what point to skip to.
# Mainly serves to prevent me from having to create dummy entries in the data.

skip = (('PARENTS', 'I can only believe that God chose me even before my birth.', 'Start'),
        ('BIRTH', 'It was from the moment of my birth that God saw fit to change my life.', 'Mundane Parents'),
        ('EARLY CHILDHOOD', 'I didn\'t feel the Hand of God upon my fate until I was a young child.', 'Mundane Infant'),
        ('CHILDHOOD', 'Not until I was a child.', 'Mundane Young Child'),
        ('TEENAGER', 'Not until I was a teenager.', 'Mundane Child'),
        ('YOUNG ADULT', 'Not until I was a young adult.', 'Mundane Teen'),
        ('ADULT', 'Not until I was an adult.', 'Mundane Young Adult'),
       )

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
    'age'     : -1,
    'text'    : "Starting point of character generation, before any details are determined.",
    'effects' : {},
    'years'   : 0,
    'choices' : ('Mundane Parents', 'Warrior Parents', 'Wizard Parents', 'Mysterious Parents'),
},
# Age 0: Parents (~-9 months old)
'Mundane Parents' : {
    'age'     : 0,
    'text'    : "My parents were regular people like yourself.",
    'short'   : "a normal family",
    'effects' : {},
    'choices' : ('Mundane Infant', 'Dark Omen', 'Strange Omen', 'Holy Day', 'Bloody Birth', 'Immediate Adoption'),
},
'Warrior Parents' : {
    'age'     : 0,
    'text'    : "My parents were skilled warriors.",
    'short'   : "heir to martial prowess",
    'effects' : {},
    'choices' : ('Mundane Infant', 'Dark Omen', 'Strange Omen', 'Holy Day', 'Bloody Birth', 'Immediate Adoption'),
},
'Wizard Parents' : {
    'age'     : 0,
    'text'    : "Both of my parents were powerful mages.",
    'short'   : "heir to magical power",
    'effects' : {},
    'choices' : ('Mundane Infant', 'Dark Omen', 'Strange Omen', 'Holy Day', 'Bloody Birth', 'Immediate Adoption'),
},
'Mysterious Parents' : {
    'age'     : 0,
    'text'    : "My parents never spoke of how it came to pass, but I was certainly no child of my father.",
    'short'   : "uncertain heritage",
    'effects' : {},
    'choices' : ('Mundane Infant', 'Dark Omen', 'Strange Omen', 'Holy Day', 'Bloody Birth', 'Immediate Adoption'),
},
# Age 1: Infant (0 to 1 years old)
'Mundane Infant' : {
    'age'     : 1,
    'text'    : "My birth was exciting for my parents, but few others.",
    'short'   : "a normal birth",
    'effects' : {},
    'years'   : 1,
    'choices' : ('Mundane Young Child', 'Rich Young Child', 'Poor Young Child', 'Stolen Young Child', 'Orphaned Young Child', 'Odd Young Child'),
},
'Dark Omen' : {
    'age'     : 1,
    'text'    : "Dark omens troubled the day of my birth.",
    'short'   : 'dark omens on the day of your birth',
    'effects' : {},
    'years'   : 1,
    'choices' : ('Mundane Young Child', 'Rich Young Child', 'Poor Young Child', 'Stolen Young Child', 'Orphaned Young Child', 'Odd Young Child'),
},
'Strange Omen' : {
    'age'     : 1,
    'text'    : "Eerie signs were seen on the day of my birth.",
    'short'   : 'strange omens on the day of your birth',
    'effects' : {},
    'years'   : 1,
    'choices' : ('Mundane Young Child', 'Rich Young Child', 'Poor Young Child', 'Stolen Young Child', 'Orphaned Young Child', 'Odd Young Child'),
},
'Holy Day' : {
    'age'     : 1,
    'text'    : "I was born on a holy day.",
    'short'   : 'your blessed birth on a holy day',
    'effects' : {},
    'years'   : 1,
    'choices' : ('Mundane Young Child', 'Rich Young Child', 'Poor Young Child', 'Stolen Young Child', 'Orphaned Young Child', 'Odd Young Child'),
},
'Bloody Birth' : {
    'age'     : 1,
    'text'    : "I was born on the battlefield.",
    'short'   : 'your birth on the chaos of the battlefield',
    'effects' : {},
    'years'   : 1,
    'choices' : ('Mundane Young Child', 'Rich Young Child', 'Poor Young Child', 'Stolen Young Child', 'Orphaned Young Child', 'Odd Young Child'),
},
'Immediate Adoption' : {
    'age'     : 1,
    'text'    : "I was given up right after birth - unwanted by my own mother.",
    'short'   : 'your parents giving you up',
    'effects' : {},
    'years'   : 1,
    'choices' : ('Mundane Young Child', 'Rich Young Child', 'Poor Young Child', 'Stolen Young Child', 'Orphaned Young Child', 'Odd Young Child'),
},
# FORK: Who raised you? ('Immediate Adoption')
'Church Young Child' : {
    'age'     : 2,
    'text'    : "My early years were uneventful.",
    'short'   : 'being raised by the church',
    'effects' : {},
    'years'   : 1,
},
# Age 2: Young Child (1 to 6 years old)
'Mundane Young Child' : {
    'age'     : 2,
    'text'    : "My early years were uneventful.",
    'short'   : 'an uneventful young childhood',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Child', 'Rich Child', 'Poor Child'),
},
'Rich Young Child' : {
    'age'     : 2,
    'text'    : "I spent my early years swaddled in cloth-of-gold.",
    'short'   : 'a young childhood in a wealthy family',
    'effects' : {},
    'years'   : 6,
},
'Poor Young Child' : {
    'age'     : 2,
    'text'    : "Even as an infant, I was deprived of life's necessities. Luxuries were unheard of.",
    'short'   : 'a young childhood spent in poverty',
    'effects' : {},
    'years'   : 6,
},
'Stolen Young Child' : {
    'age'     : 2,
    'text'    : "I was stolen away from my parents.",
    'short'   : 'theft from your parents',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Changeling Young Child', 'Cultist Young Child', 'Initiate Young Child'),
},
'Orphaned Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth, my parents were brutally killed.",
    'effects' : {},
    'years'   : 6,
},
'Odd Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'effects' : {},
    'years'   : 6,
},
# FORK: Who raised you? 
'Church Young Child' : {
    'age'     : 2,
    'text'    : "It was merely an accident of fate - unexpected, but not unusual.",
    'effects' : {},
    'years'   : 6,
},
# FORK: What were you stolen by? ('Stolen Young Child')
'Changeling Young Child' : {
    'age'     : 2,
    'text'    : "Faeries came from the deep wood and swapped one of their children for me.",
    'effects' : {},
    'choices' : ('Changeling Child', 'Rescued Child'),
},
'Cultist Young Child' : {
    'age'     : 2,
    'text'    : "Demon-worshipers saw something in me and took me as theirs. Perhaps I was intended to be a sacrifice, but was granted compassion for some reason.",
    'effects' : {},
    'choices' : ('Cultist Child', 'Rescued Child'),
},
'Initiate Young Child' : {
    'age'     : 2,
    'text'    : "My abductors were a fanatical religious order dedicated to slaying demons.",
    'effects' : {},
    'choices' : ('Initiate Child', 'Rescued Child'),
},
# FORK: What killed your parents? ('Orphaned Young Child')
'Pirate Young Child' : {
    'age'     : 2,
    'text'    : "My parents were attacked by black-hearted pirates. They slaughtered everyone, but even they couldn't bear to harm a helpless child.",
    'effects' : {},
    'choices' : ('Pirate Child', 'Rescued Child'),
},
'Bandit Young Child' : {
    'age'     : 2,
    'text'    : "My parents were attacked by bandits. My mother attempted to flee and they shot her where she stood. It wasn't until they heard my screams that they realized she had only been trying to protect me.",
    'effects' : {},
    'choices' : ('Bandit Child', 'Rescued Child'),
},
'Wolf Young Child' : {
    'age'     : 2,
    'text'    : "a pack of wolves, hungered by encroaching farmers, came upon my family during their travels. One of the wolves took me in as her own.",
    'effects' : {},
    'choices' : ('Wolf Child', 'Rescued Child'),
},
# FORK: What kind of odd behaviors? ('Odd Young Child')
'Magical Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'effects' : {},
},
'Bookish Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'effects' : {},
},

# Age 3: Child (7 to 12 years old)
'Mundane Child' : {
    'age'     : 3,
    'text'    : "I had an uneventful childhood.",
    'short'   : 'an uneventful childhood',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Teen',),
},
'Rich Child' : {
    'age'     : 3,
    'text'    : "Fortune smiled upon me as a young child.",
    'effects' : {},
    'years'   : 6,
},
'Poor Child' : {
    'age'     : 3,
    'text'    : "Fortune spat upon me as a young child.",
    'effects' : {},
    'years'   : 6,
},
'Rescued Child' : {
    'age'     : 3,
    'text'    : "I had an uneventful childhood.",
    'effects' : {},
    'years'   : 6,
},
'Odd Child' : {
    'age'     : 3,
    'text'    : "Even the few friends I had as a child considered me to be queer.",
    'effects' : {},
    'years'   : 6,
},
# FORK: Stolen infants
'Changeling Child' : {
    'age'     : 3,
    'text'    : "Separated from the civilization of my birth, my upbringing was unusual indeed.",
    'effects' : {},
    'years'   : 6,
    'choices' : ('Changeling Teen', 'Rescued Teen'),
},
'Cultist Child' : {
    'age'     : 3,
    'text'    : "Separated from the civilization of my birth, my upbringing was unusual indeed.",
    'effects' : {},
    'years'   : 6,
    'choices' : ('Cultist Teen', 'Rescued Teen'),
},
'Initiate Child' : {
    'age'     : 3,
    'text'    : "Separated from the civilization of my birth, my upbringing was unusual indeed.",
    'effects' : {},
    'years'   : 6,
    'choices' : ('Initiate Teen', 'Rescued Teen'),
},
# FORK: Orphaned infants
'Bandit Child' : {
    'age'     : 3,
    'text'    : "Separated from the civilization of my birth, my upbringing was unusual indeed.",
    'effects' : {},
    'years'   : 6,
    'choices' : ('Bandit Teen', 'Rescued Teen'),
},
'Pirate Child' : {
    'age'     : 3,
    'text'    : "Separated from the civilization of my birth, my upbringing was unusual indeed.",
    'effects' : {},
    'years'   : 6,
    'choices' : ('Pirate Teen', 'Rescued Teen'),
},
'Wolf Child' : {
    'age'     : 3,
    'text'    : "Separated from the civilization of my birth, my upbringing was unusual indeed.",
    'effects' : {},
    'years'   : 6,
    'choices' : ('Wolf Teen', 'Rescued Teen'),
},
# FORK: Who rescued you? ('Rescued Child')
# FORK: How were you odd? ('Odd Child')

# Age 4: Teen (13 to 18 years old)
'Mundane Teen' : {
    'age'     : 4,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'short'   : 'uninteresting teenage years',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Young Adult',),
},
'Dedicated Teen' : {
    'age'     : 4,
    'text'    : "I turned my efforts to labor from a young age, and I learned much from my experiences.",
    'effects' : {},
    'years'   : 6,
},
'Scoundrel Teen' : {
    'age'     : 4,
    'text'    : "I turned my efforts to sin from a young age, and I learned much from my experiences.",
    'effects' : {},
    'years'   : 6,
},
'Enlisted Teen' : {
    'age'     : 4,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'effects' : {},
    'years'   : 6,
},
'Odd Teen' : {
    'age'     : 4,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'effects' : {},
    'years'   : 6,
},
# FORK: Stolen teens
'Changeling Teen' : {
    'age'     : 4,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'effects' : {},
    'years'   : 6,
},
'Cultist Teen' : {
    'age'     : 4,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'effects' : {},
    'years'   : 6,
},
'Initiate Teen' : {
    'age'     : 4,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'effects' : {},
    'years'   : 6,
},
# FORK: Orphaned teens
'Bandit Teen' : {
    'age'     : 4,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'effects' : {},
    'years'   : 6,
},
'Pirate Teen' : {
    'age'     : 4,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'effects' : {},
    'years'   : 6,
},
'Wolf Teen' : {
    'age'     : 4,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'effects' : {},
    'years'   : 6,
},
# FORK: How were you odd? ('Odd Teen')

# Age 5: Young Adult (19 to 25 years old)
'Mundane Young Adult' : {
    'age'     : 5,
    'text'    : "My life was quiet as I grew into adulthood.",
    'short'   : 'a quiet first few years of adulthood',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Adult', 'Rich Adult', 'Poor Adult', 'Dedicated Adult', 'Scoundrel Adult', 'Enlisted Adult', 'Demonslayer'),
},
'Rich Young Adult' : {
    'age'     : 5,
    'text'    : "My life was quiet as I grew into adulthood.",
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Adult', 'Rich Adult', 'Poor Adult', 'Dedicated Adult', 'Scoundrel Adult', 'Enlisted Adult', 'Demonslayer'),
},
'Poor Young Adult' : {
    'age'     : 5,
    'text'    : "My life was quiet as I grew into adulthood.",
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Adult', 'Rich Adult', 'Poor Adult', 'Dedicated Adult', 'Scoundrel Adult', 'Enlisted Adult', 'Demonslayer'),
},
'Dedicated Young Adult' : {
    'age'     : 4,
    'text'    : "I turned my efforts to labor from a young age, and I learned much from my experiences.",
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Adult', 'Rich Adult', 'Poor Adult', 'Dedicated Adult', 'Scoundrel Adult', 'Enlisted Adult', 'Demonslayer'),
},
'Scoundrel Young Adult' : {
    'age'     : 4,
    'text'    : "I turned my efforts to sin from a young age, and I learned much from my experiences.",
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Adult', 'Rich Adult', 'Poor Adult', 'Dedicated Adult', 'Scoundrel Adult', 'Enlisted Adult', 'Demonslayer'),
},
'Enlisted Young Adult' : {
    'age'     : 5,
    'text'    : "My life was quiet as I grew into adulthood.",
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Adult', 'Rich Adult', 'Poor Adult', 'Dedicated Adult', 'Scoundrel Adult', 'Enlisted Adult', 'Demonslayer'),
},
# FORK: How were you trained? ('Immediate Adoption', rescued, or enlisted)
# FORK: How were you wild? ('Wild Young Adult')
# FORK: How were you odd? ('Odd Young Adult')

# Age 6: Adult (>25 years old)
'Mundane Adult' : {
    'age'     : 6,
    'text'    : "As an adult, little troubled me.",
    'effects' : {},
    'years'   : 6,
    'choices' : ('Demonslayer',),
},
'Rich Adult' : {
    'age'     : 6,
    'text'    : "As an adult, little troubled me.",
    'effects' : {},
    'years'   : 6,
    'choices' : ('Demonslayer',),
},
'Poor Adult' : {
    'age'     : 6,
    'text'    : "As an adult, little troubled me.",
    'effects' : {},
    'years'   : 6,
    'choices' : ('Demonslayer',),
},
'Dedicated Adult' : {
    'age'     : 6,
    'text'    : "I turned my efforts to labor from a young age, and I learned much from my experiences.",
    'effects' : {},
    'years'   : 6,
    'choices' : ('Demonslayer',),
},
'Scoundrel Adult' : {
    'age'     : 6,
    'text'    : "I turned my efforts to sin from a young age, and I learned much from my experiences.",
    'effects' : {},
    'years'   : 6,
    'choices' : ('Demonslayer',),
},
'Enlisted Adult' : {
    'age'     : 6,
    'text'    : "As an adult, little troubled me.",
    'effects' : {},
    'years'   : 6,
    'choices' : ('Demonslayer',),
},

# Everything above must lead to Demonslayer.

# FORK: How did you get into demon-slaying?
'Demonslayer' : {
    'age'     : 7,
    'text'    : "The time came for me to follow my true calling. I've travelled for years, now, slaying demons all the while. It seems that wherever I go, they are there... but at least wherever I leave, they aren't.",
    'short'   : 'travelled as a demonslayer',
    'effects' : {},
    'years'   : 2,
    'choices' : ('Reluctant Demonslayer', 'Vengeful Demonslayer', 'Zealous Demonslayer', 'Violent Demonslayer', 'Curious Demonslayer', 'Corrupt Demonslayer'),
},

# FORK: What was your reason for wanting to become a demonslayer?
'Reluctant Demonslayer' : {
    'text'    : "I did not want to, but against the forces of darkness, what choice did I have?",
    'short'   : 'became a demonslayer to protect others',
    'effects' : {},
    'choices' : ('End',),
},
'Vengeful Demonslayer' : {
    'text'    : "I have seen too much bloodshed. I need to destroy the fiends before they hurt anyone else.",
    'short'   : 'became a demonslayer to seek revenge',
    'effects' : {},
    'choices' : ('End',),
},
'Zealous Demonslayer' : {
    'text'    : "I don't regret leaving my life behind me. God himself called me to this task, and I will listen and obey.",
    'short'   : 'became a demonslayer to purify the world',
    'effects' : {},
    'choices' : ('End',),
},
'Violent Demonslayer' : {
    'text'    : "I plan to slay every one of those abominations. Even if they won't stay dead, I'll kill them until they get the picture.",
    'short'   : 'became a demonslayer to shed blood',
    'effects' : {},
    'choices' : ('End',),
},
'Curious Demonslayer' : {
    'text'    : "I didn't truly believe they existed - not at first - but now I have to learn more about them.",
    'short'   : 'became a demonslayer out of curiosity',
    'effects' : {},
    'choices' : ('End',),
},
'Corrupt Demonslayer' : {
    'text'    : "The forces of darkness have vast... vast power. Power you wouldn't believe. It has to be studied.",
    'short'   : 'became a demonslayer for dark reasons',
    'effects' : {},
    'choices' : ('End',),
},

# End character generation.
'End' : {
    'text'    : "I can't attest to whether you've found my story interesting, but at least I can swear that every word I've told you is the truth.",
    'effects' : {},
    'choices' : None,
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
