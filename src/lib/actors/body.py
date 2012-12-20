from hitloc import *
from generators import items
from operator import attrgetter

# Body layouts - humanoid, hexapod, etc.
class BodyPlan:
    def __init__(self, parent):
        self.parent = parent
        # Size (0 for a human)
        self.size = None
        # Shape (tall, long, or full)
        self.shape = None
        # Body parts indexed by key
        self.locs = {}
        # Body parts indexed by 3d6 roll
        self.table = {}
        # Primary slot
#        self.primary_slot = None

    # Build a body from the class information.
    def build(self, owner):
        for order, partname, partclass, parent, sublocation, rolls in self.parts:
            part = partclass(partname, owner)
            part.sorting = order
            self.locs[partname] = part

            # Generate natural weapons.
            weapons = self.weapons.get(partname)
            if weapons is not None:
                for weapon in weapons:
                    # List, for consistency elsewhere.
                    part.attack_options[weapon] = [items.generate_item(weapon)]

            # Set up relationships between parts.
            if parent is not None:
                HitLoc.add_child(self.locs[parent], part)

            # Add the location to the hit location chart.
            for roll in rolls:
                if isinstance(roll, tuple) is True:
                    base, subrolls = roll
                    for subroll in subrolls:
                        self.table["%s-%s" % (base, subroll)] = part
                else:
                    self.table[roll] = part

    # Very simple display of body information.
    def display(self):
        screen = []
        screen.append("")
        screen.append("--Body--")
#        screen.append("Size: %s" % self.size)
#        screen.append("Shape: %s" % self.shape)
        for loc in sorted(sorted(self.locs.values(), key=attrgetter("type"), reverse=True), key=attrgetter("sorting")):
            if loc is not None:
                screen.extend(loc.display())
        return screen

    # Implement this for anything that needs a paperdoll.
    def paperdoll(self):
        return False

class Humanoid(BodyPlan):
    # These tuples represent:
    # 1: Sorting order (lowest first).
    # 2: Part name.
    # 3: Class.
    # 4: Parent part. Only list parts that have already been listed.
    # 5: True if it's a sublocation rather than a real one.
    # 6: List representing what 3d6 rolls hit that spot.
    #    If a further d6 roll is required, use a list like:
    #        [15, [16, 1, 2, 3], 17]
    parts = (
             (2, 'Torso', HitLoc, None, False, [9, 10]),
             (1, 'Neck', Neck, 'Torso', False, [17, 18]),
             (1, 'Skull', Skull, 'Neck', False, [3, 4]),
             (1, 'Face', Face, 'Skull', False, [5]),
             (3, 'RArm', Limb, 'Torso', False, [8]),
             (3, 'LArm', Limb, 'Torso', False, [12]),
             (4, 'RHand', Extremity, 'RArm', False, [(15, (1, 2, 3))]),
             (4, 'LHand', Extremity, 'LArm', False, [(15, (4, 5, 6))]),
             (5, 'Groin', HitLoc, 'Torso', False, [11]),
             (6, 'RLeg', Leg, 'Groin', False, [6, 7]),
             (6, 'LLeg', Leg, 'Groin', False, [13, 14]),
             (7, 'RFoot', Foot, 'RLeg', False, [(16, (1, 2, 3))]),
             (7, 'LFoot', Foot, 'LLeg', False, [(16, (4, 5, 6))]),
    )

    primary_slot = 'RHand'

    weapons = {
        'RHand' : ("fist",),
        'LHand' : ("fist",),
#        'RFoot' : ("kick"),
#        'LFoot' : ("kick"),
    }

    def __init__(self, parent):
        BodyPlan.__init__(self, parent)
        self.build(parent)
    def paperdoll(self):
        p = self.parent
        list = []

