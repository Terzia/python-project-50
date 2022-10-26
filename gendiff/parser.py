import json

import yaml

import os


def get_format(path):
    ext = os.path.splitext(path)[1]
    return ext.lstrip('.')


def parse(data, format):
    """Parses json or yaml to dictionary"""
    if format == 'json':
        return json.loads(data)
    elif format in ('yaml', 'yml'):
        return yaml.safe_load(data)
    else:
        print('Unsupported file format')
        exit(0)
