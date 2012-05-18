# TODO: Move test code to lifepath.py

# String to show for skipping to a point and what point to skip to.
# Mainly serves to prevent me from having to create dummy entries in the data.

skip = (('PARENTS', 'I can only believe that God chose me even before my birth.', []),
        ('BIRTH', 'It was from the moment of my birth that God saw fit to change my life.', ['Mundane Parents']),
        ('EARLY CHILDHOOD', 'I didn\'t feel the Hand of God upon my fate until I was a young child.', ['Mundane Parents', 'Mundane Infant']),
        ('CHILDHOOD', 'Not until I was a child.', ['Mundane Parents', 'Mundane Infant', 'Mundane Young Child']),
        ('TEENAGER', 'Not until I was a teenager.', ['Mundane Parents', 'Mundane Infant', 'Mundane Young Child', 'Mundane Child']),
        ('YOUNG ADULT', 'Not until I was a young adult.', ['Mundane Parents', 'Mundane Infant', 'Mundane Young Child', 'Mundane Child', 'Mundane Teen']),
        ('ADULT', 'Not until I was an adult.', ['Mundane Parents', 'Mundane Infant', 'Mundane Young Child', 'Mundane Child', 'Mundane Teen', 'Mundane Young Adult']),
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
    'effects' : {'Strength': 10, 'Dexterity': 10, 'Intelligence': 10, 'Health': 10},
    'years'   : 0,
    'choices' : ('Mundane Parents', 'Warrior Parents', 'Wizard Parents'),
},
# Age 0: Parents (~-9 months old)
'Mundane Parents' : {
    'age'     : 0,
    'text'    : "My parents were regular people like yourself.",
    'short'   : "had a normal family",
    'effects' : {},
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
# Age 1: Infant (0 to 1 years old)
'Mundane Infant' : {
    'age'     : 1,
    'text'    : "My birth was exciting for my parents, but few others.",
    'short'   : "were brought into this world without incident",
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
'Unknown Parents' : {
    'age'     : 0,
    'text'    : "My parents never spoke of how it came to pass, but I was certainly no child of my father. Perhaps not even of my mother.",
    'short'   : "were of uncertain heritage",
    'effects' : {},
    'years'   : 1,
    'choices' : ('Mundane Young Child', 'Rich Young Child', 'Poor Young Child', 'Stolen Young Child', 'Orphaned Young Child', 'Odd Young Child'),
},
'Immediate Adoption' : {
    'age'     : 1,
    'text'    : "I was given up right after birth - unwanted by my own mother.",
    'short'   : 'were given up for adoption after birth',
    'effects' : {},
    'years'   : 1,
    'choices' : ('Mundane Young Child', 'Rich Young Child', 'Poor Young Child', 'Stolen Young Child', 'Orphaned Young Child', 'Odd Young Child', 'Church Young Child'),
},
# Age 2: Young Child (1 to 6 years old)
# Core choices
'Mundane Young Child' : {
    'age'     : 2,
    'text'    : "My early years were uneventful.",
    'short'   : 'spent your early years in an average family',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Child', 'Rich Child', 'Poor Child', 'Odd Child'),
},
'Rich Young Child' : {
    'age'     : 2,
    'text'    : "I spent my early years swaddled in cloth-of-gold.",
    'short'   : 'spent your early years in a wealthy family',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Child', 'Rich Child', 'Poor Child', 'Odd Child'),
},
'Poor Young Child' : {
    'age'     : 2,
    'text'    : "Even as an infant, I was deprived of life's necessities. Luxuries were unheard of.",
    'short'   : 'spent your early years in a poor family',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Child', 'Rich Child', 'Poor Child', 'Odd Child'),
},
# Branching choices
'Stolen Young Child' : {
    'age'     : 2,
    'text'    : "I was stolen away from my parents.",
    'short'   : 'were stolen away soon after birth',
    'effects' : {},
    'choices' : ('Changeling Young Child', 'Cultist Young Child', 'Initiate Young Child'),
},
'Orphaned Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth, my parents were brutally killed.",
    'short'   : 'were orphaned soon after birth',
    'effects' : {},
    'choices' : ('Pirate Young Child', 'Bandit Young Child', 'Wolf Young Child'),
},
'Odd Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'short'   : 'exhibited odd behaviors soon after birth',
    'effects' : {},
    'choices' : ('Magical Young Child', 'Bookish Young Child'),
},
# Raised by someone else
'Church Young Child' : {
    'age'     : 2,
    'text'    : "My early years were uneventful.",
    'short'   : 'spent your early years in the church',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Church Child',),
},
# Stolen by something
'Changeling Young Child' : {
    'age'     : 2,
    'text'    : "Faeries came from the deep wood and swapped one of their own children for me.",
    'short'   : 'were abducted by faeries',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Changeling Child', 'Rescued Child'),
},
'Cultist Young Child' : {
    'age'     : 2,
    'text'    : "Demon-worshipers saw something in me and took me as theirs. Perhaps I was intended to be a sacrifice, but was granted compassion for some reason.",
    'short'   : 'were abducted by a dark cult',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Cultist Child', 'Rescued Child'),
},
'Initiate Young Child' : {
    'age'     : 2,
    'text'    : "My abductors were a fanatical religious order dedicated to slaying demons.",
    'short'   : 'were abducted by a secret order',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Initiate Child', 'Rescued Child'),
},
# Orphaned by something
'Pirate Young Child' : {
    'age'     : 2,
    'text'    : "My parents were attacked by black-hearted pirates. They slaughtered everyone, but even they couldn't bear to harm a helpless child.",
    'short'   : 'were the sole survivor of a pirate attack',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Pirate Child', 'Rescued Child'),
},
'Bandit Young Child' : {
    'age'     : 2,
    'text'    : "My parents were attacked by bandits. My mother attempted to flee and they shot her where she stood. It wasn't until they heard my screams that they realized she had only been trying to protect me.",
    'short'   : 'were the sole survivor of a bandit attack',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Bandit Child', 'Rescued Child'),
},
'Wolf Young Child' : {
    'age'     : 2,
    'text'    : "a pack of wolves, hungered by encroaching farmers, came upon my family during their travels. One of the wolves took me in as her own.",
    'short'   : 'were the sole survivor of a wolf attack',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Wolf Child', 'Rescued Child'),
},
# Innate talents
'Magical Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'short'   : 'had innate magical talent',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Child', 'Rich Child', 'Poor Child', 'Magical Child'),
},
'Bookish Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'short'   : 'had an unnatural aptitude for reading',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Child', 'Rich Child', 'Poor Child', 'Bookish Child'),
},
# Age 3: Child (7 to 12 years old)
# Core choices
'Mundane Child' : {
    'age'     : 3,
    'text'    : "I had an uneventful childhood.",
    'short'   : 'grew to adolescence in a normal household',
    'effects' : {'Skill/Farming' : 1},
    'years'   : 6,
    'choices' : ('Mundane Teen', 'Rich Teen', 'Poor Teen', 'Dedicated Teen', 'Scoundrel Teen', 'Odd Teen', 'Enlisted Teen'),
},
'Rich Child' : {
    'age'     : 3,
    'text'    : "Fortune smiled upon me as a young child.",
    'short'   : 'grew to adolescence in a wealthy household',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Teen', 'Rich Teen', 'Poor Teen', 'Dedicated Teen', 'Scoundrel Teen', 'Odd Teen', 'Enlisted Teen'),
},
'Poor Child' : {
    'age'     : 3,
    'text'    : "Fortune spat upon me as a young child.",
    'short'   : 'grew to adolescence in an impoverished household',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Teen', 'Rich Teen', 'Poor Teen', 'Dedicated Teen', 'Scoundrel Teen', 'Odd Teen', 'Enlisted Teen'),
},
# Branching choices
'Odd Child' : {
    'age'     : 3,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'short'   : 'exhibited odd behaviors as a child',
    'effects' : {},
    'choices' : ('Magical Child', 'Bookish Child'),
},
'Rescued Child' : {
    'age'     : 3,
    'text'    : "I had an uneventful childhood.",
    'short'   : 'were rescued from your plight',
    'effects' : {},
    'choices' : ('Adventurer Child', 'Church Child', 'Returned Child'),
},
# Raised by someone else
'Adventurer Child' : {
    'age'     : 3,
    'text'    : "Separated from the civilization of my birth, my upbringing was unusual indeed.",
    'short'   : 'made the hard adjustment back to a normal life',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Teen', 'Rich Teen', 'Poor Teen', 'Dedicated Teen', 'Scoundrel Teen', 'Odd Teen', 'Enlisted Teen', 'Adventurer Teen'),
},
'Church Child' : {
    'age'     : 3,
    'text'    : "Separated from the civilization of my birth, my upbringing was unusual indeed.",
    'short'   : 'made the hard adjustment back to a normal life',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Teen', 'Rich Teen', 'Poor Teen', 'Dedicated Teen', 'Scoundrel Teen', 'Odd Teen', 'Enlisted Teen', 'Church Teen'),
},
'Returned Child' : {
    'age'     : 3,
    'text'    : "Separated from the civilization of my birth, my upbringing was unusual indeed.",
    'short'   : 'made the hard adjustment back to a normal life',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Teen', 'Rich Teen', 'Poor Teen', 'Dedicated Teen', 'Scoundrel Teen', 'Odd Teen', 'Enlisted Teen'),
},
# Stolen by something
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
# Orphaned by something
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
# Innate talents
'Magical Child' : {
    'age'     : 3,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'short'   : 'had innate magical talent',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Teen', 'Rich Teen', 'Poor Teen', 'Magical Teen'),
},
'Wizard Child' : {
    'age'     : 3,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'short'   : 'continued to hone your powers',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Teen', 'Rich Teen', 'Poor Teen', 'Wizard Teen'),
},
'Bookish Child' : {
    'age'     : 3,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'short'   : 'had an unnatural aptitude for reading',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Teen', 'Rich Teen', 'Poor Teen', 'Scholar Teen'),
},
# Age 4: Teen (13 to 18 years old)
# Core choices
'Mundane Teen' : {
    'age'     : 4,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'short'   : 'faced the usual struggles of teenagers',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Young Adult', 'Rich Young Adult', 'Poor Young Adult', 'Dedicated Young Adult', 'Scoundrel Young Adult', 'Enlisted Young Adult'),
},
'Rich Teen' : {
    'age'     : 4,
    'text'    : "I understood that I had been blessed, and I was full of vigor as I confronted the world.",
    'short'   : 'spent years in luxury',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Young Adult', 'Rich Young Adult', 'Poor Young Adult', 'Dedicated Young Adult', 'Scoundrel Young Adult', 'Enlisted Young Adult'),
},
'Poor Teen' : {
    'age'     : 4,
    'text'    : "I didn't understand why this was happening to me, but I was full of rage as I confronted the world.",
    'short'   : 'spent years in poverty',
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
    'choices' : ('Mundane Young Adult', 'Rich Young Adult', 'Poor Young Adult', 'Dedicated Young Adult', 'Scoundrel Young Adult', 'Enlisted Young Adult'),
},
'Scoundrel Teen' : {
    'age'     : 4,
    'text'    : "I turned my efforts to sin from a young age, and I learned much from my experiences.",
    'short'   : 'abdicated responsibility through your teenage years',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Young Adult', 'Rich Young Adult', 'Poor Young Adult', 'Dedicated Young Adult', 'Scoundrel Young Adult', 'Enlisted Young Adult', 'Arrested Young Adult'),
},
# Branching choices
'Odd Teen' : {
    'age'     : 4,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'short'   : 'were an outcast even among the outcasts',
    'effects' : {},
    'choices' : ('Magical Teen', 'Bookish Teen'),
},
'Rescued Teen' : {
    'age'     : 4,
    'text'    : "I had an uneventful childhood.",
    'short'   : 'were rescued from your plight',
    'effects' : {},
    'choices' : ('Adventurer Teen', 'Church Teen', 'Returned Teen'),
},
# Raised by someone else
'Adventurer Teen' : {
    'age'     : 4,
    'text'    : "Separated from the civilization of my birth, my upbringing was unusual indeed.",
    'short'   : 'made the hard adjustment back to a normal life',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Young Adult', 'Rich Young Adult', 'Poor Young Adult', 'Dedicated Young Adult', 'Scoundrel Young Adult', 'Enlisted Young Adult', 'Adventurer Young Adult'),
},
'Church Teen' : {
    'age'     : 4,
    'text'    : "Separated from the civilization of my birth, my upbringing was unusual indeed.",
    'short'   : 'made the hard adjustment back to a normal life',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Young Adult', 'Rich Young Adult', 'Poor Young Adult', 'Dedicated Young Adult', 'Scoundrel Young Adult', 'Enlisted Young Adult', 'Church Young Adult'),
},
'Returned Teen' : {
    'age'     : 4,
    'text'    : "Separated from the civilization of my birth, my upbringing was unusual indeed.",
    'short'   : 'made the hard adjustment back to a normal life',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Young Adult', 'Rich Young Adult', 'Poor Young Adult', 'Dedicated Young Adult', 'Scoundrel Young Adult', 'Arrested Young Adult', 'Enlisted Young Adult'),
},
# Stolen by something
'Changeling Teen' : {
    'age'     : 4,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'short'   : 'embraced the teachings of the fairies',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Changeling Young Adult', 'Returned Young Adult'),
},
'Cultist Teen' : {
    'age'     : 4,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'short'   : 'embraced the teachings of the cultists',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Cultist Young Adult', 'Returned Young Adult'),
},
'Initiate Teen' : {
    'age'     : 4,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'short'   : 'embraced the teachings of the order',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Initiate Young Adult', 'Returned Young Adult'),
},
# Orphaned by something
'Bandit Teen' : {
    'age'     : 4,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'short'   : 'chose to join the bandits',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Bandit Young Adult', 'Returned Young Adult', 'Arrested Young Adult'),
},
'Pirate Teen' : {
    'age'     : 4,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'short'   : 'chose to join the pirates',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Pirate Young Adult', 'Returned Young Adult', 'Arrested Young Adult'),
},
'Wolf Teen' : {
    'age'     : 4,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'short'   : 'chose to stay among the pack',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Wolf Young Adult', 'Returned Young Adult'),
},
# Innate talents
'Magical Teen' : {
    'age'     : 4,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'short'   : 'manifested your magical power at puberty',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Young Adult', 'Rich Young Adult', 'Poor Young Adult', 'Dedicated Young Adult', 'Scoundrel Young Adult', 'Enlisted Young Adult', 'Wizard Young Adult'),
},
'Wizard Teen' : {
    'age'     : 4,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'short'   : 'were invited to attend a magic school',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Young Adult', 'Rich Young Adult', 'Poor Young Adult', 'Dedicated Young Adult', 'Scoundrel Young Adult', 'Enlisted Young Adult', 'Wizard Young Adult'),
},
'Bookish Teen' : {
    'age'     : 4,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'short'   : 'were at home with books',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Young Adult', 'Rich Young Adult', 'Poor Young Adult', 'Dedicated Young Adult', 'Scoundrel Young Adult', 'Enlisted Young Adult', 'Scholar Young Adult'),
},
'Scholar Teen' : {
    'age'     : 4,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'short'   : 'had an unnatural aptitude for reading',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Young Adult', 'Rich Young Adult', 'Poor Young Adult', 'Dedicated Young Adult', 'Scoundrel Young Adult', 'Enlisted Young Adult', 'Scholar Young Adult'),
},
# Military career
'Enlisted Teen' : {
    'age'     : 4,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'short'   : 'served as a common soldier',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Young Adult', 'Rich Young Adult', 'Poor Young Adult', 'Dedicated Young Adult', 'Scoundrel Young Adult', 'Enlisted Young Adult', 'Officer Young Adult'),
},
# Age 5: Young Adult (19 to 25 years old)
# Core choices
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
    'age'     : 5,
    'text'    : "As I grew into adulthood, I indulged in little more than hard work and steady habits.",
    'short'   : 'dedicated yourself to gainful work',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Adult', 'Rich Adult', 'Poor Adult', 'Dedicated Adult', 'Scoundrel Adult', 'Enlisted Adult', 'Demonslayer'),
},
'Scoundrel Young Adult' : {
    'age'     : 5,
    'text'    : "As I grew into adulthood, I indulged in nothing less than decadent debauchery and cunning crimes.",
    'short'   : 'indulged in questionable pursuits',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Adult', 'Rich Adult', 'Poor Adult', 'Dedicated Adult', 'Scoundrel Adult', 'Enlisted Adult', 'Demonslayer'),
},
# Raised by someone else
'Adventurer Young Adult' : {
    'age'     : 5,
    'text'    : "Separated from the civilization of my birth, my upbringing was unusual indeed.",
    'short'   : 'made the hard adjustment back to a normal life',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Adult', 'Rich Adult', 'Poor Adult', 'Dedicated Adult', 'Scoundrel Adult', 'Enlisted Adult', 'Adventurer Adult', 'Demonslayer'),
},
'Church Young Adult' : {
    'age'     : 5,
    'text'    : "Separated from the civilization of my birth, my upbringing was unusual indeed.",
    'short'   : 'made the hard adjustment back to a normal life',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Adult', 'Rich Adult', 'Poor Adult', 'Dedicated Adult', 'Scoundrel Adult', 'Enlisted Adult', 'Church Adult', 'Demonslayer'),
},
'Returned Young Adult' : {
    'age'     : 5,
    'text'    : "Separated from the civilization of my birth, my upbringing was unusual indeed.",
    'short'   : 'made the hard adjustment back to a normal life',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Adult', 'Rich Adult', 'Poor Adult', 'Dedicated Adult', 'Scoundrel Adult', 'Enlisted Adult', 'Arrested Adult', 'Demonslayer'),
},
# Stolen by something
'Changeling Young Adult' : {
    'age'     : 5,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'short'   : 'embraced the teachings of the fairies',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Changeling Adult', 'Returned Adult'),
},
'Cultist Young Adult' : {
    'age'     : 5,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'short'   : 'embraced the teachings of the cultists',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Cultist Adult', 'Returned Adult', 'Arrested Adult'),
},
'Initiate Young Adult' : {
    'age'     : 5,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'short'   : 'embraced the teachings of the order',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Initiate Adult', 'Returned Adult'),
},
# Orphaned by something
'Bandit Young Adult' : {
    'age'     : 5,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'short'   : 'chose to join the bandits',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Bandit Adult', 'Returned Adult', 'Arrested Adult'),
},
'Pirate Young Adult' : {
    'age'     : 5,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'short'   : 'chose to join the pirates',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Pirate Adult', 'Returned Adult', 'Arrested Adult'),
},
'Wolf Young Adult' : {
    'age'     : 5,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'short'   : 'chose to stay among the pack',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Wolf Adult', 'Returned Adult'),
},
# Innate talents
'Wizard Young Adult' : {
    'age'     : 5,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'short'   : 'were invited to attend a magic school',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Adult', 'Rich Adult', 'Poor Adult', 'Dedicated Adult', 'Scoundrel Adult', 'Enlisted Adult', 'Wizard Adult', 'Demonslayer'),
},
'Scholar Young Adult' : {
    'age'     : 5,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'short'   : 'had an unnatural aptitude for reading',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Adult', 'Rich Adult', 'Poor Adult', 'Dedicated Adult', 'Scoundrel Adult', 'Enlisted Adult', 'Scholar Adult', 'Demonslayer'),
},
# Military careers
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
    'short'   : 'served as a respected officer',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Adult', 'Rich Adult', 'Poor Adult', 'Dedicated Adult', 'Scoundrel Adult', 'Officer Adult', 'Heroic Adult', 'Demonslayer'),
},
# Crime
'Arrested Young Adult' : {
    'age'     : 5,
    'text'    : "Separated from the civilization of my birth, my upbringing was unusual indeed.",
    'short'   : 'managed to avoid being executed',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Mundane Adult', 'Rich Adult', 'Poor Adult', 'Dedicated Adult', 'Scoundrel Adult', 'Enlisted Adult', 'Prisoner Adult', 'Demonslayer'),
},
# Age 6: Adult (>25 years old)
# Core choices
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
# Raised by someone else
'Adventurer Adult' : {
    'age'     : 6,
    'text'    : "Separated from the civilization of my birth, my upbringing was unusual indeed.",
    'short'   : 'made the hard adjustment back to a normal life',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Demonslayer',),
},
'Church Adult' : {
    'age'     : 6,
    'text'    : "Separated from the civilization of my birth, my upbringing was unusual indeed.",
    'short'   : 'made the hard adjustment back to a normal life',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Demonslayer',),
},
'Returned Adult' : {
    'age'     : 6,
    'text'    : "Separated from the civilization of my birth, my upbringing was unusual indeed.",
    'short'   : 'made the hard adjustment back to a normal life',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Demonslayer',),
},
# Stolen by something
'Changeling Adult' : {
    'age'     : 6,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'short'   : 'were treated as a prince among the fey',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Demonslayer',),
},
'Cultist Adult' : {
    'age'     : 6,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'short'   : 'became a powerful figure within the cult',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Demonslayer',),
},
'Initiate Adult' : {
    'age'     : 6,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'short'   : 'rose to a position of power in the order',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Demonslayer',),
},
# Orphaned by something
'Bandit Adult' : {
    'age'     : 6,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'short'   : 'became a bandit leader',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Demonslayer',),
},
'Pirate Adult' : {
    'age'     : 6,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'short'   : 'became a pirate captain',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Demonslayer',),
},
'Wolf Adult' : {
    'age'     : 6,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'short'   : 'ruled the forests with your pack',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Demonslayer',),
},
# Innate talents
'Wizard Adult' : {
    'age'     : 6,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'short'   : 'were invited to attend a magic school',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Demonslayer',),
},
'Scholar Adult' : {
    'age'     : 6,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'short'   : 'had an unnatural aptitude for reading',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Demonslayer',),
},
# Military careers
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
    'text'    : "served as a respected officer.",
    'short'   : 'served as a respected officer',
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
# Crime
'Arrested Adult' : {
    'age'     : 6,
    'text'    : "Separated from the civilization of my birth, my upbringing was unusual indeed.",
    'short'   : 'managed to avoid being executed',
    'effects' : {},
    'years'   : 6,
    'choices' : ('Demonslayer',),
},
'Prisoner Adult' : {
    'age'     : 6,
    'text'    : "Separated from the civilization of my birth, my upbringing was unusual indeed.",
    'short'   : 'managed to avoid being executed',
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
    'text'    : "I did not want to become a demonslayer, but against the forces of darkness, what choice did I have but to stand? If I hadn't chosen to protect others, there's no guessing whether anyone else would have. It's a lonely calling, but a necessary one, and for now the burden rests on my shoulders.",
    'short'   : 'became a demonslayer to protect others',
    'effects' : {},
    'choices' : ('End',),
},
'Vengeful Demonslayer' : {
    'text'    : "I wish that I could have been content to cower, but I had seen too much bloodshed. Families torn apart. Churches razed. Entire towns swallowed whole by the maw of Chaos. I felt an overpowering urge to destroy as many of these fiends as I could, as soon as I could... before they had a chance to hurt anyone else.",
    'short'   : 'became a demonslayer to seek revenge',
    'effects' : {},
    'choices' : ('End',),
},
'Zealous Demonslayer' : {
    'text'    : "God himself called me to this task. I will listen to Him, and I will obey. The life I've left behind was just an instrument He crafted to prepare me for my true purpose, and when I left it behind it was with no regrets.",
    'short'   : 'became a demonslayer to serve God',
    'effects' : {},
    'choices' : ('End',),
},
# TODO: Weapon text!
'Violent Demonslayer' : {
    'text'    : "I'll slay these abominations until I drown in their blood. Anything that stands before me will meet a swift death, and to anything that flees I'll gift a slow one. Even if they won't stay dead, I'll rip and tear them apart until they get the picture!",
    'short'   : 'became a demonslayer out of lust for violence',
    'effects' : {},
    'choices' : ('End',),
},
'Curious Demonslayer' : {
    'text'    : "I had never truly believed in demons - not until I saw them with my own eyes. I felt like a veil had been pulled back; like I had been given a glimpse of the truth of the world. I purge the abominations wherever I find them, but every night I lay awake and question the reasons for their existence.",
    'short'   : 'became a demonslayer out of curiosity',
    'effects' : {},
    'choices' : ('End',),
},
'Corrupt Demonslayer' : {
    'text'    : "The forces of darkness have vast power. Power you wouldn't believe. It has to be... studied. In time, their dark secrets will be turned against us, and I won't be unprepared.",
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

def full_dot(tree, eventname):
    event = tree.get(eventname, None)
    if event is not None:
        if event.get("choices", None) != None:
            for choice in event["choices"]:
                if choice != '':
                    print "%s -> %s" % (eventname.replace(' ', ''), choice.replace(' ', ''))
                    full_dot(tree, choice)

def dot(tree):
        for name, event in tree.items():
            choices = event.get("choices", None)
            if choices is not None:
                for choice in choices:
                    if choice != '':
                        print "%s -> %s" % (name.replace(' ', ''), choice.replace(' ', ''))

if __name__ == "__main__":

# Print all event names
#    for k, v in eventdata.items():
#        print k

# Print a tree
#    recurse(eventdata, "Start", 0)

# Print DOT language text
    print "digraph Hellmouth {"
    dot(eventdata)
    #full_dot(eventdata, "Start")
    print "}"
