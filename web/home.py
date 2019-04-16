import cherrypy
from .base import PartsHorseBase

class Home(PartsHorseBase):
    @cherrypy.expose
    def index(self):
        return self.render()
