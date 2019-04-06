import os
from lib.model.part import Part
from pathlib import Path
import time
import socket
import threading
import urllib

from .base import *
from lib.model.part import Part


class Diagnostic():
    INFO = 'info'
    GOOD = 'good'
    BAD = 'bad'

    def __init__(self):
        self.name = type(self).__name__
        self.status, self.summary = self.check()


class MetaDiagnostic(Diagnostic):
    def __init__(self, status, summary):
        self.name = 'Diagnostics'
        self.summary = summary
        self.status = status


class MemoryUsage(Diagnostic):
    def check(self):
        path = Path('/proc/self/status')
        if not path.exists():
            return (self.INFO, "Unavailable.")

        data = path.read_text()
        lines = data.strip().split('\n')
        data = dict(map(lambda x: map(str.strip, x.split(':', 1)), lines))

        return (self.GOOD, data['VmRSS'])


class ThreadCount(Diagnostic):
    def check(self):
        return (self.INFO, str(threading.active_count()))


class Search(Diagnostic):
    def check(self):
        port = cherrypy.config.get('server.socket_port', 5000)
        query = 'cd'
        search_url = 'http://localhost:{}/search?q={}'.format(port, query)

        start = time.time()
        result = None
        try:
            result = urllib.request.urlopen(search_url)
        except (urllib.error.URLError, socket.timeout) as err:
            return (self.BAD, 'Error: {}'.format(str(err)))
        end = time.time()
        duration = end - start

        if result.status < 200 or result.status >= 400:
            return (self.BAD, 'Got HTTP {}'.format(result.status))

        if duration > 0.5:
            return 'Degraded performance.'

        body = result.read().decode()
        has_schmitt = 'CD40106 - Hex Schmitt Trigger' in body
        has_dual_and = 'CD4081 - Quad 2-Input AND Gate'
        if not (has_schmitt and has_dual_and):
            return (self.BAD, 'Got unexpected results.')

        return (self.GOOD, 'Good')


class DiagnosticsHandler():
    classes = [
        ThreadCount,
        MemoryUsage,
        Search,
    ]

    def __init__(self):
        self.diagnostics = [
            MetaDiagnostic(Diagnostic.BAD, 'Diagnostics never started!')
        ]
        self.run()

    def run(self):
        thread = threading.Thread(
            target=self.update,
            args=(self.store_diagnostics,),
            daemon=True,
        ).start()

    def update(self, callback):
        callback([
            MetaDiagnostic(Diagnostic.INFO, 'Waiting for data.')
        ])
        time.sleep(1)
        while True:
            print('Generating diagnostics.')
            callback(list(map(lambda cls: cls(), self.classes)))
            time.sleep(5 * 60) # 5 minutes.

    def store_diagnostics(self, diagnostics):
        self.diagnostics = diagnostics
        webhook = os.environ.get('DIAGNOSTIC_WEBHOOK', None)
        if webhook is not None:
            pass # TODO: Actually submit data via webhook.


class Diagnostics(PartsHorseBase):
    handler = DiagnosticsHandler()

    @cherrypy.expose
    @cherrypy.tools.response_env()
    def index(self):
        return self.render({
            'diagnostics': self.handler.diagnostics,
        })
