import json
import cherrypy
from jinja2 import Environment, FileSystemLoader
from lib.render import PHRender


class PartsHorseBase:
    """Base class other Parts Horse apps should build on top of."""

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
