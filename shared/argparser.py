import argparse
import pathlib


def dir_path(string):
    path = pathlib.Path.cwd().joinpath(string).resolve()
    if path.is_dir():
        return path
    else:
        raise NotADirectoryError(string)


class Parser:
    def __init__(self):
        self._parser = argparse.ArgumentParser(description="file sync program")
        self._parser.add_argument("-p", "--path", help="directory path to be synced", type=dir_path)
        self._parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
        self._parser.add_argument("-c", "--compress", help="use compression", action="store_true")

        self._args = self._parser.parse_args()

    @property
    def target_path(self):
        return self._args.path

    @property
    def verbose(self):
        return self._args.verbose

    @property
    def compressed(self):
        return self._args.compress
