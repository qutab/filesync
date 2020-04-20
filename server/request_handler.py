import http.server
import logging

from server.executor_mixin import ExecutorMixin
from server.parse_mixin import ParseMixin
from server.sync_mixin import SyncMixin


class RequestHandler(SyncMixin, ParseMixin, ExecutorMixin, http.server.CGIHTTPRequestHandler):
    """
    This is the main class responsible for handling incoming client requests
    It uses different mixin classes to sync contents on server filesystem
    """

    def __init__(self, *args, **kwargs):
        self._postvars = None
        self._form = None
        super(RequestHandler, self).__init__(*args, **kwargs)

    @property
    def post_vars(self):
        return self._postvars

    @property
    def post_form(self):
        return self._form

    def do_POST(self):
        """Handle POST request."""
        try:
            self.parse_post()
        except RuntimeError:
            logging.error("Unsupported form data received from client")
            self.on_failure(code=403)
            return

        if self.execute_command():
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
