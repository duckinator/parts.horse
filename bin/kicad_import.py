#!/usr/bin/env python3

"""A script to import part information from KiCad."""

from pathlib import Path
import json
import re

# We don't want a bunch of `fixme` warnings for this script.
# pylint: disable=fixme


def parse_part(part):
    """Converts KiCad's string representation of a part to a dict."""

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
    """Checks if a package style guess is a known package style."""

    # Try to catch as many as possible, but prefer missing a few over
    # having false matches.

    candidate = candidate.strip()

    if re.match(r'^(SM)?DIP\d+([A-Z]+)?$', candidate):
        candidate = candidate.replace('DIP', 'DIP-')

    # DO-<number> or DO-<number><letters>
    do_pkg = re.match(r'^DO-\d+([A-Z]+)?$', candidate)
    # DFN-<number>
    dfn = re.match(r'^DFN-\d+$', candidate)
    # DIP-<number>, SMDIP-<number>, or PDIP-<number>
    dip = re.match(r'^(SM|P)?DIP-\d+([A-Z]+)?$', candidate)
    sod = re.match(r'^SOD-\d+$', candidate)
    soic = re.match(r'^SOIC-\d+([A-Z]+)?$', candidate)
    # SSOP-<number>, MSOP-<number>, TSSOP-<number>
    sop = re.match(r'^(S|M|TS)SOP-\d+$', candidate)
    # TO-<number>
    to_pkg = re.match(r'^TO-\d+$', candidate)

    # If it's MELF(X), check that X is a valid packaging style.
    # For e.g. "MELF(DO-213AA)"
    if candidate.startswith('MELF(') and candidate.endswith(')'):
        return is_package_style(candidate.split('MELF(')[1][0:-2])

    # For e.g. "DIP-8/SOIC-8/TSSOP-8/DFN-8".
    if '/' in candidate and all(map(is_package_style, candidate.split('/'))):
        return True

    return do_pkg or dfn or dip or sod or soic or sop or to_pkg


def pin_count_from_package(package):
    """If the package style contain a number, that's usually the pin count."""

    if '-' not in package:
        return -1

    candidate = package.split('-')[-1]

    if not re.match(r'^\d+[A-Z]*$', candidate):
        return -1

    candidate = re.sub(r'[A-Z]', '', candidate)

    return int(candidate)


def normalize_summary(_part, summary):
    """Normalizes a part summary to avoid weird capitalization,
    single-word summaries, etc."""

    # Hack to work around the multiple descriptions of just 'Monostable',
    # 'Retriggerable monostable', 'Dual retriggerable Monostable', etc.
    summary = summary.replace('Monostable', 'monostable')

    if summary.endswith('monostable'):
        summary += ' multivibrator'

    if summary.startswith('monostable'):
        summary = 'M' + summary[1:]

    return summary


def normalize_package_style(package_style):
    """Normalizes the package style."""
    if '/' in package_style:
        parts = map(normalize_package_style, package_style.split('/'))
        print(list(parts))
        return '/'.join(parts)

    return '-'.join(package_style.split('-')[0:-1])


def try_save(part):
    """Generates a dict representing the part. If it is something we want
    and have enough information for, try to save it."""

    path = (Path('parts') / part['name'].lower()).with_suffix('.json')

    if path.exists():
        print('{} exists; skipping.'.format(path))
        return

    if part['desc'] and 'for simulation' in part['desc']:
        print('{} is for simulation only; skipping.'.format(part['name']))
        return

    print('Creating {}'.format(path))

    summary = part['desc']

    # This only happens a single time, so *shrug*
    summary = summary.replace('DIP-8, SO-8', 'DIP-8/SO-8')

    package_style = 'UNKNOWN'
    if summary and ', ' in summary:
        candidate = summary.split(', ')[-1]
        if is_package_style(candidate):
            print('  Package style: {}'.format(candidate))
            summary = ', '.join(summary.split(', ')[0:-1])
            package_style = candidate
        else:
            print('  Not package style: {}'.format(candidate))

    if package_style == 'UNKNOWN':
        print(' Unknown package style for {}'.format(part['name']))
        return

    number_of_pins = pin_count_from_package(package_style)
    summary = normalize_summary(part, summary)
    package_style = normalize_package_style(package_style)

    link = part['link']

    # There's a lot of these links without leading 'http://' or 'https://',
    # and these are confirmed to support https links.
    if link.startswith('www.allegromicro.com/') or \
        link.startswith('www.fairchildsemi.com/') or \
        link.startswith('www.st.com/') or \
        link.startswith('www.ti.com/') or \
        link.startswith('www.zilog.com/'):
        link = 'https://' + link

    if not link.startswith('http://') and not link.startswith('https://'):
        print('  Invalid link: {}'.format(link))
        return

    data = {
        'name': part['name'],
        'datasheet': link,
        'details': '', # FIXME
        'summary': summary,
        'style': package_style,
        'tags': part['tags'],
        'number_of_pins': number_of_pins,
        'pins': [], # FIXME
    }

    if ignored(data):
        print('  Ignored part: {}'.format(data['name']))
        return

    path.write_text(json.dumps(data, indent=2))


def ignored(part):
    """Determine if a part is ignored.

    A part being ignored does not mean it will never be added, it just means
    it's not _currently_ being added."""
    style = part['style']

    # Ignore any styles we don't support right now.
    known_styles = [
        # Dual-row.
        'DIP',
        'PDIP',
        'MSOP',
        'SO', 'SOIC', 'SOP',
        'SOT',
        'SSOP',
        'TDFN',
        'TSOP',
        'TSSOP',
        # Quad-row.
        'PLCC',
        'CLCC',
        'LQFP',
        'TQFP',
        'TQFN',
    ]
    # TO-3, TO-5, TO-18, etc.
    is_to = style.upper().split('-')[0] == 'TO'
    if is_to or not any(map(lambda x: x == style.upper(), known_styles)):
        return True

    return False


def handle(part_file):
    """Given a part file, extract individual part data, and try to save it."""
    data = part_file.read_text()
    parts = data.split('\n$ENDCMP\n')
    parts = filter(lambda x: x is not None, map(parse_part, parts))
    for part in parts:
        try_save(part)


def main():
    """Find every .dcm file in the local kicad library, and add part info."""
    # TODO: Clone the library repo and use that instead.

    library = Path('/usr/share/kicad/library')
    files = library.glob('*.dcm')
    for part_file in files:
        handle(part_file)


main()
