#!/usr/bin/env python3

import os

from elasticsearch import Elasticsearch
from quart import Quart, request, render_template

from lib.model.part import Part

app = Quart(__name__, static_folder="./_site", static_url_path="/")

if 'ELASTICSEARCH' in os.environ:
    es = Elasticsearch([os.environ['ELASTICSEARCH']])
else:
    es = Elasticsearch()

def for_hoomans():
    m = request.accept_mimetypes
    return m.accept_html or not m.accept_json

@app.route("/search", strict_slashes=False)
async def search():
    q = request.args.get("q", '')
    start = request.args.get("start", 0)
 
    if not q:
        summary, timing, results = ('', '', [])
    else:
        es_results = es.search(index="parts", body={
            "query": {
                "simple_query_string": {
                    "all_fields": True,
                    "query": q,
                }
            },
            "timeout": "500ms",
            "from": start,
        })
        if es_results['timed_out']:
            raise RuntimeError(f"Query timed out: '{q}'")

        hits = es_results['hits']

        if hits['total']['relation'] == 'gte':
            prefix = 'about '
        else:
            prefix = ''
        summary = f"Found {prefix}{hits['total']['value']} results."
        timing = f"Search took approximately {es_results['took']}ms."

        results = [Part.get_dict(r['_id']) for r in sorted(hits['hits'], key=lambda x: x['_score'])]

    page = {
        'query': q,
        'summary': summary,
        'timing': timing,
        'results': results,
    }

    if for_hoomans():
        return await render_template("search.html", page=page)
    else:
        return page


if __name__ == "__main__":
    app.run(debug=True)
