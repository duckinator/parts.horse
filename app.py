#!/usr/bin/env python3

import cherrypy
from web.api            import Api
from web.home           import Home
from web.datasheets     import Datasheets
from web.diagnostics    import Diagnostics
from web.directory      import Directory
from web.search         import Search

if __name__ == '__main__':
    cherrypy.tree.mount(Home(),         '/',            'config/home.conf')
    cherrypy.tree.mount(Api(),          '/api',         'config/app.conf')
    cherrypy.tree.mount(Datasheets(),   '/datasheets',  'config/app.conf')
    cherrypy.tree.mount(Datasheets(),   '/ds',          'config/app.conf')
    cherrypy.tree.mount(Diagnostics(),  '/diagnostics', 'config/app.conf')
    cherrypy.tree.mount(Directory(),    '/parts',       'config/app.conf')
    cherrypy.tree.mount(Search(),       '/search',      'config/app.conf')

    cherrypy.config.update('config/server.conf')

    cherrypy.engine.start()
    cherrypy.engine.block()
