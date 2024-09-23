from abc import abstractmethod, ABC
from pathlib import Path
from typing import NoReturn


class BaseExportSolutionModule(ABC):
    """
    Base module to export a solution
    """
    solution_filepath: Path

    def __init__(self, solution_filepath: Path) -> NoReturn:
        self.solution_filepath = solution_filepath

    @abstractmethod
    def run(self) -> NoReturn:
        raise NotImplementedError()
