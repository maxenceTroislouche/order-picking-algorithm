import unittest
from pathlib import Path

from src.modules.instance_parser.instance_parser import InstanceParserModule, InstanceParserModuleException


class TestInstanceParser(unittest.TestCase):
    def test_check_line_is_comment(self):
        instance_parser = InstanceParserModule(Path(''))
        self.assertTrue(instance_parser.check_line_is_comment('// commentaire de test'))
        self.assertFalse(instance_parser.check_line_is_comment('123'))

    def test_check_line_is_whitespace(self):
        instance_parser = InstanceParserModule(Path(''))
        self.assertTrue(instance_parser.check_line_is_whitespace('      '))
        self.assertTrue(instance_parser.check_line_is_whitespace(''))
        self.assertFalse(instance_parser.check_line_is_whitespace(' coucou'))

    def test_check_string_is_int(self):
        instance_parser = InstanceParserModule(Path(''))
        self.assertTrue(instance_parser.check_string_is_int('123'))
        self.assertFalse(instance_parser.check_string_is_int('salut'))

    def test_read_int(self):
        instance_parser = InstanceParserModule(Path(''))
        self.assertTrue(instance_parser.read_int('123'))
        self.assertRaises(InstanceParserModuleException, lambda: instance_parser.read_int('Not a number'))

    def test_get_next_line(self):
        pass

    def test_instance_parser(self):
        instance_filepath = Path("./instance.txt")
        instance_data = InstanceParserModule(instance_filepath)
