from lib import helpers
import json
from pathlib import Path

class Part(object):
    _all = None
    def all():
        if Part._all is None:
            Part._all = sorted(list(map(Part.get_dict, Part.names())), key=Part.id)
        return Part._all

    def names():
        parts_files = Path('parts').glob('**/*.json')
        return list(map(lambda path: path.name.replace('.json', ''), parts_files))

    def id(part_dict):
        return part_dict['id']

    def get(name):
        return Part(name)

    def get_dict(name, extra={}):
        return Part(name).to_dict(extra)


    def __init__(self, part_name):
        self.part_name = part_name.replace('/', '-').lower()
        self.file = Path('parts').joinpath(self.part_name + '.json')

        try:
            self.data = json.loads(self.file.read_text())
        except json.decoder.JSONDecodeError:
            print("[ERROR] Invalid JSON file: {}.".format(data_file))
            raise

    def to_dict(self, extra={}):
        site_url = helpers.get_site_url()
        page = {}

        for key in self.data.keys():
            page[key] = self.data[key]

        page['id'] = self.part_name
        page['datasheet_redirect_target'] = page['datasheet']
        page['datasheet'] = site_url + '/ds/' + self.part_name
        page['url_path'] = '/parts/' + self.part_name
        page['json_path'] = '/json/' + self.part_name
        page['canonical_url'] = site_url + page['url_path']
        page['canonical_json_url'] = site_url + page['json_path']

        for k in extra.keys():
            page[k] = extra[k]

        return page

