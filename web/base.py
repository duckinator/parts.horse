import cherrypy
from jinja2 import Environment, FileSystemLoader

import lib.tool.response_env

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
