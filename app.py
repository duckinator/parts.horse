#!/usr/bin/env python3

import cherrypy
from jinja2 import Environment, FileSystemLoader
import json
import os
from pathlib import Path

class Helpers:
    def link(value):
        if Helpers.is_html_response():
            return '<a href="{url}">{url}</a>'.format(url=value)
        else:
            return '<{url}>'.format(url=value)

    def environment():
        env = Environment(loader=FileSystemLoader('templates'))

        env.filters['link'] = Helpers.link
        env.filters['ljust'] = lambda value, *args: value.ljust(*args)
        env.filters['rjust'] = lambda value, *args: value.rjust(*args)

        return env

    def site_dict():
        site = {}
        port = cherrypy.config.get('server.socket_port')
        url = os.environ.get('SITE_URL', 'http://{}'.format(cherrypy.request.headers['Host']))

        site['name'] = os.environ.get('SITE_NAME') or 'Parts Horse'
        site['url']  = url

        return site

    def page_dict(part_name):
        data_file = Path('content/parts').joinpath(part_name.replace('/', '-') + '.json')
        site = Helpers.site_dict()
        page = json.loads(data_file.read_text())

        page['datasheet_redirect_target'] = page['datasheet']
        page['datasheet'] = site['url'] + '/ds/' + page['name']
        page['is_html'] = Helpers.is_html_response()

        return page

    def is_html_response():
        return ('text/html' in cherrypy.request.headers['Accept'].split(','))

    def response_type():
        if Helpers.is_html_response():
            return 'text/html'
        else:
            return 'text/plain'


class PartHomePage(object):
    @cherrypy.expose
    def index(self):
        return 'awoo'


class PartDirectory(object):
    def __init__(self):
        self.env = Helpers.environment()
        self.template = self.env.get_template('part.html')

    def _cp_dispatch(self, vpath):
        if len(vpath) == 1:
            cherrypy.request.params['part_name'] = vpath.pop()
            return self
        return vpath

    def get_parent_template(self):
        if Helpers.is_html_response():
            return 'base.html'
        else:
            return 'base.txt'

    @cherrypy.expose
    def index(self, part_name):
        part_name = part_name.lower()

        site = Helpers.site_dict()
        page = Helpers.page_dict(part_name)

        cherrypy.response.headers['Link'] = '</application.css>;rel=stylesheet'
        cherrypy.response.headers['Content-Type'] = Helpers.response_type() + '; charset=utf-8'

        return self.template.render(
                site=site,
                page=page,
                parent_template=self.get_parent_template(),
        )


class DatasheetRedirects(object):
    def _cp_dispatch(self, vpath):
        if len(vpath) == 1:
            cherrypy.request.params['part_name'] = vpath.pop()
            return self
        return vpath

    @cherrypy.expose
    def index(self, part_name):
        page = Helpers.page_dict(part_name)
        cherrypy.response.headers['Location'] = page['datasheet_redirect_target']
        cherrypy.response.status = 302
        return page['datasheet_redirect_target']


class PartSearch(object):
    pass


if __name__ == '__main__':
    site_dir = str(Path(__file__).resolve().parent)

    home_config = {
            '/': {
                'tools.staticdir.root': site_dir,
                'tools.staticdir.on': True,
                'tools.staticdir.dir': 'assets',
                }
            }

    search_config = {
            }

    cherrypy.tree.mount(PartHomePage(),  '/',       home_config)
    cherrypy.tree.mount(PartDirectory(), '/parts')
    cherrypy.tree.mount(PartSearch(),    '/search', search_config)
    cherrypy.tree.mount(DatasheetRedirects(),   '/datasheets')
    cherrypy.tree.mount(DatasheetRedirects(),   '/ds')

    cherrypy.config.update({'server.socket_port': int(os.environ.get('PORT', 5000))})

    cherrypy.engine.start()
    cherrypy.engine.block()
