from pathlib import Path
from typing import Type

from src.modules.check_boxes_are_valid.base import BaseCheckBoxesAreValidModule
from src.modules.check_boxes_are_valid.check_boxes_module import CheckBoxesModule
from src.modules.check_trolleys_are_valid.base import BaseCheckTrolleysAreValidModule
from src.modules.check_trolleys_are_valid.check_trolleys_module import CheckTrolleysModule
from src.modules.export_solution.base import BaseExportSolutionModule
from src.modules.export_solution.export_solution_module import ExportSolutionModule
from src.modules.instance_parser.base import BaseInstanceParserModule
from src.modules.instance_parser.instance_parser import InstanceParserModule
from src.modules.organise_boxes.OrganiseBoxesDummy import OrganiseBoxesDummy
from src.modules.organise_boxes.base import BaseOrganiseBoxesModule
from src.modules.organise_trolleys.base import BaseOrganiseTrolleysModule
from src.modules.organise_trolleys.dummy import DummyOrganiseTrolleysModule


def execute_workflow(
        instance_file_path: Path,
        solution_file_path: Path,
        instance_parser_module_cls: Type[BaseInstanceParserModule],
        organise_boxes_module_cls: Type[BaseOrganiseBoxesModule],
        check_boxes_are_valid_module_cls: Type[BaseCheckBoxesAreValidModule],
        organise_trolleys_module_cls: Type[BaseOrganiseTrolleysModule],
        check_trolleys_are_valid_module_cls: Type[BaseCheckTrolleysAreValidModule],
        export_solution_module_cls: Type[BaseExportSolutionModule],
):
    instance_parser = instance_parser_module_cls(instance_file_path)
    instance_data = instance_parser.run()
    boxes = organise_boxes_module_cls(instance_data).run()
    # Throws an exception if the boxes are not valid
    check_boxes_are_valid_module_cls(instance_data, boxes).run()

    trolleys = organise_trolleys_module_cls(instance_data, boxes).run()
    # Throws an exception if the trolleys are not valid
    check_trolleys_are_valid_module_cls(instance_data, boxes, trolleys).run()

    export_solution_module_cls(solution_file_path, instance_data, boxes, trolleys).run()


if __name__ == '__main__':
    INSTANCE_FILE_PATH = Path('data/instance.txt')
    SOLUTION_FILE_PATH = Path('data/solution.txt')

    execute_workflow(INSTANCE_FILE_PATH, SOLUTION_FILE_PATH, InstanceParserModule, OrganiseBoxesDummy, CheckBoxesModule,
                     DummyOrganiseTrolleysModule, CheckTrolleysModule, ExportSolutionModule)
