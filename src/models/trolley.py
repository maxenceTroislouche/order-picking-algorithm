from typing import List

from src.models.box import Box


class Trolley:
    """
    Represents a trolley
    """
    boxes: List[Box]

    def __init__(self, boxes: List[Box]):
        self.boxes = boxes
