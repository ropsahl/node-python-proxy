import glob
import hashlib
import socket
from subprocess import Popen

import time

CMD_LINE_ARG_PORT = ' --port='


def get_free_tcp_port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(('', 0))
    addr, port = tcp.getsockname()
    tcp.close()
    print("get_free_port: " + str(port))
    return port


class UpService:
    def __init__(self, file):
        self.file = file
        self.hash = hash_for_file(file)
        self.port = 0
        split = file.split('.')
        self.type = split[len(split) - 1]
        self.name = file[len('service_'):-(len(self.type) + 1)]
        self.command = None
        self.process = None

    def __eq__(self, other):
        return self.hash == other.hash

    def set_port(self, port):
        self.port = port

    def get_command(self, new_port=False):
        if self.command is None or new_port:
            self.port = get_free_tcp_port()
            if self.type == 'js':
                self.command = 'node ./' + self.file + CMD_LINE_ARG_PORT + str(self.port)
            elif self.type == 'py':
                self.command = 'python3 -u ./' + self.file + CMD_LINE_ARG_PORT + str(self.port)
            elif self.type == 'sh':
                self.command = 'bash ./' + self.file + CMD_LINE_ARG_PORT + str(self.port)
            self.command = self.command
        return self.command

    def get_name(self):
        return self.name

    def get_name_port_option(self):
        return self.name + '.port=' + str(self.port)

    def has_stopped(self):
        if self.process is None or self.process.poll() is not None:
            print("Has stopped: " + self.name)
            return True
        return False

    def stop(self):
        print("stopping: " + self.name + ", command: " + self.get_command())
        self.process.kill()

    def start(self, new_port=False):
        command = self.get_command(new_port) + ' 2>&1 | ./up-log.sh ' + self.name
        print("starting: " + self.name + ", command: " + command)
        self.process = Popen(command, shell=True)

    def restart(self):
        if not self.has_stopped():
            self.stop()
            self.process.wait()
        self.hash = hash_for_file(self.file)
        self.start(True)


class UpRoute(UpService):
    def __init__(self, file, port, services):
        super().__init__(file)
        self.services = services
        self.port = port
        split = file.split('.')
        self.type = split[len(split) - 1]
        self.name = file[len('route_'):-(len(self.type) + 1)]

    def get_command(self, new_port=False):
        if self.type == 'js':
            self.command = 'node ./' + self.file + CMD_LINE_ARG_PORT + str(
                self.port) + self.services_args()
        return self.command

    def services_args(self):
        ret = ""
        for service in self.services:
            ret += ' --service.' + service.get_name_port_option()
        return ret

    def restart(self, services):
        self.services = services
        super().restart()


def hash_for_file(filename):
    sha = hashlib.md5()
    with open(filename, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha.update(byte_block)
    return sha.hexdigest()[:8]


def scan_services():
    ret = []
    for file in glob.glob('service*'):
        ret.append(UpService(file))
    return ret


def scan_route(services, port):
    for file in glob.glob('route*'):
        return UpRoute(file, port, services)


def handle_config_change(running_services, configured_services):
    change = False
    for running in running_services:
        if running not in configured_services:
            print("Service changed or removed: " + running.get_name())
            running.stop()
            change = True

    for configured in configured_services:
        if configured not in running_services:
            r_list = list(filter(lambda r: (r.get_name() == configured.get_name()), running_services))
            if len(r_list) == 1:
                running = r_list[0]
                print("Service has changed: " + running.get_name())
                running.restart()
            else:
                print("Service added: " + configured.get_name())
                configured.start(True)
                running_services.append(configured)
            change = True
    return change


services = scan_services()
for service in services:
    service.start()

route = scan_route(services, 8100)
route.start()

print("---------------- Start monitoring -----------------")
while 1 == 1:
    for service in services:
        if service.has_stopped():
            service.restart()
    if route.has_stopped():
        route.restart()

    if handle_config_change(services, scan_services()):
        print("Change detected, restarting route")
        time.sleep(3)
        route.restart(services)

    time.sleep(2)
