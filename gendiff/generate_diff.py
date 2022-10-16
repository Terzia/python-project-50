import json

import yaml

from gendiff.formatters.stylish import stylish


def get_dictionary(file_path):
    '''Parses json or yaml files to dictionary'''
    with open(file_path, 'r') as file:
        if 'json' in file_path:
            return json.load(file)
        return yaml.safe_load(file)


def gen_diff(data1, data2):
    '''Generates tree of difference between two dicts into list of
    dictionaries, where items describe every key in original data,
    with name, status: added, deleted, unchanged, changed or nested,
    and value, or 'children' in case if both of changed values are
    dictionaries. 'Children' is the same list of dictionaries.
    For changed values in another case, function generates list, where
    first item is value in 1st data.'''
    keys = list(data1.keys() | data2.keys())
    keys.sort()
    result = []
    for key in keys:
        dictionary = {}
        dictionary['name'] = key
        if key not in data1:
            dictionary['status'] = 'added'
            dictionary['value'] = data2.get(key)
            result.append(dictionary)
        elif key not in data2:
            dictionary['status'] = 'deleted'
            dictionary['value'] = data1.get(key)
            result.append(dictionary)
        elif data1.get(key) == data2.get(key):
            dictionary['status'] = 'unchanged'
            dictionary['value'] = data2.get(key)
            result.append(dictionary)
        elif data1.get(key) != data2.get(key) and \
                isinstance(data1.get(key), dict) and \
                isinstance(data2.get(key), dict):
            dictionary['status'] = 'nested'
            dictionary['children'] = gen_diff(data1[key], data2[key])
            result.append(dictionary)
        else:
            dictionary['status'] = 'changed'
            dictionary['value'] = [
                data1.get(key),
                data2.get(key)
            ]
            result.append(dictionary)
    return result


def generate_diff(file_path1, file_path2, formatter=stylish):
    '''Generates tree of difference between two json or yaml files
    and converts it to string with given format of output.'''
    dict1 = get_dictionary(file_path1)
    dict2 = get_dictionary(file_path2)
    diff = gen_diff(dict1, dict2)
    return formatter(diff)
