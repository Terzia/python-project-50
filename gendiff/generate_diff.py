from gendiff.parser import parse, get_format

from gendiff.build_tree import build_tree

from gendiff.formatters.choose_format import format_output


def read(path):
    with open(path, 'r') as file:
        result = file.read()
    return result


def generate_diff(file_path1, file_path2, formatter='stylish'):
    """Generate tree of difference between two json or yaml files
    and convert it to string.

    The result string is output in the given format:
    the default format is stylish, besides, plain and json format
    can be chosen.
    Positional arguments:
        file_path1 (str): absolute or relative path to the 1st compared file
        file_path2 (str): absolute or relative path to the 2nd compared file
    Optional keyword argument:
        formatter (str): format of output
            values: 'stylish' (default)
                    'plain'
                    'json'
    Returns:
        string in the given format
    """
    dict1 = parse(read(file_path1),
                  get_format(file_path1))
    dict2 = parse(read(file_path2),
                  get_format(file_path2))
    diff = build_tree(dict1, dict2)
    return format_output(diff, formatter)