# Small size:
############
#    [ ]   #
#  .--+--. #
#  | = = | #
#  ' -|- ' #
#   .\=/.  #
#   |   |  #
#   |   |  #
#  --   -- #
############

        list.append('    <%s>[</>%s<%s>]</>   ' % (p.loccol('Skull'), p.locdr('Skull'), p.loccol('Skull')))
        list.append('  <%s>.--</><%s>+</><%s>--.</> ' % (p.loccol('LArm'), p.loccol('Neck'), p.loccol('RArm')))
        list.append(' %s<%s>|</> <%s>=</>%s<%s>=</> <%s>|</>%s' % (p.locdr('LArm'), p.loccol('LArm'), p.loccol('Torso'), p.locdr('Torso'), p.loccol('Torso'), p.loccol('RArm'), p.locdr('RArm')))
        list.append(' %s<%s>\'</> <%s>-|-</> <%s>\'</>%s ' % (p.locdr('LHand'), p.loccol('LHand'), p.loccol('Torso'), p.loccol('RHand'), p.locdr('RHand')))
        list.append('   <%s>.\</><%s>=</><%s>/.</>   ' % (p.loccol('LLeg'), p.loccol('Groin'), p.loccol('RLeg')))
        list.append('  %s<%s>|</>   <%s>|</>%s  ' % (p.locdr('LLeg'), p.loccol('LLeg'), p.loccol('RLeg'), p.locdr('RLeg')))
        list.append('   <%s>|</>   <%s>|</>   ' % (p.loccol('LLeg'), p.loccol('RLeg')))
        list.append(' %s<%s>--</>   <%s>--</>%s ' % (p.locdr('LFoot'), p.loccol('LFoot'), p.loccol('RFoot'), p.locdr('RFoot')))
        return list

class Vermiform(BodyPlan):
    # These tuples represent:
    # 1: Sorting order (lowest first).
    # 2: Part name.
    # 3: Class.
    # 4: Parent part. Only list parts that have already been listed.
    # 5: True if it's a sublocation rather than a real one.
    # 6: List representing what 3d6 rolls hit that spot.
    #    If a further d6 roll is required, use a list like:
    #        [15, [16, 1, 2, 3], 17]
    parts = (
             (2, 'Torso', HitLoc, None, False, range(9, 18+1)),
             (1, 'Neck', Neck, 'Torso', False, [6, 7, 8]),
             (1, 'Skull', Skull, 'Neck', False, [3, 4]),
             (1, 'Face', Face, 'Skull', False, [5]),
    )

    primary_slot = None

    weapons = {
        'Skull' : ("sharp teeth",),
    }

    def __init__(self, parent):
        BodyPlan.__init__(self, parent)
        self.build(parent)
    def paperdoll(self):
        p = self.parent
        list = []

# Small paperdoll:
############
#   _____  #
#  / __ n\ #
# / /  \  \#
#/t/   /s o#
#\ \   \/\/#
# \ \___// #
#  \____/  #
#          #
############
# n = neck
# s = skull
# t = torso
        list.append('  <%s> _____</>  ' % p.loccol('Torso'))
        list.append('  <%s>/ __</> %s<%s>\</> ' % (p.loccol('Torso'), p.locdr('Neck'), p.loccol('Neck')))
        list.append(' <%s>/ /</>  <%s>\</>  <%s>\</>' % (p.loccol('Torso'), p.loccol('Neck'), p.loccol('Skull')))
        list.append('<%s>/</>%s<%s>/</>   <%s>/</>%s o' % (p.loccol('Torso'), p.locdr('Torso'), p.loccol('Torso'), p.loccol('Skull'), p.locdr('Skull')))
        list.append('<%s>\ \</>   <%s>\/\/</>' % (p.loccol('Torso'), p.loccol('Face')))
        list.append('<%s> \ \___//</> ' % p.loccol('Torso'))
        list.append('<%s>  \____/</>  ' % p.loccol('Torso'))
        list.append('')
        return list

