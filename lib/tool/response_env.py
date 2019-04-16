import cherrypy
from lib import helpers

@cherrypy.tools.register('on_start_resource')
def response_env():
    headers = cherrypy.response.headers
    config = cherrypy.request.config

    is_json = helpers.is_json_response()

    if is_json:
        config['content-type'] = 'application/json'
    else:
        config['content-type'] = 'text/html'

    headers['Content-Type'] = config['content-type'] + '; charset=utf-8'
    config['globals'] = {'response': {'is_json': is_json}}
