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
            contents = uut.get_fs_contents()

            # Then
            self.assertEqual((
                bidict.bidict(), bidict.bidict({
                    'test0': '6968a3798f1eaa7a1e2aa9418c8beb8e261dfeef',
                    'folder0/test1': '72e26403288b64570b5f49e1393d7ba415ddedad'}
                )
            ), contents)

            # And when
            asyncio.run(uut.scan_fs_contents())
            contents = uut.get_fs_contents()

            # Then
            self.assertEqual((
                bidict.bidict({
                    'test0': '6968a3798f1eaa7a1e2aa9418c8beb8e261dfeef',
                    'folder0/test1': '72e26403288b64570b5f49e1393d7ba415ddedad'}),
                bidict.bidict({
                    'test0': '6968a3798f1eaa7a1e2aa9418c8beb8e261dfeef',
                    'folder0/test1': '72e26403288b64570b5f49e1393d7ba415ddedad'}
                )
            ), contents)

            # And when
            mock_read.side_effect = mock.mock_open(read_data=b'changed text')
            asyncio.run(uut.scan_fs_contents())
            contents = uut.get_fs_contents()

            # Then
            self.assertEqual((
                bidict.bidict({
                    'test0': '6968a3798f1eaa7a1e2aa9418c8beb8e261dfeef',
                    'folder0/test1': '72e26403288b64570b5f49e1393d7ba415ddedad'}),
                bidict.bidict({
                    'test0': 'c136c2a7fcf59b20961b01f4e7ccd0cc6c6a3db3',
                    'folder0/test1': 'e97a5834941affe8eaf7fbdec8b6cc044a80ad34'}
                )
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
