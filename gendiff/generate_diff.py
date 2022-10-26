from gendiff.formatters.stylish import stylish

from gendiff.formatters.plain import plain

from gendiff.formatters.json_format import json_format

from gendiff.parser import parse, get_format


def gen_diff(data1, data2):
    """Generate tree of difference between two dicts into list of
    dictionaries.

    List items describe every key in original data, with name,
    status (added, deleted, unchanged, changed or nested) and value,
    or 'children' in case if both of changed values are
    dictionaries. 'Children' is the list of dictionaries too.
    For changed values in another case, function generates key 'value'
    with nested dictionary as value, where 'old' key is value in 1st data,
    and 'new' key is value in 2nd.
    """
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
            dictionary['value'] = {
                'old': data1.get(key),
                'new': data2.get(key)
            }
            result.append(dictionary)
    return result


def read(path):
    with open(path, 'r') as file:
        result = file.read()
    return result


def format_output(diff, formatter):
    if formatter == 'stylish':
        return stylish(diff)
    if formatter == 'plain':
        return plain(diff)
    if formatter == 'json':
        return json_format(diff)


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
    diff = gen_diff(dict1, dict2)
    return format_output(diff, formatter)
