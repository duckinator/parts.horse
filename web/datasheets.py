from .base import *
from lib.model.part import Part

@cherrypy.popargs('part_name')
class Datasheets(PartsHorseBase):
    @cherrypy.expose
    @cherrypy.tools.response_env()
    def index(self, part_name):
        page = Part.get_dict(part_name)
        cherrypy.response.headers['Location'] = page['datasheet_redirect_target']
        cherrypy.response.status = 302
        return self.render(page)
