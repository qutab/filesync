import requests
from urllib.parse import urljoin
import pathlib
from shared import argparser


class Request:
    def __init__(self, host="localhost", port=9999):
        self._url = "http://{host}:{port}".format(host=host, port=port)
        self._response = requests.Response()

        parser = argparser.Parser()
        self._target_dir = parser.get_target_path()

    def send_file(self, filename, action='add'):
        abs_path = self._target_dir.joinpath(filename)
        files = {'file': open(abs_path.as_posix(), 'rb'), 'relative_path': filename}
        self._response = requests.post(urljoin(self._url, action), files=files)
        self.print_response()

    def print_response(self):
        print("status:", self._response.status_code)
        return
        # TODO: Print the following in verbose mode
        # for attr in self._response.__attrs__:
        #    print(str(attr), ": ", getattr(self._response, attr))


def main():
    print("sending request")

    req = Request()
    req.send_file("test0.txt")
    req.send_file("test1.txt")
    req.send_file("folder0/nested file0.txt")
    req.send_file("folder1/nested folder/double nested file0.txt")
    req.send_file("folder1/nested file1.txt")


if __name__ == '__main__':
    main()
