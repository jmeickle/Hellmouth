import drawing
from hitloc import HitLoc

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
        self.primary_slot = None

    # Build a body from the class information.
    def build(self, owner):
        for partname, parent, sublocation, rolls in self.parts:
            part = HitLoc(partname, owner)
            self.locs[partname] = part
            if parent is not None:
                HitLoc.add_child(self.locs[parent], part)
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

    # Implement this for anything that needs a paperdoll.
    def paperdoll(self):
        return False

class Humanoid(BodyPlan):
    # These tuples represent:
    # 1: Part name.
    # 2: Parent part. Only list parts that have already been listed.
    # 3: True if it's a sublocation rather than a real one.
    # 4: List representing what 3d6 rolls hit that spot.
    #    If a further d6 roll is required, use a list like:
    #        [15, [16, 1, 2, 3], 17]
    parts = (
             ('Torso', None, False, [9, 10]),
             ('Groin', 'Torso', False, [11]),
             ('Neck', 'Torso', False, [17, 18]),
             ('Head', 'Neck', False, [3, 4, 5]),
             ('RArm', 'Torso', False, [8]),
             ('LArm', 'Torso', False, [12]),
             ('RHand', 'RArm', False, [15, 1, 2, 3]),
             ('LHand', 'LArm', False, [15, 4, 5, 6],),
             ('RLeg', 'Groin', False, [6, 7]),
             ('LLeg', 'Groin', False, [13, 14]),
             ('RFoot', 'RLeg', False, [[16, 1, 2, 3]]),
             ('LFoot', 'LLeg', False, [[16, 4, 5, 6]]),
    )

    primary_slot = 'RHand'

    def __init__(self, parent):
        BodyPlan.__init__(self, parent)
        self.build(parent)

    def paperdoll(self):
        p = self.parent
        list = []
        list.append('    <%s>[</>%s<%s>]</>   ' % (p.loccol('Head'), p.wound('Head'), p.loccol('Head')))
        list.append('  <%s>.--</><%s>+</><%s>--.</> ' % (p.loccol('LArm'), p.loccol('Torso'), p.loccol('RArm')))
        list.append(' %s<%s>|</> <%s>=</>%s<%s>=</> <%s>|</>%s' % (p.wound('LArm'), p.loccol('LArm'), p.loccol('Torso'), p.wound('Torso'), p.loccol('Torso'), p.loccol('RArm'), p.wound('RArm')))
        list.append(' %s<%s>.</> <%s>-|-</> <%s>.</>%s ' % (p.wound('LHand'), p.loccol('LHand'), p.loccol('Torso'), p.loccol('RHand'), p.wound('RHand')))
        list.append('   <%s>.-</><%s>|</><%s>-.</>   ' % (p.loccol('LLeg'), p.loccol('Groin'), p.loccol('RLeg')))
        list.append('  %s<%s>|</>   <%s>|</>%s  ' % (p.wound('LLeg'), p.loccol('LLeg'), p.loccol('RLeg'), p.wound('RLeg')))
        list.append('   <%s>|</>   <%s>|</>   ' % (p.loccol('LLeg'), p.loccol('RLeg')))
        list.append(' %s<%s>--</>   <%s>--</>%s ' % (p.wound('LFoot'), p.loccol('LFoot'), p.loccol('RFoot'), p.wound('RFoot')))
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

