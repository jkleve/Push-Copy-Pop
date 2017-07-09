import pcp

import sys
import unittest


class TestPush(unittest.TestCase):
    def setUp(self):
        print("\n================")
        print("Testing {}".format(self.id()))
        pcp.empty_stack()
        sys.argv.append("push")

    def tearDown(self):
        pcp.empty_stack()
        del sys.argv[1:]
        print("Done testing {}".format(self.id()))
        print("================")

    def test_file_does_not_exist(self):
        sys.argv.append("LICENSES")
        pcp._ArgsHandler.push()
        self.assertEqual(len(pcp._stack), 0)

    def test_file_with_period(self):
        sys.argv.append("./LICENSE")
        pcp._ArgsHandler.push()
        self.assertEqual(len(pcp._stack), 1)

    def test_file_with_double_period(self):
        sys.argv.append("../Push-Copy-Pop/LICENSE")
        pcp._ArgsHandler.push()
        self.assertEqual(len(pcp._stack), 1)

    def test_two_files(self):
        sys.argv.append("LICENSE README.md")
        pcp._ArgsHandler.push()
        self.assertEqual(len(pcp._stack), 2)


if __name__ == "__main__":
    unittest.main()
