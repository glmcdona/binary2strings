import unittest
# import our `pybind11`-based extension module from package python_cpp_example
from binary2strings import binary2strings

class MainTest(unittest.TestCase):
    def test_extract_all_ascii_unicode(self):
        # Test ASCII UTF8 and ASCII UNICODE parsing
        data = b"hello world\x00\x00a\x00b\x00c\x00d\x00\x00"
        result = binary2strings.extract_all_strings(data, 4)
        print(result) # [('hello world', 'UTF8', (0, 10)), ('abcd', 'WIDE_STRING', (13, 19))]
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0], "hello world")
        self.assertEqual(result[0][1], "UTF8")
        self.assertEqual(result[1][0], "abcd")
        self.assertEqual(result[1][1], "WIDE_STRING")

    def test_extract_all_utf(self):
        # Test UTF8 international language parsing
        string = "\x00世界您好\x00"
        data = bytes(string, 'utf-8')
        result = binary2strings.extract_all_strings(data, 4)
        print(result) # [('世界您好', 'UTF8', (1, 12))]
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "世界您好")
        self.assertEqual(result[0][1], "UTF8")
    
    def test_extract_all_utf2(self):
        # Generate 256 random bytes
        import random
        data = bytes(random.getrandbits(8) for _ in range(256))

        # Test UTF8 international language parsing
        string = "\x10此外，使用口头报告是教师可以应用的一项很棒的活动，同时将读写技能与任何学科领域联系起来（Altieri，2010，154）。因此，学生可能需要研究词源，或研究一个词在不同语义和历史背景下的具体应用\x00\x00"
        data += bytes(string, 'utf-8')
        result = binary2strings.extract_all_strings(data, 10)

        print(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "此外，使用口头报告是教师可以应用的一项很棒的活动，同时将读写技能与任何学科领域联系起来（Altieri，2010，154）。因此，学生可能需要研究词源，或研究一个词在不同语义和历史背景下的具体应用")
        self.assertEqual(result[0][1], "UTF8")

    def test_extract_single(self):
        # Test extraction of single strings
        string = "世界您好\x0f"
        data = bytes(string, 'utf-8')
        result = binary2strings.extract_string(data, 4)
        self.assertEqual(result[0], "世界您好")
        self.assertEqual(result[1], "UTF8")

        string = "世界您好\x0f"
        data = bytes(string, 'utf-8')
        result = binary2strings.extract_string(data, 6)
        self.assertEqual(result[0], "")

        string = "\x10世界您好\x0f"
        data = bytes(string, 'utf-8')
        result = binary2strings.extract_string(data, 2)
        self.assertEqual(result[0], "")



if __name__ == '__main__':
    unittest.main()