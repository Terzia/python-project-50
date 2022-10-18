import os

import pytest

from gendiff.formatters.plain import plain

from gendiff.generate_diff import generate_diff

from gendiff.formatters.json_format import json_format as json


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

#Expected output
plain_data = read(get_abs_fixture_path('plain.txt')).rstrip().split('\n\n\n')
nested_data = read(get_abs_fixture_path('nested.txt')).rstrip().split('\n\n\n')


def test_abs_path():
    """Tests working with absolute paths and plain json files."""
    path1 = get_abs_fixture_path('file1.json')
    path2 = get_abs_fixture_path('file2.json')
    assert generate_diff(path1, path2) == plain_data[0]


plain_paths = [
    (get_rel_fixture_path('file1.json'),
     get_rel_fixture_path('file2.json')),
    (get_abs_fixture_path('file1.yaml'),
     get_abs_fixture_path('file2.yaml'))
]

nest_paths = [
    (get_rel_fixture_path('nest_file1.json'),
     get_rel_fixture_path('nest_file2.json')),
    (get_abs_fixture_path('nest_file1.yaml'),
     get_abs_fixture_path('nest_file2.yaml'))
]


@pytest.mark.parametrize("path1, path2", plain_paths)
def test_rel_path(path1, path2):
    """Tests working with plain files, stylish output format."""
    assert generate_diff(path1, path2) == plain_data[0]


@pytest.mark.parametrize("path1, path2", nest_paths)
def test_nested_stylish(path1, path2):
    """Tests working with nested files, stylish output format."""
    assert generate_diff(path1, path2) == nested_data[0]


@pytest.mark.parametrize("path1, path2", nest_paths)
def test_plain_output(path1, path2):
    """Tests working with nested files, plain output format."""
    assert generate_diff(path1, path2, plain) == nested_data[1]


@pytest.mark.parametrize("path1, path2", nest_paths)
def test_plain_output(path1, path2):
    """Tests working with nested files, json output format."""
    assert generate_diff(path1, path2, json) == nested_data[2]
