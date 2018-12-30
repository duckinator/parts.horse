import cherrypy
from jinja2 import Environment, FileSystemLoader
import json
import os
from pathlib import Path

from .helpers import Helpers
from .parts import Parts

@cherrypy.tools.register('on_start_resource')
def response_env():
    headers = cherrypy.response.headers
    config = cherrypy.request.config

    is_html = Helpers.is_html_response()

    if is_html:
        response_type = 'text/html'
    else:
        response_type = 'text/plain'

    headers['Content-Type'] = response_type + '; charset=utf-8'
    config['globals'] = {
            'response': {'is_html': is_html}
    }

class PartsHorseBase(object):
    def __init__(self):
        env = Environment(loader=FileSystemLoader('templates'))
        env.filters['ljust'] = lambda value, *args: value.ljust(*args)
        env.filters['rjust'] = lambda value, *args: value.rjust(*args)
        self.env = env

        classname = self.__class__.__name__.lower()

        html_template = self._get_template_by_name(classname, 'html', alt=None)
        text_template = self._get_template_by_name(classname, 'txt', alt=html_template)

        self.templates = {
                'text/html': html_template,
                'text/plain': text_template,
                }

    def part_dict(self, part_name, extra={}):
        return Parts.get(part_name).to_dict(Helpers.get_site_url(), extra)

    def render(self, page={}):
        config = cherrypy.request.config
        content_type = cherrypy.response.headers['Content-Type'].split(';')[0].lower()
        return self.templates[content_type].render(page=page, **config['globals'])

    def _get_template_by_name(self, name, fmt, alt=None):
        template_name = '{}.{}'.format(name, fmt)

        if Path('templates/{}'.format(template_name)).exists():
            return self.env.get_template(template_name)
        else:
            return alt
