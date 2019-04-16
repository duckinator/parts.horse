from .base import *

class About(PartsHorseBase):
    @cherrypy.expose
    @cherrypy.tools.response_env()
    def index(self):
        return self.render()
