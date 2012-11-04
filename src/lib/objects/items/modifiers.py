class Modifier:
    dr = 0

# Materials
class Meat(Modifier):
    appearance = "meat"
    dr = 1

class Bone(Modifier):
    appearance = "bone"
    dr = 2

# Construction
class Thin(Modifier):
    appearance = "thin"
    dr = -1

class Thick(Modifier):
    appearance = "thick"
    dr = 1

# Quality
class Cheap(Modifier):
    appearance = "cheap"

class Fine(Modifier):
    appearance = "fine"

class VeryFine(Modifier):
    appearance = "very fine"


