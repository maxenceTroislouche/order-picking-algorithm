import unittest

from src.utils.string import check_line_is_comment, check_line_is_whitespace, check_string_is_int, get_int, get_ints, \
    check_string_contains_n_ints, get_n_ints


class TestStringUtils(unittest.TestCase):
    def test_check_line_is_comment(self):
        self.assertTrue(check_line_is_comment('// commentaire'))
        self.assertFalse(check_line_is_comment('123'))

    def test_check_line_is_whitespace(self):
        self.assertTrue(check_line_is_whitespace('      '))
        self.assertFalse(check_line_is_whitespace(' coucou'))

    def test_check_string_is_int(self):
        self.assertTrue(check_string_is_int('123'))
        self.assertFalse(check_string_is_int('salut'))

    def test_check_string_contains_n_ints(self):
        self.assertTrue(check_string_contains_n_ints('1 2 3 4', 4))
        self.assertFalse(check_string_contains_n_ints('1 2 3 4', 3))
        self.assertFalse(check_string_contains_n_ints('1 2 3 salut', 4))

    def test_get_int(self):
        class TestGetIntException(Exception):
            pass

        self.assertEqual(get_int('123', TestGetIntException), 123)
        self.assertRaises(TestGetIntException, lambda: get_int('Not a number', TestGetIntException))

    def test_get_ints(self):
        class TestGetIntsException(Exception):
            pass

        self.assertEqual(get_ints('1 2 3 4', TestGetIntsException), [1, 2, 3, 4])
        self.assertRaises(TestGetIntsException, lambda: get_ints('1 2 3 salut', TestGetIntsException))

    def test_get_n_ints(self):
        class TestGetNIntsException(Exception):
            pass

        self.assertEqual(get_n_ints('1 2 3 4', 4, TestGetNIntsException), [1, 2, 3, 4])
        self.assertRaises(TestGetNIntsException, lambda: get_n_ints('1 2 3 4', 3, TestGetNIntsException))
        self.assertRaises(TestGetNIntsException, lambda: get_n_ints('1 2 3 salut', 4, TestGetNIntsException))
