import cgi
import http.server
import logging
import pathlib
from cgi import parse_header
from urllib.parse import parse_qs

from shared import argparser


class RequestHandler(http.server.CGIHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self._postvars = None
        self._form = None
        self._target_dir = pathlib.Path(argparser.Parser().target_path)
        print(f"path: {self._target_dir}")
        if not self._target_dir.exists() or not self._target_dir.is_dir():
            raise NotADirectoryError

        super(RequestHandler, self).__init__(*args, **kwargs)

    def handle_delete(self):
        file_rel_path = self._postvars[b'relative_path'][0].decode()
        abs_path = self._target_dir.joinpath(file_rel_path)
        try:
            abs_path.unlink(abs_path)
        except FileNotFoundError:
            logging.error(f"File {abs_path} not found on server.")

    def handle_add(self):
        if self._form:
            fileitem = self._form['file']
        else:
            # TODO: Handle syncing of empty folders
            logging.warning("Failed to add file/folder. Empty folders are not synced currently.")
            return

        relative_path = self._form.getvalue('relative_path')
        relative_path = pathlib.Path(relative_path)

        if fileitem.filename:
            target_path = self._target_dir.joinpath(relative_path.parent)
            pathlib.Path(target_path).mkdir(parents=True, exist_ok=True)

            open(target_path.joinpath(fileitem.filename).absolute(), 'wb').write(fileitem.file.read())
            logging.debug(f"File {fileitem.filename} saved successfully!")
        else:
            logging.warning("No file was uploaded while handling add command.")

    def handle_update(self):
        self.handle_add()

    def parse_post(self):
        ctype, pdict = parse_header(self.headers['content-type'])

        if ctype == 'multipart/form-data':
            self._form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': self.headers['Content-Type'],
                }
            )
            if not self._form.list:
                return
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            self._postvars = parse_qs(self.rfile.read(length), keep_blank_values=True)
        else:
            raise RuntimeError

    def parse_path(self):
        command = self.path.split('/', 1)[1]

        if command == "add":
            self.handle_add()
        elif command == "delete":
            self.handle_delete()
        elif command == "update":
            self.handle_update()
        else:
            logging.error(f"Unsupported file command {self.path} received.")
            return False

        return True

    def do_POST(self):
        """Respond to a GET request."""
        try:
            self.parse_post()
        except RuntimeError:
            logging.error("Unsupported form data received from client")
            self.on_failure(code=403)
        else:
            if self.parse_path():
                self.on_success()
            else:
                self.on_failure()

    def on_success(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def on_failure(self, code=500):
        self.send_response(code)
        self.send_header("Content-type", "text/html")
        self.end_headers()
