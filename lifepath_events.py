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
    'effects' : {'Intelligence': 10},
    'years'   : 0,
    'choices' : ('Mundane Parents', 'Warrior Parents', 'Wizard Parents', 'Mysterious Parents'),
},
# Age 0: Parents (~-9 months old)
'Mundane Parents' : {
    'age'     : 0,
    'text'    : "My parents were regular people like yourself.",
    'short'   : "had a normal family",
    'effects' : {'Intelligence': 3},
    'choices' : ('Mundane Infant', 'Dark Omen', 'Strange Omen', 'Holy Day', 'Bloody Birth', 'Immediate Adoption'),
},
'Warrior Parents' : {
    'age'     : 0,
    'text'    : "My parents were skilled warriors.",
    'short'   : "were heir to martial prowess",
    'effects' : {'HP' : 1},
    'choices' : ('Mundane Infant', 'Dark Omen', 'Strange Omen', 'Holy Day', 'Bloody Birth', 'Immediate Adoption'),
},
'Wizard Parents' : {
    'age'     : 0,
    'text'    : "Both of my parents were powerful mages.",
    'short'   : "were heir to magical power",
    'effects' : {'MP' : 1},
    'choices' : ('Mundane Infant', 'Dark Omen', 'Strange Omen', 'Holy Day', 'Bloody Birth', 'Immediate Adoption'),
},
'Mysterious Parents' : {
    'age'     : 0,
    'text'    : "My parents never spoke of how it came to pass, but I was certainly no child of my father.",
    'short'   : "had uncertain heritage",
    'effects' : {},
    'choices' : ('Mundane Infant', 'Dark Omen', 'Strange Omen', 'Holy Day', 'Bloody Birth', 'Immediate Adoption'),
},
# Age 1: Infant (0 to 1 years old)
'Mundane Infant' : {
    'age'     : 1,
    'text'    : "My birth was exciting for my parents, but few others.",
    'short'   : "had a normal birth",
    'effects' : {'Intelligence' : -1},
    'years'   : 1,
    'choices' : ('Mundane Young Child', 'Rich Young Child', 'Poor Young Child', 'Stolen Young Child', 'Orphaned Young Child', 'Odd Young Child'),
},
'Dark Omen' : {
    'age'     : 1,
    'text'    : "Dark omens troubled the day of my birth.",
    'short'   : 'were born under dark omens',
    'effects' : {},
    'years'   : 1,
    'choices' : ('Mundane Young Child', 'Rich Young Child', 'Poor Young Child', 'Stolen Young Child', 'Orphaned Young Child', 'Odd Young Child'),
},
'Strange Omen' : {
    'age'     : 1,
    'text'    : "Eerie signs were seen on the day of my birth.",
    'short'   : 'were born under strange omens',
    'effects' : {},
    'years'   : 1,
    'choices' : ('Mundane Young Child', 'Rich Young Child', 'Poor Young Child', 'Stolen Young Child', 'Orphaned Young Child', 'Odd Young Child'),
},
'Holy Day' : {
    'age'     : 1,
    'text'    : "I was born on a holy day.",
    'short'   : 'were born on a holy day',
    'effects' : {},
    'years'   : 1,
    'choices' : ('Mundane Young Child', 'Rich Young Child', 'Poor Young Child', 'Stolen Young Child', 'Orphaned Young Child', 'Odd Young Child'),
},
'Bloody Birth' : {
    'age'     : 1,
    'text'    : "I was born on the battlefield.",
    'short'   : 'were born on the chaos of the battlefield',
    'effects' : {'Combat Reflexes' : True},
    'years'   : 1,
    'choices' : ('Mundane Young Child', 'Rich Young Child', 'Poor Young Child', 'Stolen Young Child', 'Orphaned Young Child', 'Odd Young Child'),
},
'Immediate Adoption' : {
    'age'     : 1,
    'text'    : "I was given up right after birth - unwanted by my own mother.",
    'short'   : 'were given up for adoption after birth',
    'effects' : {},
    'years'   : 1,
    'choices' : ('Mundane Young Child', 'Rich Young Child', 'Poor Young Child', 'Stolen Young Child', 'Orphaned Young Child', 'Odd Young Child'),
},
# Age 2: Young Child (1 to 6 years old)
'Mundane Young Child' : {
    'age'     : 2,
    'text'    : "My early years were uneventful.",
    'short'   : 'had an uneventful young childhood',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Child', 'Rich Child', 'Poor Child'),
},
'Rich Young Child' : {
    'age'     : 2,
    'text'    : "I spent my early years swaddled in cloth-of-gold.",
    'short'   : 'spent your early years in a wealthy family',
    'effects' : {},
    'years'   : 6,
},
'Poor Young Child' : {
    'age'     : 2,
    'text'    : "Even as an infant, I was deprived of life's necessities. Luxuries were unheard of.",
    'short'   : 'spent your early years in a poor family',
    'effects' : {},
    'years'   : 6,
},
# TODO: Years are only for the actual choices
'Stolen Young Child' : {
    'age'     : 2,
    'text'    : "I was stolen away from my parents.",
    'short'   : 'were stolen away from your parents soon after birth',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Changeling Young Child', 'Cultist Young Child', 'Initiate Young Child'),
},
'Orphaned Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth, my parents were brutally killed.",
    'short'   : 'were orphaned soon after birth',
    'effects' : {},
    'years'   : 6,
},
'Odd Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'short'   : 'exhibited odd behaviors from a very young age',
    'effects' : {},
    'years'   : 6,
},
# FORK: Who raised you? ('Immediate Adoption')
'Church Young Child' : {
    'age'     : 2,
    'text'    : "My early years were uneventful.",
    'short'   : 'spent your early years in the church',
    'effects' : {},
    'years'   : 1,
},
# FORK: Who raised you? 
'Church Young Child' : {
    'age'     : 2,
    'text'    : "It was merely an accident of fate - unexpected, but not unusual.",
    'short'   : 'spent your early years in the church',
    'effects' : {},
    'years'   : 6,
},
# FORK: What were you stolen by? ('Stolen Young Child')
'Changeling Young Child' : {
    'age'     : 2,
    'text'    : "Faeries came from the deep wood and swapped one of their children for me.",
    'short'   : 'were abducted by faeries',
    'effects' : {},
    'choices' : ('Changeling Child', 'Rescued Child'),
},
'Cultist Young Child' : {
    'age'     : 2,
    'text'    : "Demon-worshipers saw something in me and took me as theirs. Perhaps I was intended to be a sacrifice, but was granted compassion for some reason.",
    'short'   : 'were abducted by a dark cult',
    'effects' : {},
    'choices' : ('Cultist Child', 'Rescued Child'),
},
'Initiate Young Child' : {
    'age'     : 2,
    'text'    : "My abductors were a fanatical religious order dedicated to slaying demons.",
    'short'   : 'were abducted by a secret order',
    'effects' : {},
    'choices' : ('Initiate Child', 'Rescued Child'),
},
# FORK: What killed your parents? ('Orphaned Young Child')
'Pirate Young Child' : {
    'age'     : 2,
    'text'    : "My parents were attacked by black-hearted pirates. They slaughtered everyone, but even they couldn't bear to harm a helpless child.",
    'short'   : 'were the sole survivor of a pirate attack',
    'effects' : {},
    'choices' : ('Pirate Child', 'Rescued Child'),
},
'Bandit Young Child' : {
    'age'     : 2,
    'text'    : "My parents were attacked by bandits. My mother attempted to flee and they shot her where she stood. It wasn't until they heard my screams that they realized she had only been trying to protect me.",
    'short'   : 'were the sole survivor of a bandit attack',
    'effects' : {},
    'choices' : ('Bandit Child', 'Rescued Child'),
},
'Wolf Young Child' : {
    'age'     : 2,
    'text'    : "a pack of wolves, hungered by encroaching farmers, came upon my family during their travels. One of the wolves took me in as her own.",
    'short'   : 'were the sole survivor of a wolf attack',
    'effects' : {},
    'choices' : ('Wolf Child', 'Rescued Child'),
},
# FORK: What kind of odd behaviors? ('Odd Young Child')
'Magical Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'short'   : 'had innate magical talent',
    'effects' : {},
},
'Bookish Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'short'   : 'had an unnatural aptitude for reading',
    'effects' : {},
},

