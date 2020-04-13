import hashlib
from os import walk
import pathlib


class DirMonitor:
    """
    This class monitors all files and folders in the given directory
    periodically and notifies that sync is needed if checksum changes
    """
    def __init__(self, target_path=pathlib.Path.cwd()):
        self._path = target_path
        self._checksum = hashlib.sha1()
        self._fsitemlist = []

        if self._path.exists():
            if self._path.is_dir():
                scanned_dirs = walk(self._path)
                for item in scanned_dirs:
                    dirpath, dirnames, filenames = item

                    # Empty folder should affect the checksum also
                    if len(dirnames) == 0 and len(filenames) == 0:
                        self._fsitemlist.append(pathlib.Path(dirpath))
                        self._checksum.update(str(dirpath).encode())
                        assert pathlib.Path(dirpath).is_dir()

                    self._update_checksum(self._checksum, dirpath, filenames)

            elif self._path.is_file():
                self._update_checksum(self._checksum, self._path.parent, self._path.name)

    def get_checksum(self):
        return self._checksum.hexdigest()

    def is_checksum_changed(self):
        pass

    def get_fsitem_list(self):
        return self._fsitemlist

    def _update_checksum(self, checksum, dirname, filenames):
        for filename in sorted(filenames):
            fsitem = pathlib.Path(dirname).joinpath(pathlib.Path(filename))
            self._fsitemlist.append(fsitem)

            if fsitem.is_file():
                checksum.update(str(fsitem).encode())

                fh = open(fsitem, 'rb')
                while 1:
                    buf = fh.read(4096)
                    if not buf:
                        break
                    checksum.update(buf)
                fh.close()
