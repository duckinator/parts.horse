import cherrypy
from .datasheets import Datasheets
from .search import Search


class Home:
    pass


def prepare():
    cherrypy.tree.mount(Home(), '/', 'config/app.conf')
    cherrypy.tree.mount(Datasheets(),
                        '/',
                        'config/app.conf')
    cherrypy.tree.mount(Search(),
                        '/',
                        'config/app.conf')

    cherrypy.config.update('config/server.conf')


def start():
    cherrypy.engine.start()


def block():
    cherrypy.engine.block()
