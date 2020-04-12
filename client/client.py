import requests
from urllib.parse import urljoin
import pathlib

class Request:
    def __init__(self, host="localhost", port=9999):
        self._url = "http://{host}:{port}".format(host=host, port=port)
        self._response = requests.Response()
        self._target_dir = pathlib.Path.cwd().joinpath('.files')

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
    #req.send_file(".files/test0.txt")
    #req.send_file(".files/test1.txt")
    #req.send_file(".files/test2.txt")
    req.send_file("folder0/nested file.txt")

if __name__ == '__main__':
    main()
