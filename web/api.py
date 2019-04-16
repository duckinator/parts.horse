import cherrypy
from .base import PartsHorseBase

class Api(PartsHorseBase):
    @cherrypy.expose
    def index(self):
        return self.render()
