from enum import Enum


class Actions(Enum):
    """Models all possible actions."""
    top_left: int = 0
    top_center: int = 1
    top_right: int = 2
    middle_left: int = 3
    middle_center: int = 4
    middle_right: int = 5
    bottom_left: int = 6
    bottom_center: int = 7
    bottom_right: int = 8
