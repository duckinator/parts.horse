import cherrypy
from jinja2 import Environment, FileSystemLoader

from .helpers import Helpers
from .parts import Parts

@cherrypy.tools.register('on_start_resource')
def response_env():
    headers = cherrypy.response.headers
    config = cherrypy.request.config

    is_html = Helpers.is_html_response()

    if is_html:
        config['content-type'] = 'text/html'
    else:
        config['content-type'] = 'text/plain'

    headers['Content-Type'] = config['content-type'] + '; charset=utf-8'
    config['globals'] = {
        'response': {'is_html': is_html}
    }


class PartsHorseBase(object):
    def __init__(self):
        env = Environment(loader=FileSystemLoader('templates'))
        env.filters['ljust'] = lambda value, *args: value.ljust(*args)
        env.filters['rjust'] = lambda value, *args: value.rjust(*args)
        self.env = env

        classname = self.__class__.__name__.lower()

        self.templates = {
            'text/html':    env.get_template(classname + '.html'),
            'text/plain':   env.get_template(classname + '.txt'),
        }

    def render(self, page={}):
        config = cherrypy.request.config
        content_type = config['content-type']
        return self.templates[content_type].render(page=page, **config['globals'])
