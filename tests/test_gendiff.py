import os

import pytest

from gendiff.generate_diff import generate_diff


def get_abs_fixture_path(file_name):
    '''Returns absolute path to file for comparing.'''
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'fixtures', file_name)


def get_rel_fixture_path(file_name):
    '''Returns relative path to file for comparing.'''
    current_dir = os.path.dirname(os.path.relpath(__file__))
    return os.path.join(current_dir, 'fixtures', file_name)


def read(file_path):
    '''Reads the file with expected output.'''
    with open(file_path, 'r') as file:
        result = file.read()
    return result

#Expected output
plain_data = read(get_abs_fixture_path('plain.txt'))


def test_abs_path():
    '''Tests working with absolute paths and plain json files.'''
    path1 = get_abs_fixture_path('file1.json')
    path2 = get_abs_fixture_path('file2.json')
    assert generate_diff(path1, path2) == read(get_abs_fixture_path('plain.txt'))


def test_rel_path():
    '''Tests working with relative paths and plain json files.'''
    path1 = get_rel_fixture_path('file1.json')
    path2 = get_rel_fixture_path('file2.json')
    assert generate_diff(path1, path2) == read(get_abs_fixture_path('plain.txt'))

def test_yaml():
    '''Tests working with plain yaml files.'''
    path1 = get_abs_fixture_path('file1.yaml')
    path2 = get_abs_fixture_path('file2.yaml')
    assert generate_diff(path1, path2) == read(get_abs_fixture_path('plain.txt'))