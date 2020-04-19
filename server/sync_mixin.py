import logging
from pathlib import Path
from shared import argparser
import zlib


class SyncMixin(object):
    """
    Helper mixin for handling filesystem commands received from the client
    """

    def __init__(self, *args, **kwargs):
        self._target_dir = argparser.Parser().target_path
        if not self._target_dir.exists() or not self._target_dir.is_dir():
            raise NotADirectoryError
        self._compressed = argparser.Parser().compressed

        super(SyncMixin, self).__init__(*args, **kwargs)

    def handle_delete(self):
        file_rel_path = self.post_vars[b'relative_path'][0].decode()
        abs_path = self._target_dir.joinpath(file_rel_path)
        try:
            abs_path.unlink(abs_path)
        except FileNotFoundError:
            logging.error(f"File {abs_path} not found on server.")
        else:
            logging.debug(f"File {abs_path} deleted.")

    def handle_add(self):
        if not self.post_form:
            logging.error("Failed to add file/folder.")
            return

        form_file = self.post_form['file']
        relative_path = Path(self.post_form.getvalue('relative_path'))

        if form_file.file and relative_path:
            # Ensure file directory exists
            full_path = self._target_dir.joinpath(relative_path).absolute()
            Path(full_path.parent).mkdir(parents=True, exist_ok=True)

            # Write file contents
            if self._compressed:
                contents = zlib.decompress(form_file.file.read())
            else:
                contents = form_file.file.read()

            open(full_path, 'wb').write(contents)
            logging.debug(f"File {full_path} saved successfully!")
        else:
            logging.error("Failed to add file/folder.")

    def handle_update(self):
        # For now just update the whole file
        self.handle_add()
