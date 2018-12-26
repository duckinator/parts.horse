import cherrypy
import os

class Helpers:
    def is_html_response():
        user_agent = cherrypy.request.headers.get('User-Agent', '')
        accepted_response_types = cherrypy.request.headers['Accept'].split(',')

        # If the user is using ELinks, we should always return HTML.
        if user_agent.startswith("ELinks/"):
            return True

        # If there were no relevant special cases, use the Accept header.
        return ('text/html' in accepted_response_types)

    def get_site_url():
        port = cherrypy.config.get('server.socket_port')
        socket_host = cherrypy.config.get('server.socket_host')
        host = cherrypy.request.headers.get('Host', socket_host)

        scheme = 'https' if (port == 443) else 'http'

        if scheme == 'http' and not host.endswith(str(port)):
            host += ':{}'.format(port)

        default_url = '{}://{}'.format(scheme, host)

        return os.environ.get('SITE_URL', default_url)
