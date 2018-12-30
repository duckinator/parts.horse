import cherrypy
from jinja2 import Environment, FileSystemLoader
import json
import os
from pathlib import Path

from .helpers import Helpers
from .part import Part

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

    def fixme_please_i_am_a_gross_hack(self):
        self.env.globals['response']['is_html'] = Helpers.is_html_response()
        self.env.globals['site']['url'] = Helpers.get_site_url()

    def part_dict(self, part_name, extra={}):
        self.fixme_please_i_am_a_gross_hack()
        return Part(part_name).to_dict(Helpers.get_site_url(), extra)

    def render(self, page={}):
        self.fixme_please_i_am_a_gross_hack()

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
