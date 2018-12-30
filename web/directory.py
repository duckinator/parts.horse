from .base import *
from lib.model.part import Part

@cherrypy.popargs('part_name')
class Directory(PartsHorseBase):
    @cherrypy.expose
    @cherrypy.tools.response_env()
    def index(self, part_name):
        page = Part.get_dict(part_name)
        return self.render(page)
