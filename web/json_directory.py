from .base import *
from lib.model.part import Part

class JsonDirectoryEntry(PartsHorseBase):
    def __init__(self, part_name):
        self.part_name = part_name
        super().__init__()

    @cherrypy.expose
    @cherrypy.tools.response_env()
    @cherrypy.tools.json_out()
    def index(self):
        page = Part.get_dict(self.part_name)
        return page

@cherrypy.popargs('part_name', handler=JsonDirectoryEntry)
class JsonDirectory(PartsHorseBase):
    @cherrypy.expose
    @cherrypy.tools.response_env()
    @cherrypy.tools.json_out()
    def index(self):
        return {'parts': Part.all()}
