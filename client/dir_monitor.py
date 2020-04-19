import hashlib
import os
import pathlib
import logging


class DirMonitor:
    """
    This class monitors all files and folders in the given directory
    periodically and notifies that sync is needed if checksum changes
    """

    def __init__(self, target_path: pathlib.Path = pathlib.Path.cwd()):
        self._path = pathlib.Path(target_path)
        self._fsitems_prev = {}
        self._fsitems_curr = {}

    async def scan_fs_contents(self):
        """
        The function scans contents of the given directory and
        calculates checksums of each file.
        """
        self._fsitems_prev = self._fsitems_curr.copy()
        self._fsitems_curr = {}

        if self._path.exists() and self._path.is_dir():
            scanned_dirs = os.walk(self._path)
            for dirpath, dirnames, filenames in scanned_dirs:
                logging.debug(f"scanned contents: {dirpath} {dirnames} {filenames}")

                # Empty folder should affect the checksum also
                is_empty_folder = len(dirnames) == 0 and len(filenames) == 0
                await self._update_checksum(dirpath, filenames, is_empty_folder)
        else:
            raise NotADirectoryError

    async def get_fs_contents(self):
        """
        :return: Pair of filename to checksum mapping.
        The first element is the mapping before the scan and the second one after the scan.
        """
        return self._fsitems_prev, self._fsitems_curr

    async def _update_checksum(self, dirname: str, filenames: list, is_empty_folder: bool):
        if is_empty_folder:
            assert pathlib.Path(dirname).is_dir()
            assert not filenames
            logging.warning("Empty folder are not synced currently...")

        for filename in sorted(filenames):
            checksum = hashlib.sha1()
            fsitem = pathlib.Path(dirname).joinpath(pathlib.Path(filename))
            assert fsitem.is_file()

            # Full path of the file also changes the checksum
            # This ensures that files with same contents have different checksums
            checksum.update(str(fsitem.as_posix()).encode())

            with open(fsitem, 'rb') as fh:
                while True:
                    buf = fh.read(4096)
                    if not buf:
                        break
                    checksum.update(buf)

            rel_path = fsitem.relative_to(self._path.as_posix())
            try:
                self._fsitems_curr[rel_path.as_posix()] = checksum.hexdigest()
            except Exception as exc:
                logging.error(f"Unhandled exception {exc}. Program may be in an unexpected state.")
