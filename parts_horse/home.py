from .base import *
from .search import *

class Home(PartsHorseBase):
    @cherrypy.expose
    def index(self):
        page = self.page_dict({"recent": Search.recent()})
        return self.render(page)
