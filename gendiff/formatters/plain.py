def convert_to_json(value):
    if isinstance(value, dict):
        return '[complex value]'
    if isinstance(value, bool):
        return str(value).lower()
    if value is None:
        return 'null'
    if isinstance(value, int):
        return value
    return f"'{value}'"


def plain(diff, path=''):
    '''Converts difference between two files into plain format'''
    string = []
    for node in diff:
        name = f"{path}{node['name']}"
        if node.get('status') == 'added':
            string.append(f"Property {name} "
                          f"was added with value: "
                          f"{convert_to_json(node.get('value'))}")
        if node.get('status') == 'deleted':
            string.append(f"Property {name} was removed")
        if node.get('status') == 'changed':
            string.append(f"Property {name} "
                          f"was updated from "
                          f"{convert_to_json(node.get('value')[0])} "
                          f"to {convert_to_json(node.get('value')[1])}")
        if node.get('status') == 'nested':
            string.append(plain(node.get('children'), f'{name}.'))
    return '\n'.join(string)
