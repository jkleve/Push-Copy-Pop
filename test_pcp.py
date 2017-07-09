import pcp

import sys
import unittest

class TestPush(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pcp.empty_stack()

    def test_file_does_not_exist(self):
        sys.argv.append("push")
        sys.argv.append("LICENSE")
        pcp._ArgsHandler.push()
        self.assertEqual(len(pcp._stack), 1)


if __name__ == "__main__":
    unittest.main()
