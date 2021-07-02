#!/usr/bin/env python3

import os
from pathlib import Path
import re
import shlex
import socket
import subprocess
import sys
from time import sleep
from urllib.request import urlopen as get


class ManagedProcess:
    def __init__(self, process_type, command):
        self.command = command.strip()
        self.type = process_type
        self.env = {}
        self.proc = None
        self.log_file = None

    def port(self):
        return self.env['PORT']

    # Find an unused port.
    @staticmethod
    def find_port():
        # Create a socket.
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        return port

    def get_env(self):
        self.env['PORT'] = str(self.find_port())
        for (key, val) in os.environ.items():
            self.env[key] = val
        return self.env

    def start(self):
        env = self.get_env()

        command = self.command
        for (key, val) in env.items():
            command.replace('${}'.format(key), val)

        cmd = shlex.split(command)
        # pylint: disable=consider-using-with
        self.log_file = open('test-{}.log'.format(self.type), 'w')
        self.proc = subprocess.Popen(
            cmd,
            env=env,
            stdout=self.log_file,
            stderr=subprocess.STDOUT)
        # pylint: enable=consider-using-with

    def stop(self):
        try:
            self.proc.communicate(timeout=1)
        except subprocess.TimeoutExpired:
            pass
        self.proc.terminate()
        self.log_file.flush()
        self.log_file.close()


class ProcessManager:
    def __init__(self, procfile):
        self.processes = self.parse(procfile)

    def http_port(self):
        for proc in self.processes:
            if proc.type == 'web':
                return proc.port()
        return None

    @staticmethod
    def parse(procfile):
        procfile_lines = procfile.strip().split('\n')
        processes = []
        for line in procfile_lines:
            process_type, command = line.split(':', 1)
            processes += [ManagedProcess(process_type, command)]
        return processes

    def start(self, types):
        print('Start: ', end='')
        for proc in self.processes:
            if proc.type in types:
                print(proc.type, end=' ')
                proc.start()
        print('\n')

    def stop(self):
        print('\nStop:  ', end='')
        for proc in self.processes:
            if proc:
                print(proc.type, end=' ')
                proc.stop()
        print('')

class CheckRunner:
    def __init__(self, checks):
        self.env, self.checks = self.parse(checks)
        self.wait = int(self.env.get('WAIT', 1))
        self.timeout = int(self.env.get('TIMEOUT', 30))
        self.attempts = int(self.env.get('ATTEMPTS', 5))

    @staticmethod
    def parse(checks):
        env_regex = re.compile(r'^[A-Z_]+=.*')
        lines = checks.strip().split('\n')
        env = {}
        checks = []

        for line in lines:
            # Skip blank lines and comments.
            if len(line.strip()) == 0 or line[0] == '#':
                continue

            if env_regex.match(line):
                key, _, val = line.partition('=')
                env[key] = val
            else:
                checks += [line]

        return [env, checks]

    def run_check(self, url, content, line):
        result = None

        for attempt in range(1, self.attempts):
            try:
                result = get(url).read().decode()  # pylint: disable=consider-using-with
            except: # pylint: disable=bare-except
                exc_type, exc_value, _ = sys.exc_info()
                if attempt <= self.attempts:
                    if os.environ.get('DEBUG', 'false').lower() != 'false':
                        print('---  Attempt {} failed.'.format(attempt))
                else:
                    print('ERR  {}'.format(line))
                    print('  {}: {}'.format(exc_type.__name__, exc_value))
                    return False

            if result is not None and content in result:
                print('PASS {}'.format(line))
                if attempt > 1:
                    print('  !!! Took {} attempts.'.format(attempt))
                return True

        print('FAIL {}'.format(line))
        print('  {}'.format('Page did not include: {}'.format(content)))
        return False

    def run(self, port):
        total = 0
        failed = 0

        for line in self.checks:
            total += 1

            url, _, content = line.partition(' ')
            content = content.lstrip()

            if url.startswith('/'):
                url = 'http://127.0.0.1:{}{}'.format(port, url)

            success = self.run_check(url, content, line)

            if not success:
                failed += 1

        print('')
        print('{} checks, {} failures'.format(total, failed))

        return failed == 0


class TestThingy:
    def __init__(self, directory):
        self.procfile = Path(directory, 'Procfile').read_text()
        self.checks = Path(directory, 'CHECKS').read_text()

    def run(self):
        pm = ProcessManager(self.procfile)
        checks = CheckRunner(self.checks)

        try:
            pm.start(checks.env.get('TEST_PROCS', 'web'))
            sleep(1 + int(checks.env.get('WAIT', 1)))
            success = checks.run(pm.http_port())
        finally:
            pm.stop()

        if success:
            sys.exit(0)
        else:
            sys.exit(1)


if __name__ == '__main__':
    TestThingy(Path.cwd()).run()
