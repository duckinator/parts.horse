from .base import *

class About(PartsHorseBase):
    @cherrypy.expose
    def index(self):
        return self.render()
