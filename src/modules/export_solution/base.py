from abc import abstractmethod, ABC
from pathlib import Path
from typing import NoReturn

from src.models.box import Box
from src.models.instance_data import InstanceData
from src.models.trolley import Trolley


class BaseExportSolutionModule(ABC):
    """
    Base module to export a solution
    """
    solution_filepath: Path
    instance_data: InstanceData
    boxes: list[Box]
    trolleys: list[Trolley]

    def __init__(self, solution_filepath: Path, instance_data: InstanceData, boxes: list[Box],
                 trolleys: list[Trolley]) -> NoReturn:
        self.solution_filepath = solution_filepath
        self.instance_data = instance_data
        self.boxes = boxes
        self.trolleys = trolleys

    @abstractmethod
    def run(self) -> NoReturn:
        raise NotImplementedError()
