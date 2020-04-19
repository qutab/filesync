import unittest
from client.command_generator import *


class TestCmdGenerator(unittest.TestCase):
    def test_cmd_generation(self):
        prev = {'test0.txt': '4ba7c8fd29a627033119ac974f5e2103090d7cd1',
                'emp/ppp.txt': '8a92bff2d1af092432684995b3eb4655db48e128',
                'folder0/nested0.txt': '780198cb04890bd10d72411bdc73ee5473cec7c7',
                'folder1/folder2/nested2.txt': '77073ff26f5e338e429178a742c12b4ba1f1c8b4',
                'test1.txt': 'fb85be878a5dc10e3232c3c5a5ead0ed27690cb8'}

        curr = {'test0.txt': '4ba7c8fd29a627033119ac974f5e2103090d7cd1',
                'ppp1.txt': 'ac7b67f2d1af092432684995b3eb4655db48e128',
                'folder0/nested0.txt': '780198cb04890bd10d72411bdc73ee5473cec7c7',
                'folder1/folder2/nested2.txt': '942acbd126f5e338e429178a742c12b4ba1f1c8b4',
                'test2.txt': 'c0b32bb1e0ef3fa928dcfcaa25f45584e64544a3'}

        expected = {
            'emp/ppp.txt': [Command.DELETE],
            'ppp1.txt': [Command.ADD],
            'folder1/folder2/nested2.txt': [Command.UPDATE],
            'test1.txt': [Command.DELETE],
            'test2.txt': [Command.ADD]
        }
        self.assertEqual(get_commands(prev, curr), expected)

    def test_files_with_same_checksum(self):
        prev = {"path1": '4ba7c8fd29a627033119ac974f5e2103090d7cd1'}
        curr = {"path2": '4ba7c8fd29a627033119ac974f5e2103090d7cd1'}

        self.assertRaises(AssertionError, lambda: get_commands(prev, curr))


if __name__ == '__main__':
    unittest.main()
