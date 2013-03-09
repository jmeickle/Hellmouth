from src.lib.agents.components.bodies.parts import *
from src.lib.generators import items
from operator import attrgetter

from src.lib.agents.components.component import Component, ignore_results

# Body layouts - humanoid, hexapod, etc.
class Body(Component):
    commands = []
        
    def __init__(self, owner):
        super(Body, self).__init__(owner)
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
        self.build(self.owner)

    @ignore_results
    def get_worn(self, *args, **kwargs):
        for loc in self.locs.values():
            yield loc.appearance(), loc.worn

    def get_part(self, part_name):
        """Return the part matching a part name."""
        return self.locs.get(part_name)

    # TODO: Filter?
    def get_parts(self):
        """Generate all parts."""
        for part in self.locs.values():
            yield part

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
                BodyPart.add_child(self.locs[parent], part)

            # Add the location to the hit location chart.
            for roll in rolls:
                if isinstance(roll, tuple) is True:
                    base, subrolls = roll
                    for subroll in subrolls:
                        self.table["%s-%s" % (base, subroll)] = part
                else:
                    self.table[roll] = part

    # Very simple display of body information.
    # TODO: Deprecated.
    def get_view_data(self):
        for loc in sorted(sorted(self.locs.values(), key=attrgetter("type"), reverse=True), key=attrgetter("sorting")):
            if loc is not None:
                for line in loc.get_view_data():
                    yield line

    def get_paperdoll_part_colors(self, part, fg=True, bg=True):
        """Return the colors matching a part."""
        if part:
            return part.get_color(fg, bg)
        else:
            if fg and bg:
                return "black-black"
            else:
                return "black"

    def get_paperdoll_part_dr_colors(self, part, fg=True, bg=True):
        """Return the DR colors matching a part."""
        if part:
            return part.get_dr_colors(fg, bg)
        else:
            if fg and bg:
                return "black-black"
            else:
                return "black"

    def get_paperdoll_part_dr_glyph(self, part):
        """Return the DR glyph matching a part."""
        if part is None or part.severed() is True:
            return " "
        else:
            return part.get_dr_glyph()

    def get_paperdoll_parts(self, part_name):
        part = self.get_part(part_name)
        return self.get_paperdoll_part_colors(part), '<%s>%s</>' % (self.get_paperdoll_part_dr_colors(part), self.get_paperdoll_part_dr_glyph(part))

    # Implement this for anything that needs a paperdoll.
    def get_paperdoll(self):
        """Return this body's ASCII paperdoll."""
        yield ''

class Humanoid(Body):
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
             (2, 'Torso', BodyPart, None, False, [9, 10]),
             (1, 'Neck', Neck, 'Torso', False, [17, 18]),
             (1, 'Skull', Skull, 'Neck', False, [3, 4]),
             (1, 'Face', Face, 'Skull', False, [5]),
             (3, 'RArm', Limb, 'Torso', False, [8]),
             (3, 'LArm', Limb, 'Torso', False, [12]),
             (4, 'RHand', Hand, 'RArm', False, [(15, (1, 2, 3))]),
             (4, 'LHand', Hand, 'LArm', False, [(15, (4, 5, 6))]),
             (5, 'Groin', BodyPart, 'Torso', False, [11]),
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

    @ignore_results
    def get_paperdoll(self):

        # Small paperdoll:

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

        s, S = self.get_paperdoll_parts('Skull')
        n, N = self.get_paperdoll_parts('Neck')
        la, LA = self.get_paperdoll_parts('LArm')
        ra, RA = self.get_paperdoll_parts('RArm')
        lh, LH = self.get_paperdoll_parts('LHand')
        rh, RH = self.get_paperdoll_parts('RHand')
        t, T = self.get_paperdoll_parts('Torso')
        g, G = self.get_paperdoll_parts('Groin')
        ll, LL = self.get_paperdoll_parts('LLeg')
        rl, RL = self.get_paperdoll_parts('RLeg')
        lf, LF = self.get_paperdoll_parts('LFoot')
        rf, RF = self.get_paperdoll_parts('RFoot')

        yield '    <%s>[</>%s<%s>]</>   ' % (s, S, s)
        yield '  <%s>.--</><%s>+</><%s>--.</> ' % (la, n, ra)
        yield ' %s<%s>|</> <%s>=</>%s<%s>=</> <%s>|</>%s' % (LA, la, t, T, t, ra, RA)
        yield ' %s<%s>\'</> <%s>-|-</> <%s>\'</>%s ' % (LH, lh, t, rh, RH)
        yield '   <%s>.\</><%s>=</><%s>/.</>   ' % (ll, g, rl)
        yield '  %s<%s>|</>   <%s>|</>%s  ' % (LL, ll, rl, RL)
        yield '   <%s>|</>   <%s>|</>   ' % (ll, rl)
        yield ' %s<%s>--</>   <%s>--</>%s ' % (LF, lf, rf, RF)


class Vermiform(Body):
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
             (2, 'Torso', BodyPart, None, False, range(9, 18+1)),
             (1, 'Neck', Neck, 'Torso', False, [6, 7, 8]),
             (1, 'Skull', Skull, 'Neck', False, [3, 4]),
             (1, 'Face', Face, 'Skull', False, [5]),
    )

    primary_slot = None

    weapons = {
        'Skull' : ("sharp teeth",),
    }

    @ignore_results
    def get_paperdoll(self):

        # Small paperdoll:

        ############
        #   _____  #
        #  / __ N\ #
        # / /  \  \#
        #/T/   /S o#
        #\ \   \/\/#
        # \ \___// #
        #  \____/  #
        #          #
        ############

        f, F = self.get_paperdoll_parts('Face')
        n, N = self.get_paperdoll_parts('Neck')
        s, S = self.get_paperdoll_parts('Skull')
        t, T = self.get_paperdoll_parts('Torso')

        yield '  <%s> _____</>  ' % t
        yield '  <%s>/ __</> %s<%s>\</> ' % (t, N, n)
        yield ' <%s>/ /</>  <%s>\</>  <%s>\</>' % (t, n, s)
        yield '<%s>/</>%s<%s>/</>   <%s>/</>%s o' % (t, T, t, s, S)
        yield '<%s>\ \</>   <%s>\/\/</>' % (t, f)
        yield '<%s> \ \___//</> ' % t
        yield '<%s>  \____/</>  ' % t
        yield ''

class Octopod(Body):
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
