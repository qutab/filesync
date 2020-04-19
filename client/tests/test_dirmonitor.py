import asyncio
import unittest
from unittest import mock

from client.dirmonitor import *


class TestDirMonitor(unittest.TestCase):
    def test_dir_monitor(self):
        # Given
        with mock.patch('os.walk') as mock_walk, \
                mock.patch.object(pathlib.Path, 'exists', return_value=True), \
                mock.patch.object(pathlib.Path, 'is_file', return_value=True), \
                mock.patch('builtins.open', mock.mock_open(read_data=b'test text')) as mock_read:
            mock_walk.return_value = [
                ('/', ('folder0',), ('test0',)),
                ('/folder0', (), ('test1',)),
            ]
            uut = DirMonitor(pathlib.Path(pathlib.Path('/')))

            # When
            asyncio.run(uut.scan_fs_contents())
            contents = asyncio.run(uut.get_fs_contents())

            # Then
            self.assertEqual((
                {}, {
                    'test0': 'f4d5d7de98c43a302f6ffe982dd143f7bc92afb7',
                    'folder0/test1': '8ca875d99ae8cb169aff5b36d15eb5de36ee20f0'}
            ), contents)

            # And when
            asyncio.run(uut.scan_fs_contents())
            contents = asyncio.run(uut.get_fs_contents())

            # Then
            self.assertEqual((
                {
                    'test0': 'f4d5d7de98c43a302f6ffe982dd143f7bc92afb7',
                    'folder0/test1': '8ca875d99ae8cb169aff5b36d15eb5de36ee20f0'},
                {
                    'test0': 'f4d5d7de98c43a302f6ffe982dd143f7bc92afb7',
                    'folder0/test1': '8ca875d99ae8cb169aff5b36d15eb5de36ee20f0'}
            ), contents)

            # And when
            mock_read.side_effect = mock.mock_open(read_data=b'changed text')
            asyncio.run(uut.scan_fs_contents())
            contents = asyncio.run(uut.get_fs_contents())

            # Then
            self.assertEqual((
                {
                    'test0': 'f4d5d7de98c43a302f6ffe982dd143f7bc92afb7',
                    'folder0/test1': '8ca875d99ae8cb169aff5b36d15eb5de36ee20f0'},
                {
                    'test0': 'c5105adac8eff93dd7e94549fa116ae711826be1',
                    'folder0/test1': 'e49829a2b00c2d432c5301748255566c012cb9ab'}
            ), contents)

    def test_invalid_path(self):
        # Given
        with mock.patch('os.walk') as mock_walk, \
                mock.patch.object(pathlib.Path, 'exists', return_value=True) as mock_exist, \
                mock.patch.object(pathlib.Path, 'is_dir', return_value=False), \
                mock.patch('builtins.open', mock.mock_open(read_data=b'test text')):
            uut = DirMonitor(pathlib.Path(pathlib.Path('/test_file')))

            # When (path is a file) - Then
            self.assertRaises(NotADirectoryError, lambda: asyncio.run(uut.scan_fs_contents()))

            # When (path does not exist)
            mock_exist.return_value = False
            # Then
            self.assertRaises(NotADirectoryError, lambda: asyncio.run(uut.scan_fs_contents()))


if __name__ == '__main__':
    unittest.main()
