from abc import ABC, abstractmethod
from typing import NoReturn

from src.models.box import Box
from src.models.instance_data import InstanceData
from src.models.trolley import Trolley


class BaseCheckTrolleysAreValidModule(ABC):
    """
    Base module to check if the trolleys are valid
    """
    instance_data: InstanceData
    boxes: list[Box]
    trolleys: list[Trolley]

    def __init__(self, instance_data: InstanceData, boxes: list[Box], trolleys: list[Trolley]):
        self.instance_data = instance_data
        self.boxes = boxes
        self.trolleys = trolleys

    @abstractmethod
    def run(self) -> NoReturn:
        raise NotImplementedError()
