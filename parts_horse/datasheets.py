from .base import *
from .parts import Parts

@cherrypy.popargs('part_name')
class Datasheets(PartsHorseBase):
    @cherrypy.expose
    @cherrypy.tools.response_env()
    def index(self, part_name):
        page = Parts.get_dict(part_name)
        cherrypy.response.headers['Location'] = page['datasheet_redirect_target']
        cherrypy.response.status = 302
        return self.render(page)
