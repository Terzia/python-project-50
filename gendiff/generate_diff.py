import json

import yaml

import itertools


def get_dictionary(file_path):
    '''Parses json or yaml files to dictionary'''
    with open(file_path, 'r') as file:
        if 'json' in file_path:
            return json.load(file)
        return yaml.safe_load(file)


def convert_to_json(value):
    '''Converts values to json format'''
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    return value


def get_str(dictionary, start, indent='  '):
    '''Converts dictionary to string'''

    def inner(current_data, counter):
        if not isinstance(current_data, dict):
            return str(current_data)

        depth = counter + 1
        curr_indent = indent * depth
        string = []
        for key, value in current_data.items():
            string.append(f'{curr_indent}  {key}: {inner(value, depth + 1)}')
        result = itertools.chain("{", string, [indent * counter + "}"])
        return '\n'.join(result)

    return inner(dictionary, start)


def stylish(diff, counter=0):
    '''Converts difference between two files to string'''
    string = []
    depth = counter + 1
    indent = '  ' * depth
    for item in diff:
        if item.get('status') == 'added':
            string.append(f'{indent}+ {item.get("name")}: '
                          f'{get_str(item.get("value"), depth + 1)}')
        if item.get('status') == 'deleted':
            string.append(f'{indent}- {item.get("name")}: '
                          f'{get_str(item.get("value"), depth + 1)}')
        if item.get('status') == 'unchanged':
            string.append(f'{indent}  {item.get("name")}: '
                          f'{get_str(item.get("value"), depth + 1)}')
        if item.get('status') == 'changed':
            string.append(f'{indent}- {item.get("name")}: '
                          f'{get_str(item.get("value")[0], depth + 1)}\n'
                          f'{indent}+ {item.get("name")}: '
                          f'{get_str(item.get("value")[1], depth + 1)}')
        if item.get('status') == 'nested':
            string.append(f'{indent}  {item.get("name")}: '
                          f'{stylish(item.get("children"), depth + 1)}')
    result = itertools.chain("{", string, ['  ' * counter + "}"])
    return '\n'.join(result)


def gen_diff(data1, data2):
    '''Generates tree of difference between two dicts into list of
    dictionaries, where items describe every key in original data,
    with name, status: added, deleted, changed or nested, and value, or
    'children' in case if both of changed values are dictionaries.
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
            dictionary['value'] = convert_to_json(data2.get(key))
            result.append(dictionary)
        elif key not in data2:
            dictionary['status'] = 'deleted'
            dictionary['value'] = convert_to_json(data1.get(key))
            result.append(dictionary)
        elif data1.get(key) == data2.get(key):
            dictionary['status'] = 'unchanged'
            dictionary['value'] = convert_to_json(data2.get(key))
            result.append(dictionary)
        elif data1.get(key) != data2.get(key) and\
                isinstance(data1.get(key), dict) and\
                isinstance(data2.get(key), dict):
            dictionary['status'] = 'nested'
            dictionary['children'] = gen_diff(data1[key], data2[key])
            result.append(dictionary)
        else:
            dictionary['status'] = 'changed'
            dictionary['value'] = [
                convert_to_json(data1.get(key)),
                convert_to_json(data2.get(key))
            ]
            result.append(dictionary)
    return result


def generate_diff(file_path1, file_path2, formatter=stylish):
    '''Generates tree of difference between two files and converts it to string
    with given format'''
    dict1 = get_dictionary(file_path1)
    dict2 = get_dictionary(file_path2)
    diff = gen_diff(dict1, dict2)
    return formatter(diff)
