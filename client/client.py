import requests
from urllib.parse import urljoin
from shared import argparser
import pathlib

from dirmonitor import *


class Request:
    def __init__(self, host="localhost", port=9999, target_dir=pathlib.Path.cwd()):
        self._url = "http://{host}:{port}".format(host=host, port=port)
        self._response = requests.Response()
        self._target_dir = target_dir

    def send_file(self, filename, action='add'):
        rel_path = filename.relative_to(self._target_dir).as_posix()

        if filename.is_file():
            files = {
                'file': open(filename.as_posix(), 'rb'),
                'relative_path': rel_path,
                'is_file': True
            }
            self._response = requests.post(urljoin(self._url, action), files=files)
        else:
            data = {
                'relative_path': rel_path,
                'is_file': False
            }
            self._response = requests.post(urljoin(self._url, action), data=data)

        self.print_response()

    def print_response(self):
        print("status:", self._response.status_code)
        return
        # TODO: Print the following in verbose mode
        # for attr in self._response.__attrs__:
        #    print(str(attr), ": ", getattr(self._response, attr))


def main():
    print("sending request")

    parser = argparser.Parser()
    target_dir = parser.get_target_path()

    dirmonitor = DirMonitor(target_dir)

    req = Request(target_dir=target_dir)

    for item in dirmonitor.get_fsitem_list():
        req.send_file(item.resolve())

if __name__ == '__main__':
    main()
