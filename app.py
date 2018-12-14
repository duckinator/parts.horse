#!/usr/bin/env python3

import cherrypy
from jinja2 import Environment, FileSystemLoader
import os
from pathlib import Path

class Helpers:
    def environment():
        env = Environment(loader=FileSystemLoader('templates'))

        # Add all of the functions defined in Filters to the environment.
        filters = Filters.__dict__
        for key in filters.keys():
            if callable(filters[key]):
                env.filters[key] = filters[key]

        return env

    def is_html_response():
        return ('text/html' in cherrypy.request.headers['Accept'].split(','))

    def response_type():
        if is_html_response():
            return 'text/html'
        else:
            return 'text/plain'

class Filters:
    def link(value):
        if Helpers.is_html_response():
            return '<a href="{url}">{url}</a>'.format(url=value)
        else:
            return '<{url}>'.format(url=value)

    def ljust(value, pad_size, padding=' '):
        return value.ljust(pad_size, padding)

    def rjust(value, pad_size, padding=' '):
        return value.rjust(pad_size, padding)

class PartHomePage(object):
    @cherrypy.expose
    def index(self):
        return 'awoo'

class PartDirectory(object):
    #@cherrypy.tools.accept(media='text/plain')
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
        data = []

        site = {
                "name": "Parts Horse",
                "url": "<TODO: DETERMINE BASE URL>",
                }
        page = {}

        return self.template.render(
                site=site,
                page=page,
                parent_template=self.get_parent_template(),
        )

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

    directory_config = {
            }

    search_config = {
            }

    cherrypy.tree.mount(PartHomePage(),  '/',       home_config)
    cherrypy.tree.mount(PartDirectory(), '/parts',  directory_config)
    cherrypy.tree.mount(PartSearch(),    '/search', search_config)

    cherrypy.config.update({'server.socket_port': int(os.environ.get('PORT', 5000))})

    cherrypy.engine.start()
    cherrypy.engine.block()
