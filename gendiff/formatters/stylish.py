import itertools


INDENT = '  '


def get_json_str(value, start=1):
    """ Converts values to json strings."""
    if isinstance(value, bool):
        return str(value).lower()
    if value is None:
        return 'null'
    if isinstance(value, dict):
        return format_dict(value, start)
    return str(value)


def format_dict(dictionary, start):
    """Converts dictionary to output string with indentation
    based on nesting depth.
    """
    depth = start + 1
    curr_indent = INDENT * depth
    string = []
    for key, value in dictionary.items():
        string.append(f'{curr_indent}  {key}: '
                      f'{get_json_str(value, depth + 1)}')
    result = itertools.chain("{", string, [INDENT * start + "}"])
    return '\n'.join(result)


def stylish(diff):
    """Converts difference between two json objects into
    'stylish' output format.
    """

    def inner(diff, counter):
        depth = counter + 1
        indent = INDENT * depth
        string = []
        for node in diff:
            type = node.get('type')
            name = node.get("name")
            value = node.get("value")
            if type == 'added':
                string.append(f'{indent}+ {name}: '
                              f'{get_json_str(value, depth + 1)}')
            if type == 'deleted':
                string.append(f'{indent}- {name}: '
                              f'{get_json_str(value, depth + 1)}')
            if type == 'unchanged':
                string.append(f'{indent}  {name}: '
                              f'{get_json_str(value, depth + 1)}')
            if type == 'changed':
                old_value = get_json_str(value['old'], depth + 1)
                new_value = get_json_str(value['new'], depth + 1)
                string.append(f'{indent}- {name}: {old_value}\n'
                              f'{indent}+ {name}: {new_value}')
            if type == 'nested':
                string.append(f'{indent}  {name}: '
                              f'{inner(node.get("children"), depth + 1)}')
        result = itertools.chain("{", string, ['  ' * counter + "}"])
        return '\n'.join(result)

    return inner(diff, 0)
