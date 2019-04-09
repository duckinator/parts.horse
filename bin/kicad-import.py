#!/usr/bin/env python3

from pathlib import Path
import json


def parse_part(part):
    if not '\nF ' in part:
        return None

    lines = part.split('\n')
    name = None
    desc = None
    tags = None
    link = None
    for line in lines:
        if not ' ' in line:
            continue
        key, rest = line.split(' ', 1)
        rest = rest.strip()
        if key == '$CMP':
            name = rest
        elif key == 'D':
            desc = rest
        elif key == 'K':
            tags = list(map(str.strip, rest.split(',')))
        elif key == 'F':
            link = rest
    return {'name': name, 'desc': desc, 'tags': tags, 'link': link}


def try_save(part):
    path = (Path('parts') / part['name'].lower()).with_suffix('.json')

    if path.exists():
        print('{} exists; skipping.'.format(path))
        return
    elif part['desc'] and 'for simulation' in part['desc']:
        print('{} is for simulation only; skipping.'.format(part['name']))
        return
    else:
        print('Creating {}'.format(path))

    data = {
        'name': part['name'],
        'datasheet': part['link'],
        'details': '', # FIXME
        'summary': part['desc'],
        'style': 'UNKNOWN', # FIXME
        'tags': part['tags'],
        'number_of_pins': 0, # FIXME
        'pins': [], # FIXME
    }
    path.write_text(json.dumps(data))


def handle(part_file):
    data = part_file.read_text()
    parts = data.split('\n$ENDCMP\n')
    parts = filter(lambda x: x is not None, map(parse_part, parts))
    for part in parts:
        try_save(part)


def main():
    library = Path('/usr/share/kicad/library')
    files = library.glob('*.dcm')
    for part_file in files:
        handle(part_file)


main()
