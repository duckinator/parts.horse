#!/usr/bin/env python3

import cherrypy
from parts_horse import *

if __name__ == '__main__':
    site_dir = str(Path(__file__).resolve().parent)

    home_config = {
            '/': {
                'tools.staticdir.root': site_dir,
                'tools.staticdir.on': True,
                'tools.staticdir.dir': 'assets',
                }
            }

    cherrypy.tree.mount(PartHomePage(),  '/',       home_config)
    cherrypy.tree.mount(PartDirectory(), '/parts')
    cherrypy.tree.mount(PartSearch(),    '/search')
    cherrypy.tree.mount(DatasheetRedirects(),   '/datasheets')
    cherrypy.tree.mount(DatasheetRedirects(),   '/ds')

    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': int(os.environ.get('PORT', 5000)),
    })

    cherrypy.engine.start()
    cherrypy.engine.block()
