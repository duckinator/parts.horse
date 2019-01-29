from .base import *
from .json_directory import *
from lib.model.part import Part

class DirectoryEntry(JsonDirectoryEntry):
    @cherrypy.expose
    @cherrypy.tools.response_env()
    def index(self):
        # Take the superclass implementation and pass it to self.render().
        return self.render(super().index())

@cherrypy.popargs('part_name', handler=DirectoryEntry)
class Directory(JsonDirectory):
    @cherrypy.expose
    @cherrypy.tools.response_env()
    def index(self):
        # Take the superclass implementation and pass it to self.render().
        return self.render(super().index())
