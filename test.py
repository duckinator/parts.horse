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
    def __init__(self, process_type, command, verbose=False, env={}):
        self.command = command.strip()
        self.type = process_type
        self.env = env
        self.proc = None
        self.verbose = verbose

    def port(self):
        return self.env['PORT']

    # Get a freely-available port.
    def find_port(self):
        # Create a socket.
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", 0))
        s.listen(1)
        port = s.getsockname()[1]
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        return port

    def get_env(self):
        env = self.env
        for key in self.env.keys():
            env[key] = self.env[key]
        env['PORT'] = str(self.find_port())
        for key in os.environ.keys():
            env[key] = os.environ[key]
        return env

    def start(self):
        env = self.get_env()
        if self.verbose:
            print("[{}] Start: {} (port {})".format(self.type, self.command, env['PORT']))

        command = self.command
        for key in env.keys():
            command.replace("${}".format(key), env[key])
        cmd = shlex.split(command)
        self.log_file = open('test-{}.log'.format(self.type), 'w')
        self.proc = subprocess.Popen(cmd, env=env,
                stdout=self.log_file, stderr=subprocess.STDOUT)
        return True

    def stop(self):
        if self.verbose:
            print("[{}] Stop:  {}".format(self.type, self.command))
        try:
            self.proc.communicate(timeout=1)
        except:
            pass
        self.proc.terminate()
        self.log_file.flush()
        self.log_file.close()

class ProcessManager:
    def __init__(self, procfile, verbose=False):
        self.processes = self.parse(procfile)
        self.verbose = verbose

    def http_port(self):
        return self.find_process_by_type('web').port()

    def find_process_by_type(self, process_type):
        for proc in self.processes:
            if proc.type == process_type:
                return proc

    def parse(self, procfile):
        procfile_lines = procfile.strip().split("\n")
        processes = []
        for line in procfile_lines:
            process_type, command = line.split(':', 1)
            processes += [ManagedProcess(process_type, command)]
        return processes

    def start(self, types):
        for proc in self.processes:
            if proc.type in types:
                proc.start()

    def stop(self):
        if self.verbose:
            print("")
        for proc in self.processes:
            proc.stop()

class CheckRunner:
    def __init__(self, checks, verbose=False):
        self.env, self.checks = self.parse(checks)
        self.verbose = verbose

    def parse(self, checks):
        env_regex = re.compile(r"^[A-Z_]+=.*")
        lines = checks.strip().split("\n")
        env = {}
        checks = []

        for line in lines:
            # Skip blank lines and comments.
            if len(line.strip()) == 0 or line[0] == '#':
                continue

            if env_regex.match(line):
                key, val = line.split('=', 1)
                env[key] = val
            else:
                checks += [line]

        return [env, checks]

    def run(self, port):
        total = 0
        passed = 0
        failed = 0

        for line in self.checks:
            total += 1

            url, _, content = line.partition(' ')
            content = content.lstrip()

            if url.startswith('/'):
                url = 'http://127.0.0.1:{}{}'.format(port, url)

            exception = None
            try:
                result = get(url).read().decode()
            except ConnectionRefusedError as e:
                exception = e

            if (not exception) and (content in result):
                passed += 1
                print("PASS {}".format(line))
            else:
                print("FAIL {}".format(line))
                if exception:
                    print("  {}".format(exception))
                else:
                    print("  {}".format("Page did not include: {}".format(content)))
        print("")
        print("{} checks, {} failures".format(total, failed))

        return (failed == 0)

class TestThingy:
    def __init__(self, directory):
        self.procfile = Path(directory, 'Procfile').read_text()
        self.checks = Path(directory, 'CHECKS').read_text()

    def run(self, verbose=False):
        pm = ProcessManager(self.procfile, verbose=verbose)
        checks = CheckRunner(self.checks, verbose=verbose)

        try:
            pm.start(checks.env['TEST_PROCS'])
            sleep(1)
            success = checks.run(pm.http_port())
        finally:
            pm.stop()

        if success:
            exit(0)
        else:
            exit(1)

if __name__ == "__main__":
    verbose = '--verbose' in sys.argv
    TestThingy(Path.cwd()).run(verbose=verbose)
