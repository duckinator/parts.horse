from .base import *
from .search import *

class Api(PartsHorseBase):
    @cherrypy.expose
    @cherrypy.tools.response_env()
    def index(self):
        return self.render()
