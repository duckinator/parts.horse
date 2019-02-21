import cherrypy
import os

def is_html_response():
    headers     = cherrypy.request.headers
    user_agent  = headers.get('User-Agent', '')
    accepted    = headers.get('Accept', '').split(',')

    # If the user is using ELinks, we should always return HTML.
    if user_agent.startswith("ELinks/"):
        return True

    # If there were no relevant special cases, use the Accept header.
    return ('text/html' in accepted)

def is_json_response():
    headers     = cherrypy.request.headers
    user_agent  = headers.get('User-Agent', '')
    accepted    = headers.get('Accept', '').split(',')
    return ('application/json' in accepted)

def get_site_url():
    socket_port = cherrypy.config.get('server.socket_port')
    socket_host = cherrypy.config.get('server.socket_host')
    fallback_host = "{}:{}".format(socket_host, socket_port)

    host_header = cherrypy.request.headers.get('Host', fallback_host)

    host, port = host_header.split(':', 1)

    if port == '443':
        scheme = 'https'
    else:
        scheme = 'http'
        if port != '80':
            host = "{}:{}".format(host, port)

    default_url = '{}://{}'.format(scheme, host)

    return os.environ.get('SITE_URL', default_url)
