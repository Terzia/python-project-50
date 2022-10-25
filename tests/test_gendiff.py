import os

import pytest

from gendiff.generate_diff import generate_diff


def get_abs_fixture_path(file_name):
    '''Returns absolute path to file for comparing.'''
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'fixtures', file_name)


def get_rel_fixture_path(file_name):
    """Returns relative path to file for comparing."""
    current_dir = os.path.dirname(os.path.relpath(__file__))
    return os.path.join(current_dir, 'fixtures', file_name)


def read(file_path):
    """Reads the file with expected output."""
    with open(file_path, 'r') as file:
        result = file.read()
    return result


# Expected output
plain_data = read(get_abs_fixture_path('plain.txt')).rstrip().split('\n\n\n')
nested_data = read(get_abs_fixture_path('nested.txt')).rstrip().split('\n\n\n')


# Relative paths
plain_yaml_path1 = get_rel_fixture_path('file1.yaml')
plain_yaml_path2 = get_rel_fixture_path('file2.yaml')
plain_json_path1 = get_rel_fixture_path('file1.json')
plain_json_path2 = get_rel_fixture_path('file2.json')
nest_yaml_path1 = get_rel_fixture_path('nest_file1.yaml')
nest_yaml_path2 = get_rel_fixture_path('nest_file2.yaml')
nest_json_path1 = get_rel_fixture_path('nest_file1.json')
nest_json_path2 = get_rel_fixture_path('nest_file2.json')


test_parameters = [
    ([plain_json_path1, plain_json_path2], {}, plain_data[0]),
    ([plain_yaml_path1, plain_yaml_path2], {}, plain_data[0]),
    ([nest_json_path1, nest_json_path2], {}, nested_data[0]),
    ([nest_yaml_path1, nest_yaml_path2], {}, nested_data[0]),
    ([plain_json_path1, plain_json_path2], {'format': 'plain'}, plain_data[1]),
    ([nest_json_path1, nest_json_path2], {'format': 'plain'}, nested_data[1]),
    ([nest_yaml_path1, nest_yaml_path2], {'format': 'plain'}, nested_data[1]),
    ([nest_json_path1, nest_json_path2], {'format': 'json'}, nested_data[2]),
    ([nest_yaml_path1, nest_yaml_path2], {'format': 'json'}, nested_data[2])
]


def test_abs_path():
    """Tests working with absolute paths."""
    path1 = get_abs_fixture_path('file1.json')
    path2 = get_abs_fixture_path('file2.json')
    assert generate_diff(path1, path2) == plain_data[0]


@pytest.mark.parametrize("args, kwargs, expected", test_parameters)
def test_various_format(args, kwargs, expected):
    """Tests working with plain and nested files, stylish, plain and json output format."""
    diff = generate_diff(*args, **kwargs)
    assert diff == expected
