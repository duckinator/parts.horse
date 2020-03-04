import cherrypy
from lib.model.part import Part
from .base import PartsHorseBase


@cherrypy.popargs('part_name')
class Datasheets(PartsHorseBase):
    @cherrypy.expose
    def datasheets(self, part_name):
        page = Part.get_dict(part_name)
        cherrypy.response.headers['Location'] = page['datasheet_redirect_target']
        cherrypy.response.status = 302
        return self.render(page)

    @cherrypy.expose
    def ds(self, part_name):
        return self.datasheets(part_name)
