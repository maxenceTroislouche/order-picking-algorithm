from abc import ABC, abstractmethod
from typing import NoReturn

from src.models.box import Box
from src.models.instance_data import InstanceData


class BaseCheckBoxesAreValidModule(ABC):
    """
    Base module to check if the boxes are valid
    """
    instance_data: InstanceData
    boxes: list[Box]

    def __init__(self, instance_data: InstanceData, boxes: list[Box]) -> NoReturn:
        self.instance_data = instance_data
        self.boxes = boxes

    @abstractmethod
    def run(self) -> NoReturn:
        raise NotImplementedError()
