from gendiff.formatters.stylish import stylish

from gendiff.formatters.plain import plain

from gendiff.formatters.json_format import json_format


def format_output(diff, formatter):
    if formatter == 'stylish':
        return stylish(diff)
    if formatter == 'plain':
        return plain(diff)
    if formatter == 'json':
        return json_format(diff)
