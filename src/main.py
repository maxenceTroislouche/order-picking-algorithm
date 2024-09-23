from typing import Type

from src.modules.export_solution.base import BaseExportSolutionModule
from src.modules.instance_parser.base import BaseInstanceParserModule
from src.modules.organise_boxes.base import BaseOrganiseBoxesModule
from src.modules.organise_trolleys.base import BaseOrganiseTrolleysModule


def execute_workflow(
        instance_parser_module_cls: Type[BaseInstanceParserModule],
        organise_boxes_module_cls: Type[BaseOrganiseBoxesModule],
        organise_trolleys_module_cls: Type[BaseOrganiseTrolleysModule],
        export_solution_module_cls: Type[BaseExportSolutionModule],
):
    pass


if __name__ == '__main__':
    execute_workflow(BaseInstanceParserModule, BaseOrganiseBoxesModule,
                     BaseOrganiseTrolleysModule, BaseExportSolutionModule)
