from .base import *
from .search import *

class Home(PartsHorseBase):
    @cherrypy.expose
    def index(self):
        self.fixme()
        return self.render()
