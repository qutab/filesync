from abc import ABC, abstractmethod
import socketserver
import http.server
from cgi import parse_header, parse_multipart
import cgitb
import cgi
import pathlib


class RequestHandler(http.server.CGIHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self._form = None
        super(RequestHandler, self).__init__(*args, **kwargs)

    def handle_rename(self):
        print("rename request received")

    def handle_move(self):
        print("move request received")

    def handle_delete(self):
        print("delete request received")

    def handle_add(self):
        print("add request received")

        fileitem = self._form['file']
        if fileitem.filename:
            target_path = pathlib.Path.cwd().joinpath('.files').joinpath(fileitem.filename)
            open(target_path.absolute(), 'wb').write(fileitem.file.read())
            print('The file "' + target_path.name + '" was uploaded successfully')
        else:
            print("No file was uploaded")

    def handle_update(self):
        print("update request received")

    def parse_post(self):
        ctype, pdict = parse_header(self.headers['content-type'])
        pdict['boundary'] = str(pdict['boundary']).encode('utf-8')

        if ctype == 'multipart/form-data':
            self._form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE':self.headers['Content-Type'],
                }
            )
            if not self._form.list:
                return
        else:
            raise RuntimeError

    def parse_path(self):
        self.path = self.path.split('/', 1)[1]

        if self.path == "rename":
            self.handle_rename()
        elif self.path == "move":
            self.handle_move()
        elif self.path == "delete":
            self.handle_delete()
        elif self.path == "add":
            self.handle_add()
        elif self.path == "update":
            self.handle_update()
        else:
            return False

        return True

    def do_POST(self):
        """Respond to a GET request."""
        try:
            self.parse_post()
        except RuntimeError:
            print("Unsupported form data")
            self.send_response(405)

        if self.parse_path():
            self.on_success()

    def on_success(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def on_failure(self, code=500):
        self.send_response(code)
        self.send_header("Content-type", "text/html")
        self.end_headers()


class SyncServer(ABC):
    """Abstract base class for server's sync operations"""

    @abstractmethod
    def start(self):
        raise NotImplementedError('Derived class must implement this method')

    @abstractmethod
    def stop(self):
        raise NotImplementedError('Derived class must implement this method')


class HttpServer(SyncServer):
    def __init__(self, host="localhost", port=9999):
        self._host = host
        self._port = port

    def start(self):
        print("Starting HTTP server...")
        with socketserver.TCPServer((self._host, self._port), RequestHandler) as server:
            server.cgi_directories = "/cgi-bin"
            server.serve_forever()

    def stop(self):
        print("starting http server")


def main():
    cgitb.enable(display=0, logdir="/logs")

    server = HttpServer()
    server.start()


if __name__ == '__main__':
    main()
