from hitloc import *
from generators import items

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
        for partname, partclass, parent, sublocation, rolls in self.parts:
            part = partclass(partname, owner)
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
                if isinstance(roll, list) is True:
                    base = roll[0]
                    for x in range(len(roll)):
                        if x == 0:
                            continue;
                        subroll = roll[x]
                        self.table["%s-%s" % (base, subroll)] = part
                else:
                    self.table[roll] = part

    # Very simple display of body information.
    def display(self):
        screen = []
        screen.append("")
        screen.append("--Body--")
        screen.append("Size: %s" % self.size)
        screen.append("Shape: %s" % self.shape)
        for loc in self.locs.values():
            if loc is not None:
                screen.extend(loc.display())
        return screen

    # Implement this for anything that needs a paperdoll.
    def paperdoll(self):
        return False

class Humanoid(BodyPlan):
    # These tuples represent:
    # 1: Part name.
    # 2: Class.
    # 2: Parent part. Only list parts that have already been listed.
    # 3: True if it's a sublocation rather than a real one.
    # 4: List representing what 3d6 rolls hit that spot.
    #    If a further d6 roll is required, use a list like:
    #        [15, [16, 1, 2, 3], 17]
    parts = (
             ('Torso', HitLoc, None, False, [9, 10]),
             ('Groin', HitLoc, 'Torso', False, [11]),
             ('Neck', Neck, 'Torso', False, [17, 18]),
             ('Skull', Skull, 'Neck', False, [3, 4]),
             ('Face', Face, 'Skull', False, [5]),
             ('RArm', Limb, 'Torso', False, [8]),
             ('LArm', Limb, 'Torso', False, [12]),
             ('RHand', Extremity, 'RArm', False, [15, 1, 2, 3]),
             ('LHand', Extremity, 'LArm', False, [15, 4, 5, 6],),
             ('RLeg', Limb, 'Groin', False, [6, 7]),
             ('LLeg', Limb, 'Groin', False, [13, 14]),
             ('RFoot', Extremity, 'RLeg', False, [[16, 1, 2, 3]]),
             ('LFoot', Extremity, 'LLeg', False, [[16, 4, 5, 6]]),
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
        list.append('    <%s>[</>%s<%s>]</>   ' % (p.loccol('Skull'), p.locdr('Skull'), p.loccol('Skull')))
        list.append('  <%s>.--</><%s>+</><%s>--.</> ' % (p.loccol('LArm'), p.loccol('Neck'), p.loccol('RArm')))
        list.append(' %s<%s>|</> <%s>=</>%s<%s>=</> <%s>|</>%s' % (p.locdr('LArm'), p.loccol('LArm'), p.loccol('Torso'), p.locdr('Torso'), p.loccol('Torso'), p.loccol('RArm'), p.locdr('RArm')))
        list.append(' %s<%s>\'</> <%s>-|-</> <%s>\'</>%s ' % (p.locdr('LHand'), p.loccol('LHand'), p.loccol('Torso'), p.loccol('RHand'), p.locdr('RHand')))
        list.append('   <%s>.\</><%s>=</><%s>/.</>   ' % (p.loccol('LLeg'), p.loccol('Groin'), p.loccol('RLeg')))
        list.append('  %s<%s>|</>   <%s>|</>%s  ' % (p.locdr('LLeg'), p.loccol('LLeg'), p.loccol('RLeg'), p.locdr('RLeg')))
        list.append('   <%s>|</>   <%s>|</>   ' % (p.loccol('LLeg'), p.loccol('RLeg')))
        list.append(' %s<%s>--</>   <%s>--</>%s ' % (p.locdr('LFoot'), p.loccol('LFoot'), p.loccol('RFoot'), p.locdr('RFoot')))
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

