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

    cherrypy.tree.mount(Home(),       '/',       home_config)
    cherrypy.tree.mount(Directory(),  '/parts')
    cherrypy.tree.mount(Search(),     '/search')
    cherrypy.tree.mount(Datasheets(), '/datasheets')
    cherrypy.tree.mount(Datasheets(), '/ds')

    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': int(os.environ.get('PORT', 5000)),
    })

    cherrypy.engine.start()
    cherrypy.engine.block()
