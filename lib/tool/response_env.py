import cherrypy
from lib import helpers

@cherrypy.tools.register('on_start_resource')
def response_env():
    headers = cherrypy.response.headers
    config = cherrypy.request.config

    is_html = helpers.is_html_response()
    is_json = helpers.is_json_response()

    if is_html:
        config['content-type'] = 'text/html'
    elif is_json:
        config['content-type'] = 'application/json'
    else:
        config['content-type'] = 'text/plain'

    headers['Content-Type'] = config['content-type'] + '; charset=utf-8'
    headers['Connection'] = 'close'
    config['globals'] = {
        'response': {
            'is_html': is_html,
            'is_json': is_json,
        },
    }
