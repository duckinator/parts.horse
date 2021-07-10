#!/usr/bin/env python3

import os
from pathlib import Path

from elasticsearch import AsyncElasticsearch
from quart import Quart, redirect, request, render_template, safe_join, send_file

from lib.model.part import Part


app = Quart(__name__)

STATIC_DIR = Path(__file__).parent / '_site'

@app.route("/", defaults={'path': ""})
@app.route("/<path:path>")
async def serve(path: str):
    p = safe_join(STATIC_DIR, path)

    if p.is_dir():
        p /= 'index.html'

    if p.is_file():
        return await send_file(p)

    return "File not found", 404



if 'ELASTICSEARCH' in os.environ:
    es = AsyncElasticsearch([os.environ['ELASTICSEARCH']])
else:
    es = AsyncElasticsearch()

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
        es_results = await es.search(index="parts", body={
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


@app.route("/ds/<part_id>")
@app.route("/datasheet/<part_id>")
async def datasheet(part_id):
    part = Part.get(part_id)
    if part is None:
        return "Part not found", 404

    return redirect(part.data['datasheet'])


if __name__ == "__main__":
    app.run(debug=True)
