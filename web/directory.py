from .base import *
from lib.model.part import Part

class DirectoryEntry(PartsHorseBase):
    def __init__(self, part_name):
        self.part_name = part_name
        super().__init__()

    @cherrypy.expose
    @cherrypy.tools.response_env()
    def index(self):
        page = Part.get_dict(self.part_name)
        return self.render(page)

@cherrypy.popargs('part_name', handler=DirectoryEntry)
class Directory(PartsHorseBase):
    @cherrypy.expose
    @cherrypy.tools.response_env()
    def index(self):
        return self.render({'parts': Part.all()})
