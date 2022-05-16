import unittest
# import our `pybind11`-based extension module from package python_cpp_example
from binary2strings import binary2strings

class MainTest(unittest.TestCase):
    def test_extract_ascii_unicode(self):
        # Test ASCII UTF8 and ASCII UNICODE parsing
        data = b"hello world\x00\x00a\x00b\x00c\x00d\x00\x00"
        result = binary2strings.extract_all_strings(data, 4)
        print(result) # [('hello world', 'UTF8', (0, 10)), ('abcd', 'UNICODE', (13, 19))]
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0], "hello world")
        self.assertEqual(result[0][1], "UTF8")
        self.assertEqual(result[1][0], "abcd")
        self.assertEqual(result[1][1], "UNICODE")

    def test_extract_utf(self):
        # Test UTF8 international language parsing
        string = "\x00世界您好\x00"
        data = bytes(string, 'utf-8')
        result = binary2strings.extract_all_strings(data, 4)
        print(result) # [('世界您好', 'UTF8', (1, 12))]
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "世界您好")
        self.assertEqual(result[0][1], "UTF8")

if __name__ == '__main__':
    unittest.main()