from typing import Type


def check_line_is_comment(line: str) -> bool:
    return line.startswith('//')


def check_line_is_whitespace(line: str) -> bool:
    return line.strip() == ''


def check_string_is_int(string: str) -> bool:
    try:
        int(string)
    except ValueError:
        return False

    return True


def check_string_contains_n_ints(string: str, n: int) -> bool:
    split_string = string.split(' ')
    if '' in split_string:
        split_string.remove('')  # Remove empty strings

    if len(split_string) != n:  # Check if the number of elements is correct
        return False

    return all(check_string_is_int(s) for s in split_string)  # Check if all elements are integers


def get_int(string: str, exception: Type[Exception]) -> int:
    if not check_string_is_int(string):
        raise exception(f'Expected "{string}" to be an integer')

    return int(string)


def get_ints(string: str, exception: Type[Exception]) -> list[int]:
    split_string = string.split(' ')
    if '' in split_string:
        split_string.remove('')  # Remove empty strings

    return [get_int(s, exception) for s in split_string]


def get_n_ints(string: str, n: int, exception: Type[Exception]) -> list[int]:
    if not check_string_contains_n_ints(string, n):
        raise exception(f'Expected "{string}" to contain {n} integers')

    return get_ints(string, exception)
