def convert_to_json(value):
    """Converts values to json format for output"""
    if isinstance(value, dict):
        return '[complex value]'
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, int):
        return value
    if value is None:
        return 'null'
    return f"'{value}'"


def plain(diff, path=''):
    """Converts difference between two files into plain output format"""
    string = []
    for node in diff:
        name = f"{path}{node['name']}"
        if node.get('type') == 'added':
            string.append(f"Property '{name}' "
                          f"was added with value: "
                          f"{convert_to_json(node.get('value'))}")
        if node.get('type') == 'deleted':
            string.append(f"Property '{name}' was removed")
        if node.get('type') == 'changed':
            old_value = convert_to_json(node.get('value')['old'])
            new_value = convert_to_json(node.get('value')['new'])
            string.append(f"Property '{name}' was updated. "
                          f"From {old_value} "
                          f"to {new_value}")
        if node.get('type') == 'nested':
            string.append(plain(node.get('children'), f'{name}.'))
    return '\n'.join(string)
