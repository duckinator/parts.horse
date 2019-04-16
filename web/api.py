from .base import *

class Api(PartsHorseBase):
    @cherrypy.expose
    def index(self):
        return self.render()
