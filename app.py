#!/usr/bin/env python3

import cherrypy
import web

if __name__ == '__main__':
    cherrypy.quickstart(web.Search(), '/', config='config/server.conf')
else:
    wsgi = cherrypy.Application(web.Search(), '/', config='config/server.conf')