class Octopod(BodyPlan):
    # See Humanoid for a description.
    parts = (
             ('Mantle', None, None),
             ('Arm1', 'Mantle', None),
             ('Arm2', 'Mantle', None),
             ('Arm3', 'Mantle', None),
             ('Arm4', 'Mantle', None),
             ('Arm5', 'Mantle', None),
             ('Arm6', 'Mantle', None),
             ('Arm7', 'Mantle', None),
             ('Arm8', 'Mantle', None),
    )

    primary_slot = 'Arm1'

    def __init__(self, parent):
        BodyPlan.__init__(self, parent)
        self.build(parent)

# WIP:
# Winged Humanoid
#/-\ [ ] /-\
#| .--+--. |
#/ | = = | \
#  ' -|- ' 
#   .\=/.  
#   |   |  
#   |   |  
#  --   -- 

# Quadruped
#/-\ [ ] /-\
#| .--+--. |
#/ | = = | \
#  ' -|- ' 
#   .\=/.  
#   |   |  
#   |   |  
#  --   -- 
# *Taur
#     ( )   
#  , .-|-. ,
#  \/ = = \|
#   ___-\-  
#.:(______)
#: |\   |  \
# / |   |  / 
#"  "   "  "

# Snaketaur
#    ( )   
#  .--|--. ,
# /  = =  \|
# \,  -\-   
# ___ \ \ \  
#// _) | \ \
#\\____/ | |
# \_______/

# Humanoid
#    ( )
#  .--|--.
# /  = =  \
# \  -|-   | 
#  '.\-/.  ' 
#   |    \ 
#   |    / 
#  _|   /_ 

# Winged Humanoid
#/-\     /-\
#|,,\( )/,,|
#/ .--|--. \
# /  = =  \ 
#/   -|-   \ 
#`  .\-/.  '
#  /     \ 
#  _\   /_ 

# Avian
#/-\  __ /-\
#|,,\/o_\,,|
#|,,/  \),,|
#/,,|   /,,\
#,, |   | ,,
#,  .\ /.  ,
#  / |\  \  
#,`, |_\ ,`,

# Spidertaur
# /` ( )   
# \.--+--. ,
#  __ = = \|
# /  \_-\-  
# \/_/_/_/)
# /\/\/\/\
#| |\|\|\ \

# Arachnoid-
#__  /^\  __
# _\(   )/_
#/ \\\ /// \
# __\) (/__
#/ /( ::)\ \
#| | \;;/ || 
#\ \     / /   
#    

# Humanoid
#    ( )
#  .--|--.
# /  = =  \
# \  -|-   | 
#  '.\-/.  ' 
#   |    \ 
#   |    / 
#  _|   /_ 

# ??? 
#0    o   0
#,,'`',`'',`',,
#`',,   ,'`,'` o
# O  `'' 0

# Devil
#/-\ ( ) /-\
#| .'-|-'. |
#'/  = = | '
# \, -|- \,   
# `'.\-/. '`
#   \ | / 
#   / v \
#  m     m

# Devil
# /\ ( ) /\
#/ .>-|-<. \
#^/  = = |^^ 
# \, -|- \,   
# `'.\-/.' `
#   \ | / 
#   / v \
#  n     n

# Octopod
#     _   
# _  /4)   _ 
#(3\ \ _  /5)
# _ \ / \/ 
#(2) (   )__ 
# \__/\w/  6)
# __/ /  \_    
#(1  (8   7)
#

# Much better octopod
#     _   _
# _  / ) ( )
#( \ \___ \
# _ \(   )/_
#( ) (   o) )
# \__/\, /\  
# __/ /``  )     
#(   (    (

# Hexapod---
#       _
# ___  / __ 
#/   \_\/__\
#\___/  \_ \
#  __\__/ \
# / /|  \_/
#  / |  { }

# ___      
#/   \  __   
#\___/_/ __
# __/  \/__
#/ _\__/   \
# / / / \  
#/ |  \_/
#     { }