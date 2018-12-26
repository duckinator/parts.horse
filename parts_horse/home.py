from .base import *
from .search import *

class Home(PartsHorseBase):
    @cherrypy.expose
    def index(self):
        AppGlobals.update_site(self.env)

        page = self.page_dict({"recent": Search.recent()})
        return self.render(page)
