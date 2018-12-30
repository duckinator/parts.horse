from .base import *

@cherrypy.popargs('part_name')
class Datasheets(PartsHorseBase):
    @cherrypy.expose
    @cherrypy.tools.response_env()
    def index(self, part_name):
        page = self.part_dict(part_name)
        cherrypy.response.headers['Location'] = page['datasheet_redirect_target']
        cherrypy.response.status = 302
        return page['datasheet_redirect_target']

