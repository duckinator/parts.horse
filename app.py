#!/usr/bin/env python3

import json
import cherrypy
from lib.model.part import Part
from lib.render import PHRender


class Search:
    def __init__(self):
        self.phrender = PHRender()

        self.env = self.phrender.env
        self.template = self.phrender.get_class_template(self.__class__)

    def render(self, page=None):
        """Render the template associated with the page.

        If the client requests JSON, then this returns a JSON dump of the
        """

        if page is None:
            page = {}

        headers = cherrypy.response.headers

        if self._is_json_response():
            headers['Content-Type'] = 'application/json; charset=utf-8'
            return json.dumps(page, indent=2, sort_keys=True).encode('utf-8')

        return self.template.render(page=page)

    @staticmethod
    def _is_json_response():
        headers = cherrypy.response.headers
        accepted = headers.get('Accept', '').split(',')
        return 'application/json' in accepted

    @staticmethod
    def chunk_relevance(data, chunk):
        chunk = chunk.lower()
        results = [
            chunk in data['datasheet_redirect_target'].lower(),
            chunk in data['style'].lower(),
            chunk in data['summary'].lower(),
            chunk in map(lambda x: x.lower(), data['tags']),
            chunk in data['name'].lower(),
        ]

        return sum(results)

    def relevance(self, part, query):
        data = Part.get_dict(part)
        # Remove empty strings, None, etc.
        chunks = filter(lambda x: x, query.split(' '))
        # Determine the relevance of each chunk.
        results = map(lambda c: self.chunk_relevance(data, c), chunks)
        return sum(results)

    def _search(self, query, min_relevance=1):
        # Split by word, and remove empty strings, None, etc.
        # FIXME: Why the hell was this variable unused?! #pylint: disable=fixme
        # chunks = filter(lambda x: x, query.split(' '))
        relevances = map(lambda p: [p, self.relevance(p, query)], Part.names())
        results_f = filter(lambda x: x[1] >= min_relevance, relevances)
        results = map(lambda r: Part.get_dict(r[0], {'relevance': r}), results_f)
        return sorted(results, key=lambda x: x['relevance'])

    @cherrypy.expose
    def search(self, q=''):
        if q:
            results = self._search(q, min_relevance=1)
        else:
            results = []

        page = {
            'query': q,
            'results': results,
        }

        return self.render(page)


if __name__ == '__main__':
    cherrypy.quickstart(Search(), '/', config='config/server.conf')
else:
    wsgi = cherrypy.Application(Search(), '/', config='config/server.conf')
