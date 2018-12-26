from .base import *
import collections
from pathlib import Path
import random

class PartSearch(PartsHorseBase):
    recent_queries = collections.deque(maxlen=30)
    def add_recent(query):
        if not query.lower() in map(str.lower, PartSearch.recent_queries):
            PartSearch.recent_queries.append(query)

    def recent():
        r = PartSearch.recent_queries
        return random.sample(r, min(10, len(r)))

    def __init__(self):
        super().__init__()
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
        data = self.part_dict(part)
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
        results = map(lambda r: self.part_dict(r[0], {'relevance': r}), results)
        return sorted(results, key=lambda x: x['relevance'])

    @cherrypy.expose
    def index(self, q=''):
        if q:
            results = self.search(q, min_relevance=1)
        else:
            results = []

        if len(results) > 0:
            PartSearch.add_recent(q)

        page = self.page_dict({
            'query': q,
            'results': results,
        })

        if self.is_html_response():
            template = self.html_template
        else:
            template = self.text_template

        return self.render(template, page)
