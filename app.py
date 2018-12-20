#!/usr/bin/env python3

import cherrypy
from jinja2 import Environment, FileSystemLoader

import collections
import json
import os
from pathlib import Path
import random

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

    def page_dict(part_name, extra={}):
        part_name = part_name.replace('/', '-').lower()
        data_file = Path('content/parts').joinpath(part_name + '.json')
        site = Helpers.site_dict()
        try:
            page = json.loads(data_file.read_text())
        except json.decoder.JSONDecodeError:
            print("[ERROR] Invalid JSON file: {}.".format(data_file))
            raise

        page['datasheet_redirect_target'] = page['datasheet']
        page['datasheet'] = site['url'] + '/ds/' + part_name
        page['is_html'] = Helpers.is_html_response()
        page['url_path'] = '/parts/' + part_name
        page['canonical_url'] = site['url'] + page['url_path']

        for k in extra.keys():
            page[k] = extra[k]

        return page

    def is_html_response():
        return ('text/html' in cherrypy.request.headers['Accept'].split(','))

    def response_type():
        if Helpers.is_html_response():
            return 'text/html'
        else:
            return 'text/plain'

    def get_parent_template():
        if Helpers.is_html_response():
            return 'base.html'
        else:
            return 'base.txt'

    def render(template, page):
        site = Helpers.site_dict()

        cherrypy.response.headers['Link'] = '</application.css>;rel=stylesheet'
        cherrypy.response.headers['Content-Type'] = Helpers.response_type() + '; charset=utf-8'

        return template.render(
                site=site,
                page=page,
                parent_template=Helpers.get_parent_template(),
        )


class PartHomePage(object):
    def __init__(self):
        self.env = Helpers.environment()
        self.template = self.env.get_template('home.html')

    @cherrypy.expose
    def index(self):
        return Helpers.render(self.template, {"recent": PartSearch.recent()})


class PartDirectory(object):
    def __init__(self):
        self.env = Helpers.environment()
        self.template = self.env.get_template('part.html')

    def _cp_dispatch(self, vpath):
        if len(vpath) == 1:
            cherrypy.request.params['part_name'] = vpath.pop()
            return self
        return vpath

    @cherrypy.expose
    def index(self, part_name):
        part = part_name.lower()
        page = Helpers.page_dict(part)
        return Helpers.render(self.template, page)


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
    recent_queries = collections.deque(maxlen=30)
    def add_recent(query):
        if not query in PartSearch.recent_queries:
            PartSearch.recent_queries.append(query)

    def recent():
        r = PartSearch.recent_queries
        return random.sample(r, min(10, len(r)))

    def __init__(self):
        self.env = Helpers.environment()
        self.html_template = self.env.get_template('search.html')
        self.text_template = self.env.get_template('search.txt')

        parts_files = Path('content/parts').glob('**/*.json')
        self.parts_list = list(map(self.path_to_name, parts_files))

    def path_to_name(self, path):
        return path.name.replace('.json', '')

    def chunk_relevance(self, data, chunk):
        chunk = chunk.lower()
        rs = [
                chunk in data['datasheet_redirect_target'].lower(),
                chunk in data['style'].lower(),
                chunk in data['summary'].lower(),
                chunk in map(lambda x: x.lower(), data['tags']),
                chunk in data['name'].lower(),
            ]

        return sum(rs)

    def relevance(self, part, query):
        data = Helpers.page_dict(part)
        # Remove empty strings, None, etc.
        chunks = filter(lambda x: x, query.split(' '))
        # Determine the relevance of each chunk.
        rs = map(lambda c: self.chunk_relevance(data, c), chunks)
        return sum(rs)

    def search(self, query, min_relevance=1):
        # Split by word, and remove empty strings, None, etc.
        chunks = filter(lambda x: x, query.split(' '))
        relevances = map(lambda p: [p, self.relevance(p, query)], self.parts_list)
        results = filter(lambda x: x[1] >= min_relevance, relevances)
        results = map(lambda r: Helpers.page_dict(r[0], {'relevance': r}), results)
        return sorted(results, key=lambda x: x['relevance'])

    @cherrypy.expose
    def index(self, q=''):
        if q:
            PartSearch.add_recent(q)
            results = self.search(q, min_relevance=1)
        else:
            results = []

        page = {
            'query': q,
            'results': results,
        }

        if Helpers.is_html_response():
            template = self.html_template
        else:
            template = self.text_template

        return Helpers.render(template, page)


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

    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': int(os.environ.get('PORT', 5000)),
    })

    cherrypy.engine.start()
    cherrypy.engine.block()
