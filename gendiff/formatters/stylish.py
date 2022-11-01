import itertools


INDENT = '  '

PREFIX = {
    'added': '+ ',
    'deleted': '- ',
    'unchanged': '  ',
    'new': '+ ',
    'old': '- ',
    'nested': '  '
}


def get_json_str(value, start=1):
    """ Convert values to json strings."""
    if isinstance(value, bool):
        return str(value).lower()
    if value is None:
        return 'null'
    if isinstance(value, dict):
        return format_dict(value, start)
    return str(value)


def format_dict(dictionary, start):
    """Convert dictionary as value to output string with indentation
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


def convert_node(name, value, type, depth):
    """Convert node with value to output string, 'stylish' format"""
    indent = INDENT * depth
    return f'{indent}{PREFIX[type]}{name}: ' \
           f'{get_json_str(value, depth + 1)}'


def stylish(diff):
    """Convert difference between two json objects into
    'stylish' output format.
    """

    def inner(diff, counter):
        depth = counter + 1
        string = []
        for node in diff:
            type = node.get('type')
            name = node.get("name")
            value = node.get("value")
            if type == 'changed':
                old_value = get_json_str(value['old'], depth + 1)
                new_value = get_json_str(value['new'], depth + 1)
                string.append(convert_node(name, old_value, 'old', depth))
                string.append(convert_node(name, new_value, 'new', depth))
            elif type == 'nested':
                nested_value = inner(node.get("children"), depth + 1)
                string.append(convert_node(name, nested_value, type, depth))
            else:
                string.append(convert_node(name, value, type, depth))
        result = itertools.chain("{", string, ['  ' * counter + "}"])
        return '\n'.join(result)

    return inner(diff, 0)