# Age 3: Child (7 to 12 years old)
'Mundane Child' : {
    'age'     : 3,
    'text'    : "I had an uneventful childhood.",
    'short'   : 'grew up in a normal household',
    'effects' : {'Skill/Farming' : 1},
    'years'   : 6,
    'choices' : ('Mundane Teen',),
},
'Rich Child' : {
    'age'     : 3,
    'text'    : "Fortune smiled upon me as a young child.",
    'short'   : 'grew up in a wealthy household',
    'effects' : {},
    'years'   : 6,
},
'Poor Child' : {
    'age'     : 3,
    'text'    : "Fortune spat upon me as a young child.",
    'short'   : 'grew up in an impoverished household',
    'effects' : {},
    'years'   : 6,
},
'Rescued Child' : {
    'age'     : 3,
    'text'    : "I had an uneventful childhood.",
    'short'   : 'were rescued from your plight',
    'effects' : {},
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
    'short'   : 'grew to see the fey as your family',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Changeling Teen', 'Rescued Teen'),
},
'Cultist Child' : {
    'age'     : 3,
    'text'    : "Separated from the civilization of my birth, my upbringing was unusual indeed.",
    'short'   : 'grew to see the cultists as your family',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Cultist Teen', 'Rescued Teen'),
},
'Initiate Child' : {
    'age'     : 3,
    'text'    : "Separated from the civilization of my birth, my upbringing was unusual indeed.",
    'short'   : 'grew to see the order as your family',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Initiate Teen', 'Rescued Teen'),
},
# FORK: Orphaned infants
'Bandit Child' : {
    'age'     : 3,
    'text'    : "Separated from the civilization of my birth, my upbringing was unusual indeed.",
    'short'   : 'grew to see the bandits as your family',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Bandit Teen', 'Rescued Teen'),
},
'Pirate Child' : {
    'age'     : 3,
    'text'    : "Separated from the civilization of my birth, my upbringing was unusual indeed.",
    'short'   : 'grew to see the pirates as your family',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Pirate Teen', 'Rescued Teen'),
},
'Wolf Child' : {
    'age'     : 3,
    'text'    : "Separated from the civilization of my birth, my upbringing was unusual indeed.",
    'short'   : 'grew to see the wolves as your family',
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
    'short'   : 'faced the usual struggles of teenagers',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Young Adult', 'Rich Young Adult', 'Poor Young Adult', 'Dedicated Young Adult', 'Scoundrel Young Adult', 'Enlisted Young Adult'),
},
'Dedicated Teen' : {
    'age'     : 4,
    'text'    : "I turned my efforts to labor from a young age, and I learned much from my experiences.",
    'short'   : 'served dutifully through your teenage years',
    'effects' : {},
    'years'   : 6,
},
'Scoundrel Teen' : {
    'age'     : 4,
    'text'    : "I turned my efforts to sin from a young age, and I learned much from my experiences.",
    'short'   : 'abdicated responsibility through your teenage years',
    'effects' : {},
    'years'   : 6,
},
'Enlisted Teen' : {
    'age'     : 4,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'short'   : 'served as a common soldier',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Young Adult', 'Rich Young Adult', 'Poor Young Adult', 'Dedicated Young Adult', 'Scoundrel Young Adult', 'Enlisted Young Adult', 'Officer Young Adult'),
},
'Odd Teen' : {
    'age'     : 4,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'short'   : 'were an outcast even among the outcasts',
    'effects' : {},
    'years'   : 6,
},
# FORK: Stolen teens
'Changeling Teen' : {
    'age'     : 4,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'short'   : 'embraced the teachings of the fairies',
    'effects' : {},
    'years'   : 6,
},
'Cultist Teen' : {
    'age'     : 4,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'short'   : 'embraced the teachings of the cultists',
    'effects' : {},
    'years'   : 6,
},
'Initiate Teen' : {
    'age'     : 4,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'short'   : 'embraced the teachings of the order',
    'effects' : {},
    'years'   : 6,
},
# FORK: Orphaned teens
'Bandit Teen' : {
    'age'     : 4,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'short'   : 'chose to join the bandits',
    'effects' : {},
    'years'   : 6,
},
'Pirate Teen' : {
    'age'     : 4,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'short'   : 'chose to join the pirates',
    'effects' : {},
    'years'   : 6,
},
'Wolf Teen' : {
    'age'     : 4,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'short'   : 'chose to stay among the pack',
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
    'text'    : "As a young man, wealth freed me to do whatever my heart demanded. Many a time I cursed the fates that I had so little time with which to pursue my dreams.",
    'short'   : 'spent years in luxury',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Adult', 'Rich Adult', 'Poor Adult', 'Dedicated Adult', 'Scoundrel Adult', 'Enlisted Adult', 'Demonslayer'),
},
'Poor Young Adult' : {
    'age'     : 5,
    'text'    : "As a young man, poverty shackled me to a miserable existence of menial labor. Many a time I cursed the fates for my lot.",
    'short'   : 'spent years in poverty',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Adult', 'Rich Adult', 'Poor Adult', 'Dedicated Adult', 'Scoundrel Adult', 'Enlisted Adult', 'Demonslayer'),
},
'Dedicated Young Adult' : {
    'age'     : 4,
    'text'    : "As I grew into adulthood, I indulged in little more than hard work and steady habits.",
    'short'   : 'dedicated yourself to gainful work',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Adult', 'Rich Adult', 'Poor Adult', 'Dedicated Adult', 'Scoundrel Adult', 'Enlisted Adult', 'Demonslayer'),
},
'Scoundrel Young Adult' : {
    'age'     : 4,
    'text'    : "As I grew into adulthood, I indulged in nothing less than decadent debauchery and cunning crimes.",
    'short'   : 'indulged in questionable pursuits',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Adult', 'Rich Adult', 'Poor Adult', 'Dedicated Adult', 'Scoundrel Adult', 'Enlisted Adult', 'Demonslayer'),
},
'Enlisted Young Adult' : {
    'age'     : 5,
    'text'    : "My life was quiet as I grew into adulthood.",
    'short'   : 'served as a common soldier',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Adult', 'Rich Adult', 'Poor Adult', 'Dedicated Adult', 'Scoundrel Adult', 'Enlisted Adult', 'Officer Adult', 'Demonslayer'),
},
'Officer Young Adult' : {
    'age'     : 5,
    'text'    : "My life was quiet as I grew into adulthood.",
    'short'   : 'served as an officer',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Adult', 'Rich Adult', 'Poor Adult', 'Dedicated Adult', 'Scoundrel Adult', 'Officer Adult', 'Heroic Adult', 'Demonslayer'),
},
# FORK: How were you trained? ('Immediate Adoption', rescued, or enlisted)
# FORK: How were you wild? ('Wild Young Adult')
# FORK: How were you odd? ('Odd Young Adult')

