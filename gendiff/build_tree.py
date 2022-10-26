def build_tree(data1, data2):
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
            dictionary['type'] = 'added'
            dictionary['value'] = data2.get(key)
            result.append(dictionary)
        elif key not in data2:
            dictionary['type'] = 'deleted'
            dictionary['value'] = data1.get(key)
            result.append(dictionary)
        elif data1.get(key) == data2.get(key):
            dictionary['type'] = 'unchanged'
            dictionary['value'] = data2.get(key)
            result.append(dictionary)
        elif data1.get(key) != data2.get(key) and \
                isinstance(data1.get(key), dict) and \
                isinstance(data2.get(key), dict):
            dictionary['type'] = 'nested'
            dictionary['children'] = build_tree(data1[key], data2[key])
            result.append(dictionary)
        else:
            dictionary['type'] = 'changed'
            dictionary['value'] = {
                'old': data1.get(key),
                'new': data2.get(key)
            }
            result.append(dictionary)
    return result
