import cherrypy

class Helpers:
    def is_html_response():
        user_agent = cherrypy.request.headers.get('User-Agent', '')
        accepted_response_types = cherrypy.request.headers['Accept'].split(',')

        # If the user is using ELinks, we should always return HTML.
        if user_agent.startswith("ELinks/"):
            return True

        # If there were no relevant special cases, use the Accept header.
        return ('text/html' in accepted_response_types)

