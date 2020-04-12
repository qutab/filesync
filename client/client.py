import requests
from urllib.parse import urljoin


class Request:
    def __init__(self, host="localhost", port=9999):
        self._url = "http://{host}:{port}".format(host=host, port=port)
        self._response = requests.Response()

    def send_file(self, filename, action='add'):
        files = {'file': open(filename, 'rb'), 'relative_path': "/tmp_qazi", 'name': "filename"}
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
    req.send_file(".files/test0.txt")
    req.send_file(".files/test1.txt")
    req.send_file(".files/test2.txt")


if __name__ == '__main__':
    main()
