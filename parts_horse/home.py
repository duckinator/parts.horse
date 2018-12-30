from .base import *
from .search import *

class Home(PartsHorseBase):
    @cherrypy.expose
    def index(self):
        return self.render()
