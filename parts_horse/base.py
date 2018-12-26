import cherrypy
from jinja2 import Environment, FileSystemLoader
import json
import os
from pathlib import Path

from .helpers import Helpers

class PartsHorseBase(object):
    def __init__(self):
        env = Environment(loader=FileSystemLoader('templates'))
        env.globals['site'] = {}
        env.globals['response'] = {}
        env.filters['ljust'] = lambda value, *args: value.ljust(*args)
        env.filters['rjust'] = lambda value, *args: value.rjust(*args)
        self.env = env

        classname = self.__class__.__name__.lower()

        self.html_template = self._get_template_by_name(classname, 'html', alt=None)
        self.text_template = self._get_template_by_name(classname, 'txt', alt=self.html_template)

    def fixme(self):
        self.env.globals['response']['is_html'] = Helpers.is_html_response()
        self.env.globals['site']['url'] = Helpers.get_site_url()

    def part_dict(self, part_name, extra={}):
        self.fixme()

        site = self.env.globals['site']
        part_name = part_name.replace('/', '-').lower()
        data_file = Path('content/parts').joinpath(part_name + '.json')

        try:
            page = json.loads(data_file.read_text())
        except json.decoder.JSONDecodeError:
            print("[ERROR] Invalid JSON file: {}.".format(data_file))
            raise

        page['datasheet_redirect_target'] = page['datasheet']
        page['datasheet'] = site['url'] + '/ds/' + part_name
        page['url_path'] = '/parts/' + part_name
        page['canonical_url'] = site['url'] + page['url_path']

        for k in extra.keys():
            page[k] = extra[k]

        return page

    def render(self, page):
        if Helpers.is_html_response():
            template = self.html_template
            response_type = 'text/html'
        else:
            template = self.text_template
            response_type = 'text/plain'

        cherrypy.response.headers['Content-Type'] = response_type + '; charset=utf-8'

        return template.render(page=page)

    def _get_template_by_name(self, name, fmt, alt=None):
        template_name = '{}.{}'.format(name, fmt)

        if Path('templates/{}'.format(template_name)).exists():
            return self.env.get_template(template_name)
        else:
            return alt
