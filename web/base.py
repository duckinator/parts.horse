import cherrypy
from jinja2 import Environment, FileSystemLoader
import json

import lib.tool.response_env

class PartsHorseBase(object):
    def __init__(self):
        env = Environment(loader=FileSystemLoader('templates'))
        env.filters['ljust'] = lambda value, *args: value.ljust(*args)
        env.filters['rjust'] = lambda value, *args: value.rjust(*args)
        self.env = env

        classname = self.__class__.__name__.lower()

        self.template = env.get_template(classname + '.html')

    def render(self, page={}):
        config = cherrypy.request.config
        content_type = config['content-type']

        if config['globals']['response']['is_json']:
            return json.dumps(page, indent=2, sort_keys=True).encode('utf-8')
        else:
            return self.template.render(page=page, **config['globals'])
