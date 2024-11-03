from pathlib import Path
from typing import Type

from src.models.trolley import Trolley
from src.modules.check_boxes_are_valid.base import BaseCheckBoxesAreValidModule
from src.modules.check_boxes_are_valid.check_boxes_module import CheckBoxesModule
from src.modules.check_trolleys_are_valid.base import BaseCheckTrolleysAreValidModule
from src.modules.check_trolleys_are_valid.check_trolleys_module import CheckTrolleysModule
from src.modules.export_solution.base import BaseExportSolutionModule
from src.modules.export_solution.export_solution_module import ExportSolutionModule
from src.modules.instance_parser.base import BaseInstanceParserModule
from src.modules.instance_parser.instance_parser import InstanceParserModule
from src.modules.organise_boxes.OrganiseBoxesDummy import OrganiseBoxesDummy
from src.modules.organise_boxes.OrganiseBoxesV1 import OrganiseBoxesV1
from src.modules.organise_boxes.base import BaseOrganiseBoxesModule
from src.modules.organise_trolleys.base import BaseOrganiseTrolleysModule
from src.modules.organise_trolleys.dummy import DummyOrganiseTrolleysModule
from src.modules.organise_trolleys.dummyv2 import DummyOrganiseTrolleysModuleV2
from src.utils.checker import get_checker_data, write_results
from src.utils.instance import get_instance_files, get_solution_file_path
from src.models.box import Box


def reset_state():
    Box.BOX_ID_COUNTER = 1
    Trolley.TROLLEY_ID_COUNTER = 1
    ExportSolutionModule.file_string = []


def execute_workflow_dummy(instance_file_path: Path, solution_file_path: Path):
    instance_data = InstanceParserModule(instance_file_path).run()
    boxes = OrganiseBoxesDummy(instance_data).run()
    CheckBoxesModule(instance_data, boxes).run()
    trolleys = DummyOrganiseTrolleysModule(instance_data, boxes).run()
    CheckTrolleysModule(instance_data, boxes, trolleys).run()
    ExportSolutionModule(solution_file_path, instance_data, boxes, trolleys).run()


def execute_workflow_v1(instance_file_path: Path, solution_file_path: Path):
    instance_data = InstanceParserModule(instance_file_path).run()
    boxes = OrganiseBoxesV1(instance_data).run()
    CheckBoxesModule(instance_data, boxes).run()
    print("Organisation finished ! ")
    trolleys = DummyOrganiseTrolleysModuleV2(instance_data, boxes).run()
    CheckTrolleysModule(instance_data, boxes, trolleys).run()
    print("Trolleys checked ! ")
    ExportSolutionModule(solution_file_path, instance_data, boxes, trolleys).run()


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
    print("Organise boxes valid ! ")

    trolleys = organise_trolleys_module_cls(instance_data, boxes).run()
    # Throws an exception if the trolleys are not valid
    check_trolleys_are_valid_module_cls(instance_data, boxes, trolleys).run()

    export_solution_module_cls(solution_file_path, instance_data, boxes, trolleys).run()


if __name__ == '__main__':
    INSTANCE_DIRECTORY = Path('../instances')
    SOLUTION_DIRECTORY = Path('../solutions')
    RESULT_FILE = Path('results_dummy.csv')

    # list instances files
    instance_files = get_instance_files(INSTANCE_DIRECTORY)
    instance_and_solution_files = []

    checker_data = []

    for instance_file in instance_files:
        # create solution file path from instance file path
        solution_file = get_solution_file_path(SOLUTION_DIRECTORY, instance_file)
        instance_and_solution_files.append((instance_file, solution_file))

        # reset counters
        Box.BOX_ID_COUNTER = 1
        ExportSolutionModule.file_string = []

        try:
            # execute workflow for each instance file
            execute_workflow_v1(instance_file, solution_file)
        except Exception as e:
            print(f"Error while processing {instance_file}: {e}")

    for instance_file, solution_file in instance_and_solution_files:
        # check each solution file
        if solution_file.exists():
            number_of_trolleys, number_of_boxes, total_distance = get_checker_data(instance_file, solution_file)
        else:
            number_of_trolleys, number_of_boxes, total_distance = -1, -1, -1

        checker_data.append((instance_file, solution_file, number_of_trolleys, number_of_boxes, total_distance))

    # store results in a csv file
    write_results(checker_data, Path(RESULT_FILE))
