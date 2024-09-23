from abc import ABC, abstractmethod
from pathlib import Path
from typing import NoReturn

from src.models.instance_data import InstanceData


class BaseInstanceParserModule(ABC):
    """
    Base module to parse an instance file
    """
    instance_filepath: Path

    def __init__(self, instance_filepath: Path) -> NoReturn:
        self.instance_filepath = instance_filepath

    @abstractmethod
    def run(self) -> InstanceData:
        raise NotImplementedError()