# Age 6: Adult (>25 years old)
'Mundane Adult' : {
    'age'     : 6,
    'text'    : "As an adult, little troubled me.",
    'short'   : 'lived as a normal person',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Demonslayer',),
},
'Rich Adult' : {
    'age'     : 6,
    'text'    : "As an adult, little troubled me.",
    'short'   : 'enjoyed a luxurious life',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Demonslayer',),
},
'Poor Adult' : {
    'age'     : 6,
    'text'    : "As an adult, little troubled me.",
    'short'   : 'labored through a miserable life',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Demonslayer',),
},
'Dedicated Adult' : {
    'age'     : 6,
    'text'    : "I turned my efforts to labor from a young age, and I learned much from my experiences.",
    'short'   : 'dedicated yourself to respectable endeavors',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Demonslayer',),
},
'Scoundrel Adult' : {
    'age'     : 6,
    'text'    : "I turned my efforts to sin from a young age, and I learned much from my experiences.",
    'short'   : 'dedicated yourself to reprehensible endeavors',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Demonslayer',),
},
'Enlisted Adult' : {
    'age'     : 6,
    'text'    : "served as a common soldier.",
    'short'   : 'served as a common soldier',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Demonslayer',),
},
'Officer Adult' : {
    'age'     : 6,
    'text'    : "served as an officer.",
    'short'   : 'served as an officer',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Demonslayer',),
},
'Heroic Adult' : {
    'age'     : 6,
    'text'    : "In recognition of my prowess, I was given ever greater roles on the battlefield.",
    'short'   : 'served as a mighty leader of men',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Demonslayer',),
},

