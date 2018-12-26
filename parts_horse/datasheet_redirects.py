from .base import *

class DatasheetRedirects(PartsHorseBase):
    def _cp_dispatch(self, vpath):
        if len(vpath) == 1:
            cherrypy.request.params['part_name'] = vpath.pop()
            return self
        return vpath

    @cherrypy.expose
    def index(self, part_name):
        AppGlobals.update_site(self.env)

        page = self.part_dict(part_name)
        cherrypy.response.headers['Location'] = page['datasheet_redirect_target']
        cherrypy.response.status = 302
        return page['datasheet_redirect_target']

