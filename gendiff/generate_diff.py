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
    elif value == None:
        return 'null'
    elif value == ' ':
        return ''
    return value


def convert_dict(dictionary, indent, start):
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


def stylish(diff):
    '''Converts difference between two files to string'''

    def inner(diff, counter):
        string = []
        depth = counter + 1
        indent = '  ' * depth
        for item in diff:
            if item.get('status') == 'added':
                string.append(f'{indent}+ {item.get("name")}: '
                              f'{convert_dict(item.get("value"), "  ", depth + 1)}')
            if item.get('status') == 'deleted':
                string.append(f'{indent}- {item.get("name")}: '
                              f'{convert_dict(item.get("value"), "  ", depth + 1)}')
            if item.get('status') == 'unchanged':
                string.append(f'{indent}  {item.get("name")}: '
                              f'{convert_dict(item.get("value"), "  ", depth + 1)}')
            if item.get('status') == 'changed':
                if item.get('children'):
                    string.append(f'{indent}  {item.get("name")}: '
                                  f'{inner(item.get("children"), depth + 1)}')
                else:
                    string.append(f'{indent}- {item.get("name")}: '
                                  f'{convert_dict(item.get("value")[0], "  ", depth + 1)}\n'
                                  f'{indent}+ {item.get("name")}: '
                                  f'{convert_dict(item.get("value")[1], "  ", depth + 1)}')
        result = itertools.chain("{", string, ['  ' * counter + "}"])
        return '\n'.join(result)

    return inner(diff, 0)


def generate_diff(file_path1, file_path2, formater=stylish):
    '''Generates tree of difference between two files and converts it to string
    with formater'''
    dict1 = get_dictionary(file_path1)
    dict2 = get_dictionary(file_path2)
    def inner(data1, data2):
        keys = list(data1.keys() | data2.keys())
        keys.sort()
        result = []
        for key in keys:
            dictionary = {}
            if key not in data1:
                dictionary['name'] = key
                dictionary['status'] = 'added'
                dictionary['value'] = convert_to_json(data2.get(key))
                result.append(dictionary)
            elif key not in data2:
                dictionary['name'] = key
                dictionary['status'] = 'deleted'
                dictionary['value'] = convert_to_json(data1.get(key))
                result.append(dictionary)
            elif data1.get(key) == data2.get(key):
                dictionary['name'] = key
                dictionary['status'] = 'unchanged'
                dictionary['value'] = convert_to_json(data2.get(key))
                result.append(dictionary)
            else:
                dictionary['name'] = key
                dictionary['status'] = 'changed'
                if type(data1.get(key)) == dict and type(data2.get(key)) == dict:
                    dictionary['children'] = inner(data1.get(key), data2.get(key))
                else:
                    dictionary['value'] = [
                        convert_to_json(data1.get(key)),
                        convert_to_json(data2.get(key))
                    ]
                result.append(dictionary)
        return result

    return formater(inner(dict1, dict2))
