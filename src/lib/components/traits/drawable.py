from src.lib.util.geometry.space import Point
from src.lib.util.trait import Trait

class Drawable(Trait):
    """Provides the ability to be drawn."""
    # The position to be drawn at.
    position = Point(0, 0)

    @Trait.include
    def __draw__(self, layer):
        """Draw this View on a layer."""
        # TODO: Move this somewhere more sensible
        self.reset(layer)
        self.before_draw(layer)
        self.draw(layer)

    def before_draw(self, layer):
        """Abstract. Do something before drawing yourself."""
        pass

    def draw(self, layer):
        """Abstract. Draw self."""
        pass

    def reset(self, layer):
        """Resets drawing variables before each draw."""
        # The edges around the content.
        top, right, bottom, left = zip(self.margin, self.border, self.padding)

        # The uppermost row of the content.
        self.top = sum(top)
        # The leftmost column of the content.
        self.left = sum(left)
        # The lowermost row of the content.
        self.bottom = self.top + self.height - 1
        # The rightmost column of the content.
        self.right = self.left + self.width - 1

        # The total space taken up by the `View`.
        self.x = self.width + self.left + sum(right)
        self.y = self.height + self.top + sum(bottom)

        # Cumulative x/y tracking.
        self.x_acc = 0
        self.y_acc = 0

        # Available width/height.
        # self.width = self.x - 2*edge_x
        # assert self.width > 0, "Width was below 1 after box model: %s" % self.__dict__
        # self.height = self.y -2*edge_y
        # assert self.height > 0, "Height was below 1 after box model: %s" % self.__dict__