from abc import abstractmethod, ABC

from models.instance_data import InstanceData
from models.box import Box
from models.trolley import Trolley


class BaseOrganiseTrolleysModule(ABC):
    """
    Base module to organise Trolleys
    """
    instance_data: InstanceData
    boxes: list[Box]

    def __init__(self, instance_data: InstanceData, boxes: list[Box]):
        self.instance_data = instance_data
        self.boxes = boxes

    @abstractmethod
    def run(self) -> list[Trolley]:
        raise NotImplementedError()
