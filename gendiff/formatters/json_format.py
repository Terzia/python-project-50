import json


def json_format(diff):
    """ Outputs difference between two files in json format"""
    return json.dumps(diff, indent=2)
