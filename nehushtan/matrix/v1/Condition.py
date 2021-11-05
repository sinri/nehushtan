class Condition:
    """
    An abstract class
    """

    def __init__(self):
        self.target = None  # index / column name
        self.comparator = None
        self.object = None

    def compute_with_row(self, row) -> bool:
        pass
