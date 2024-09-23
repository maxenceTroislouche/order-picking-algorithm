from abc import ABC, abstractmethod
from typing import NoReturn

from src.models.box import Box
from src.models.instance_data import InstanceData


class BaseOrganiseBoxesModule(ABC):
    """
    Base module to organise boxes
    """
    instance_data: InstanceData

    def __init__(self, instance_data: InstanceData) -> NoReturn:
        self.instance_data = instance_data

    @abstractmethod
    def run(self) -> list[Box]:
        raise NotImplementedError()
