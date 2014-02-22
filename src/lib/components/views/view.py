from src.lib.components.component import Component
from src.lib.components.traits.drawable import Drawable

from src.lib.util import debug
from src.lib.util.geometry.space import Point
from src.lib.util.trait import Trait

@Trait.use(Drawable)
class View(Component):
    # Height and width of `View` content.
    height = 0
    width = 0

    # Like CSS: top, right, bottom, left.
    margin = Point(0, 0, 0, 0)
    border = Point(0, 0, 0, 0)
    padding = Point(0, 0, 0, 0)

    # Total size of the `View`.
    x = 0
    y = 0

    # For navigating within content.
    x_acc = 0
    y_acc = 0

    def __init__(self, layer="default"):
        super(View, self).__init__()
        self._dimensions = Point(0, 0)
        self.layer = layer