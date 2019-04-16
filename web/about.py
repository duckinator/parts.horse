import cherrypy
from .base import PartsHorseBase

class About(PartsHorseBase):
    @cherrypy.expose
    def index(self):
        return self.render()
