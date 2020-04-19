from cgi import parse_header, FieldStorage
from urllib.parse import parse_qs


class ParseMixin(object):
    """
    This mixin parses the contents of the post request and updates internal caches
    """

    def __init__(self, *args, **kwargs):
        super(ParseMixin, self).__init__(*args, **kwargs)

    def parse_post(self):
        """
        Parse contents of post request and update internal caches
        """
        ctype, pdict = parse_header(self.headers['content-type'])

        if ctype == 'multipart/form-data':
            self._form = FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': self.headers['Content-Type'],
                }
            )
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            self._postvars = parse_qs(self.rfile.read(length), keep_blank_values=True)
        else:
            raise RuntimeError
