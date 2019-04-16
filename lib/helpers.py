import cherrypy
import os

def is_json_response():
    headers     = cherrypy.request.headers
    user_agent  = headers.get('User-Agent', '')
    accepted    = headers.get('Accept', '').split(',')
    return ('application/json' in accepted)
