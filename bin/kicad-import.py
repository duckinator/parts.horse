#!/usr/bin/env python3

from pathlib import Path
import json
import re


def parse_part(part):
    if not '\nF ' in part:
        return None

    lines = part.split('\n')
    name = None
    desc = ''
    tags = []
    link = ''
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
            tags = list(map(str.strip, rest.replace(' ', ',').split(',')))
        elif key == 'F':
            link = rest

    tags = list(filter(lambda x: str(x).strip(), tags))
    return {'name': name, 'desc': desc, 'tags': tags, 'link': link}


def is_package_style(candidate):
    # Try to catch as many as possible, but prefer missing a few over
    # having false matches.

    # DO-<number> or DO-<number>A<letters>
    if re.match('^DO-\d+(A[A-Z]+)?$', candidate):
        return True

    # DFN-<number>
    if re.match('^DFN-\d+$', candidate):
        return True

    # DIP-<number> or PDIP-<number>
    if re.match('^P?DIP-\d+$', candidate):
        return True

    if re.match('^SOD-\d+$', candidate):
        return True

    if re.match('^SOIC-\d+$', candidate):
        return True

    if re.match('^TO-\d+$', candidate):
        return True

    if re.match('^TSSOP-\d+$', candidate):
        return True

    # If it's MELF(X), check that X is a valid packaging style.
    # For e.g. "MELF(DO-213AA)"
    if candidate.startswith('MELF(') and candidate.endswith(')'):
        return is_package_style(candidate.split('MELF(')[1][0:-2])

    # For e.g. "DIP-8/SOIC-8/TSSOP-8/DFN-8".
    if '/' in candidate and all(map(is_package_style, candidate.split('/'))):
        return True

    return False


def pin_count_from_package(package):
    if '-' not in package:
        return -1

    candidate = package.split('-')[-1]

    if not re.match('^\d+$', candidate):
        return -1

    return int(candidate)


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

    summary = part['desc']
    package_style = 'UNKNOWN'
    if summary and ', ' in summary:
        candidate = summary.split(', ')[-1]
        if is_package_style(candidate):
            print('  Package style: {}'.format(candidate))
            summary = ', '.join(summary.split(', ')[0:-1])
            package_style = candidate
        else:
            print('  Not package style: {}'.format(candidate))

    number_of_pins = pin_count_from_package(package_style)

    data = {
        'name': part['name'],
        'datasheet': part['link'],
        'details': '', # FIXME
        'summary': summary,
        'style': package_style,
        'tags': part['tags'],
        'number_of_pins': number_of_pins,
        'pins': [], # FIXME
    }
    path.write_text(json.dumps(data, indent=2))


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
