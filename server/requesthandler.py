import cgi
import http.server
import pathlib
from cgi import parse_header

from shared import argparser


class RequestHandler(http.server.CGIHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self._form = None
        parser = argparser.Parser()
        self._target_dir = parser.get_target_path()

        super(RequestHandler, self).__init__(*args, **kwargs)

    def handle_rename(self):
        print("rename request received")

    def handle_move(self):
        print("move request received")

    def handle_delete(self):
        print("delete request received")

    def handle_add(self):
        fileitem = self._form['file']
        relative_path = self._form.getvalue('relative_path')
        relative_path = pathlib.Path(relative_path.decode('utf-8'))

        if fileitem.filename:
            target_path = self._target_dir.joinpath(relative_path.parent)
            pathlib.Path(target_path).mkdir(parents=True, exist_ok=True)

            open(target_path.joinpath(fileitem.filename).absolute(), 'wb').write(fileitem.file.read())
        else:
            print("No file was uploaded")

    def handle_update(self):
        print("update request received")

    def parse_post(self):
        ctype, pdict = parse_header(self.headers['content-type'])

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
            print("Unsupported form data received from client")
            self.on_failure(403)

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
