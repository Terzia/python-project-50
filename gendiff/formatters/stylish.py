import itertools


def convert_to_json(value):
    """Converts values to json format for output"""
    if isinstance(value, bool):
        return str(value).lower()
    if value is None:
        return 'null'
    return value


def get_str(dictionary, start, indent='  '):
    """Converts dictionary to output string with indentation
    based on nesting depth."""
    def inner(current_data, counter):
        if not isinstance(current_data, dict):
            return str(current_data)

        depth = counter + 1
        curr_indent = indent * depth
        string = []
        for key, value in current_data.items():
            string.append(f'{curr_indent}  {key}: '
                          f'{inner(convert_to_json(value), depth + 1)}')
        result = itertools.chain("{", string, [indent * counter + "}"])
        return '\n'.join(result)

    return inner(dictionary, start)


def stylish(diff, counter=0):
    """Converts difference between two files to output string with
    indentation, based on nesting depth."""
    string = []
    depth = counter + 1
    indent = '  ' * depth
    for node in diff:
        status = node.get('status')
        name = node.get("name")
        value = convert_to_json(node.get("value"))
        if status == 'added':
            string.append(f'{indent}+ {name}: '
                          f'{get_str(value, depth + 1)}')
        if status == 'deleted':
            string.append(f'{indent}- {name}: '
                          f'{get_str(value, depth + 1)}')
        if status == 'unchanged':
            string.append(f'{indent}  {name}: '
                          f'{get_str(value, depth + 1)}')
        if status == 'changed':
            old_value = convert_to_json(value['old'])
            new_value = convert_to_json(value['new'])
            string.append(f'{indent}- {name}: '
                          f'{get_str(old_value, depth + 1)}\n'
                          f'{indent}+ {name}: '
                          f'{get_str(new_value, depth + 1)}')
        if status == 'nested':
            string.append(f'{indent}  {name}: '
                          f'{stylish(node.get("children"), depth + 1)}')
    result = itertools.chain("{", string, ['  ' * counter + "}"])
    return '\n'.join(result)
