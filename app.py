#!/usr/bin/env python3

import os
from pathlib import Path

from elasticsearch import AsyncElasticsearch
from quart import Quart, redirect, request, render_template, safe_join, send_file

from lib.model.part import Part


STATIC_DIR = Path(__file__).parent / '_site'
async def serve(path: str):
    p = safe_join(STATIC_DIR, path)

    if p.is_dir():
        p /= 'index.html'

    if p.is_file():
        return await send_file(p)

    return "File not found", 404


def for_hoomans():
    m = request.accept_mimetypes
    return m.accept_html or not m.accept_json


def search(es):
    async def handler():
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

    return handler


async def datasheet(part_id):
    part = Part.get(part_id)
    if part is None:
        return "Part not found", 404

    return redirect(part.data['datasheet'])


def gen_app():
    app = Quart(__name__)
    app.add_url_rule("/", view_func=serve, defaults={'path': ""})
    app.add_url_rule("/<path:path>", view_func=serve)

    if 'ELASTICSEARCH' in os.environ:
        es = AsyncElasticsearch([os.environ['ELASTICSEARCH']])
    else:
        es = AsyncElasticsearch()

    app.add_url_rule("/search", view_func=search(es), strict_slashes=False)
    app.add_url_rule("/ds/<part_id>", view_func=datasheet)
    app.add_url_rule("/datasheet/<part_id>", view_func=datasheet)

    return app


if __name__ == "__main__":
    gen_app().run(debug=True)
