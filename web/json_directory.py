from .base import *
from lib.model.part import Part

@cherrypy.popargs('part_name')
class JsonDirectory(PartsHorseBase):
    @cherrypy.expose
    @cherrypy.tools.response_env()
    @cherrypy.tools.json_out()
    def index(self, part_name):
        return Part.get_dict(part_name)
