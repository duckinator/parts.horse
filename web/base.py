import json
import cherrypy
from jinja2 import Environment, FileSystemLoader


class PartsHorseBase:
    """Base class other Parts Horse apps should build on top of."""

    def __init__(self):
        env = Environment(loader=FileSystemLoader('templates'))
        env.filters['ljust'] = lambda value, *args: value.ljust(*args)
        env.filters['rjust'] = lambda value, *args: value.rjust(*args)
        self.env = env

        classname = self.__class__.__name__.lower()

        self.template = env.get_template(classname + '.html')

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
