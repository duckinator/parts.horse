#!/usr/bin/env python3

import cherrypy
import web

web.prepare()
app = cherrypy.tree

cherrypy.config.update({'engine.autoreload.on': False})
cherrypy.server.unsubscribe()
web.start()
