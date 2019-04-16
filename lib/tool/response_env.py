import cherrypy

@cherrypy.tools.register('on_start_resource')
def response_env():
    headers = cherrypy.response.headers
    config = cherrypy.request.config

    accepted = headers.get('Accept', '').split(',')
    is_json = 'application/json' in accepted

    if is_json:
        config['content-type'] = 'application/json'
    else:
        config['content-type'] = 'text/html'

    headers['Content-Type'] = config['content-type'] + '; charset=utf-8'
    config['globals'] = {'response': {'is_json': is_json}}
