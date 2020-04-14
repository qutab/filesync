import unittest
from client.command_generator import *
import bidict


class TestCmdGenerator(unittest.TestCase):
    def test_cmd_generation(self):
        prev = bidict.bidict({'test0.txt': '4ba7c8fd29a627033119ac974f5e2103090d7cd1',
                              'emp/ppp.txt': 'ac7b67f2d1af092432684995b3eb4655db48e128',
                              'folder0/nested0.txt': '780198cb04890bd10d72411bdc73ee5473cec7c7',
                              'folder1/folder2/nested2.txt': '77073ff26f5e338e429178a742c12b4ba1f1c8b4',
                              'test1.txt': 'fb85be878a5dc10e3232c3c5a5ead0ed27690cb8'})

        curr = bidict.bidict({'test0.txt': '4ba7c8fd29a627033119ac974f5e2103090d7cd1',
                              'ppp1.txt': 'ac7b67f2d1af092432684995b3eb4655db48e128',
                              'folder0/nested0.txt': '780198cb04890bd10d72411bdc73ee5473cec7c7',
                              'folder1/folder2/nested2.txt': '942acbd126f5e338e429178a742c12b4ba1f1c8b4',
                              'test2.txt': 'c0b32bb1e0ef3fa928dcfcaa25f45584e64544a3'})

        expected = {
            'emp/ppp.txt': [Command.MOVE, 'ppp1.txt'],
            'folder1/folder2/nested2.txt': [Command.ADD],
            'test1.txt': [Command.DELETE],
            'test2.txt': [Command.ADD]
        }
        self.assertEqual(get_commands(prev, curr), expected)

    def test_files_with_same_contents(self):
        def _do_test(path1: str, path2: str):
            prev = bidict.bidict({path1: '4ba7c8fd29a627033119ac974f5e2103090d7cd1'})
            curr = bidict.bidict({path2: '4ba7c8fd29a627033119ac974f5e2103090d7cd1'})

            expected = {
                path1: [Command.MOVE, path2]
            }
            self.assertEqual(get_commands(prev, curr), expected)

        _do_test('same_contents.txt', 'different_name.txt')
        _do_test('same_name.txt', 'different_path/same_name.txt')


if __name__ == '__main__':
    unittest.main()
