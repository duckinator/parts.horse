import cherrypy
from jinja2 import Environment, FileSystemLoader
import json
import os
from pathlib import Path

class AppGlobals:
    def update_site(env):
        port = cherrypy.config.get('server.socket_port')
        socket_host = cherrypy.config.get('server.socket_host')
        host = cherrypy.request.headers.get('Host', socket_host)

        if port == 443:
            scheme = 'https'
        elif port == 80:
            scheme = 'http'
        else:
            scheme = 'http'
            if not host.endswith(':{}'.format(port)):
                host += ':{}'.format(port)

        default_url = '{}://{}'.format(scheme, host)

        env.globals['site']['url'] = os.environ.get('SITE_URL', default_url)

        return env.globals['site']


class PartsHorseBase(object):
    def __init__(self):
        env = Environment(loader=FileSystemLoader('templates'))
        env.globals['site'] = {}
        env.filters['ljust'] = lambda value, *args: value.ljust(*args)
        env.filters['rjust'] = lambda value, *args: value.rjust(*args)
        self.env = env

    def part_dict(self, part_name, extra={}):
        AppGlobals.update_site(self.env)

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

        return self.page_dict(page)

    def page_dict(self, extra={}):
        AppGlobals.update_site(self.env)

        site = self.env.globals['site']
        page = {}

        page['is_html'] = self.is_html_response()

        for k in extra.keys():
            page[k] = extra[k]

        return page

    def is_html_response(self):
        return ('text/html' in cherrypy.request.headers['Accept'].split(','))

    def response_type(self):
        if self.is_html_response():
            return 'text/html'
        else:
            return 'text/plain'

    def render(self, template, page):
        cherrypy.response.headers['Content-Type'] = self.response_type() + '; charset=utf-8'

        return template.render(page=page)

