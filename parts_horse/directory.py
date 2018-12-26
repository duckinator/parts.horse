from .base import *

class Directory(PartsHorseBase):
    def _cp_dispatch(self, vpath):
        AppGlobals.update_site(self.env)

        if len(vpath) == 1:
            cherrypy.request.params['part_name'] = vpath.pop()
            return self
        return vpath

    @cherrypy.expose
    def index(self, part_name):
        part = part_name.lower()
        page = self.part_dict(part)
        return self.render(page)