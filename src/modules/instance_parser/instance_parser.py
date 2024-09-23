from typing import TextIO

from src.models.instance_data import InstanceData
from src.modules.instance_parser.base import BaseInstanceParserModule


class InstanceParserModuleException(Exception):
    pass


class InstanceParserModule(BaseInstanceParserModule):
    """
    Implementation of the BaseInstanceParserModule class
    """

    @staticmethod
    def check_line_is_comment(line: str) -> bool:
        return line.startswith('//')

    @staticmethod
    def check_line_is_whitespace(line: str) -> bool:
        return line.strip() == ''

    @staticmethod
    def check_string_is_int(string: str) -> bool:
        try:
            int(string)
            return True
        except ValueError:
            return False

    def read_int(self, line: str) -> int:
        if not self.check_string_is_int(line):
            raise InstanceParserModuleException(f'Expected "{line}" to be an integer')

        return int(line)

    def get_next_line(self, file: TextIO):
        line = file.readline()
        while line:
            if self.check_line_is_comment(line) or self.check_line_is_whitespace(line):
                line = file.readline()

        raise InstanceParserModuleException(f'No more lines')

    def run(self) -> InstanceData:
        with open(self.instance_filepath, 'r') as f:
            self.get_next_line(f)

        return InstanceData()
