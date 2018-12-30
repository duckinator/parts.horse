from .base import *
from .parts import Parts

@cherrypy.popargs('part_name')
class Directory(PartsHorseBase):
    @cherrypy.expose
    @cherrypy.tools.response_env()
    def index(self, part_name):
        page = Parts.get_dict(part_name)
        return self.render(page)
