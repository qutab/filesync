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
        self._parser = argparse.ArgumentParser(description='file sync client')
        self._parser.add_argument('--path', type=dir_path)
        self._args = self._parser.parse_args()

    def get_target_path(self):
        return self._args.path

