import cherrypy
from .about         import About
from .api           import Api
from .home          import Home
from .image         import ImageGen
from .datasheets    import Datasheets
from .directory     import Directory
from .search        import Search

def prepare():
    cherrypy.tree.mount(Home(),         '/',            'config/home.conf')
    cherrypy.tree.mount(About(),        '/about',       'config/app.conf')
    cherrypy.tree.mount(Api(),          '/api',         'config/app.conf')
    cherrypy.tree.mount(ImageGen(),     '/image',       'config/app.conf')
    cherrypy.tree.mount(Datasheets(),   '/datasheets',  'config/app.conf')
    cherrypy.tree.mount(Datasheets(),   '/ds',          'config/app.conf')
    cherrypy.tree.mount(Directory(),    '/parts',       'config/app.conf')
    cherrypy.tree.mount(Search(),       '/search',      'config/app.conf')

    cherrypy.config.update('config/server.conf')

def start():
    cherrypy.engine.start()

def block():
    cherrypy.engine.block()
