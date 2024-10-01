from typing import List

from src.models.box import Box


class Trolley:
    """
    Represents a trolley
    """
    TROLLEY_ID_COUNTER = 1

    id: int
    boxes: List[Box]

    def __init__(self, boxes: List[Box]):
        self.id = Trolley.TROLLEY_ID_COUNTER
        Trolley.TROLLEY_ID_COUNTER += 1
        self.boxes = boxes
