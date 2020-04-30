#!/usr/bin/env python3

from elasticsearch import Elasticsearch
import json
import cherrypy
from lib.model.part import Part
from lib.render import PHRender


class Search:
    def __init__(self):
        self.phrender = PHRender()

        self.env = self.phrender.env
        self.template = self.phrender.get_class_template(self.__class__)

        self.es = Elasticsearch()

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
    def _es_score(result):
        return result['_score']

    def _search(self, query, start=None):
        start = start or 0
        es_results = self.es.search(index="parts", body={
            "query": {
                "simple_query_string": {
                    "all_fields": True,
                    "query": query,
                }
            },
            "timeout": "500ms",
            "from": start,
        })
        hits = es_results['hits']
        if es_results['timed_out']:
            print(f"!!! Query timed out: {query}")

        if hits['total']['relation'] == 'gte':
            prefix = 'about '
        else:
            prefix = ''
        summary = f"Found {prefix}{hits['total']['value']} results."
        timing = f"Search took approximately {es_results['took']}ms."

        results = [Part.get_dict(r['_id']) for r in sorted(hits['hits'], key=self._es_score)]
        return (summary, timing, results)

    @cherrypy.expose
    def search(self, q='', start=None):
        if q:
            summary, timing, results = self._search(q, start)
        else:
            summary = ''
            timing = ''
            results = []

        page = {
            'query': q,
            'summary': summary,
            'timing': timing,
            'results': results,
        }

        return self.render(page)


if __name__ == '__main__':
    cherrypy.quickstart(Search(), '/', config='config/server.conf')
else:
    wsgi = cherrypy.Application(Search(), '/', config='config/server.conf')