# Everything above must lead to Demonslayer.

# FORK: How did you get into demon-slaying?
'Demonslayer' : {
    'age'     : 7,
    'text'    : "It was only within the past few years that I began to actively hunt demons. I've travelled across Europe, slaying demons all the while. It seems that wherever I go, they are there... but at least wherever I leave, they aren't. For a while.",
    'short'   : 'travelled as a demonslayer',
    'effects' : {},
    'years'   : 2,
    'choices' : ('Reluctant Demonslayer', 'Vengeful Demonslayer', 'Zealous Demonslayer', 'Violent Demonslayer', 'Curious Demonslayer', 'Corrupt Demonslayer'),
},

# FORK: What was your reason for wanting to become a demonslayer?
'Reluctant Demonslayer' : {
    'text'    : "I did not want to, but against the forces of darkness, what choice did I have but to stand? If I hadn't chosen to protect others, there's no guessing whether anyone else would have. It's a lonely calling, but a necessary one, and for now the burden of demonslaying has fallen on my shoulders.",
    'short'   : 'became a demonslayer to protect others',
    'effects' : {},
    'choices' : ('End',),
},
'Vengeful Demonslayer' : {
    'text'    : "I have seen too much bloodshed. Families torn apart. Churches razed. Entire towns swallowed whole by the maw of Chaos. I need to destroy as many of these fiends as I can, as soon as I can... before they hurt anyone else.",
    'short'   : 'became a demonslayer to seek revenge',
    'effects' : {},
    'choices' : ('End',),
},
'Zealous Demonslayer' : {
    'text'    : "God himself called me to this task, and I will listen and obey. The life I left behind was just an instrument He crafted to prepare me for my true purpose, and I have left it behind me with no regrets.",
    'short'   : 'became a demonslayer to serve God',
    'effects' : {},
    'choices' : ('End',),
},
'Violent Demonslayer' : {
    'text'    : "I'll slay these abominations until I drown in their blood. Even if they won't stay dead, I'll rip them apart until they get the picture!",
    'short'   : 'became a demonslayer out of lust for violence',
    'effects' : {},
    'choices' : ('End',),
},
'Curious Demonslayer' : {
    'text'    : "I had never truly believed in demons until I saw them with my own eyes. Now that I know, I have no choice but to learn more about them.",
    'short'   : 'became a demonslayer out of curiosity',
    'effects' : {},
    'choices' : ('End',),
},
'Corrupt Demonslayer' : {
    'text'    : "The forces of darkness have vast power. Power you wouldn't believe. It has to be... studied.",
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

def dot(tree, eventname):
    event = tree.get(eventname, None)
    if event is not None:
        if event.get("choices", None) != None:
            for choice in event["choices"]:
                if choice != '':
                    print "%s -> %s" % (eventname.replace(' ', ''), choice.replace(' ', ''))
                    dot(tree, choice)

if __name__ == "__main__":

# Print all event names
#    for k, v in eventdata.iteritems():
#        print k

# Print a tree
#    recurse(eventdata, "Start", 0)

# Print DOT language text
    print "digraph Hellmouth {"
    dot(eventdata, "Start")
    print "}"
