import json


def get_dictionary(file_path):
    with open(file_path, 'r') as file:
        dictionary = json.load(file)
        return dictionary


def convert_boolean(value):
    if isinstance(value, bool):
        return str(value).lower()
    return value


def generate_diff(file_path1, file_path2):
    data1 = get_dictionary(file_path1)
    data2 = get_dictionary(file_path2)
    key_set = data1.keys() | data2.keys()
    keys = sorted(list(key_set))
    result = '{'
    for key in keys:
        if key not in data1:
            result = f'{result}\n+ {key}: {convert_boolean(data2.get(key))}'
        elif key not in data2:
            result = f'{result}\n- {key}: {convert_boolean(data1.get(key))}'
        elif data1.get(key) == data2.get(key):
            result = f'{result}\n  {key}: {convert_boolean(data1.get(key))}'
        else:
            result = f'{result}\n' \
                     f'- {key}: {convert_boolean(data1.get(key))}\n' \
                     f'+ {key}: {convert_boolean(data2.get(key))}'
    return f"{result}\n}}"
