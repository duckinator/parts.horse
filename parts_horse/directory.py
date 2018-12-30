from .base import *

@cherrypy.popargs('part_name')
class Directory(PartsHorseBase):
    @cherrypy.expose
    @cherrypy.tools.response_env()
    def index(self, part_name):
        part = part_name.lower()
        page = self.part_dict(part)
        return self.render(page)
