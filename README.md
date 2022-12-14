# ***A Difference Calculator***
This is CLI-utility that determines the difference between two data structures.
Utility features:
+ supports different input formats: yaml, json
+ generates the report with various formatting: plain text, stylish or json

It's also a library which provides 'gendiff' python module with 'generate_diff' function. 
This function returns a string of chosen format with the difference between two objects.
### Output formats examples:
+ #### stylish:
```
{
    common: {
      + follow: false
        setting1: Value 1
      - setting2: 200
      - setting3: true
      + setting3: null
      + setting4: blah blah
      + setting5: {
            key5: value5
        }
```
+ #### plain:
```
Property 'common.follow' was added with value: false
Property 'common.setting2' was removed
Property 'common.setting3' was updated. From true to null
```
+ #### json:
```
{
    "name": "common",
    "type": "nested",
    "children": [
      {
        "name": "follow",
        "type": "added",
        "value": false
      }
```
### Requirements:
- python = "^3.8"
- pytest-cov = "^3.0.0"
- PyYAML = "^6.0"
### Installation:
Open a command-line prompt

Run the following command:
```
$ make install
```

### Hexlet tests and linter type:
[![Actions type](https://github.com/Terzia/python-project-50/workflows/hexlet-check/badge.svg)](https://github.com/Terzia/python-project-50/actions)
[![Linter and pytest](https://github.com/Terzia/python-project-50/actions/workflows/Check.yml/badge.svg "Linter and pytest")](https://github.com/Terzia/python-project-50/actions/workflows/Check.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/f2e6772428d191c6fcf1/maintainability)](https://codeclimate.com/github/Terzia/python-project-50/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/f2e6772428d191c6fcf1/test_coverage)](https://codeclimate.com/github/Terzia/python-project-50/test_coverage)
<br/>

### Installation process and run with different formats of output:
[![asciicast](https://asciinema.org/a/HN6hG3yL4riHVCeSiTv2g7sid.svg)](https://asciinema.org/a/HN6hG3yL4riHVCeSiTv2g7sid)

[![asciicast](https://asciinema.org/a/jCZtKl6pVOibWgJg1sqj216ID.svg)](https://asciinema.org/a/jCZtKl6pVOibWgJg1sqj216ID)

[![asciicast](https://asciinema.org/a/ZpT8uNb1TQRm3W3Ejwbenh4Sn.svg)](https://asciinema.org/a/ZpT8uNb1TQRm3W3Ejwbenh4Sn)

[![asciicast](https://asciinema.org/a/jWykAHaVV8cauhq5Y1iFBHSE1.svg)](https://asciinema.org/a/jWykAHaVV8cauhq5Y1iFBHSE1)

[![asciicast](https://asciinema.org/a/kOwtrOiIiHWyQJWD5ER7L6ABU.svg)](https://asciinema.org/a/kOwtrOiIiHWyQJWD5ER7L6ABU)
