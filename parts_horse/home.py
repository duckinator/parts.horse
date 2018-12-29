from .base import *
from .search import *

class Home(PartsHorseBase):
    @cherrypy.expose
    def index(self):
        self.fixme()
        print(dict(cherrypy.request.config))
        return self.render({"recent": Search.recent()})
