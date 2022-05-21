import unittest
# import our `pybind11`-based extension module from package python_cpp_example
from binary2strings import binary2strings

class MainTest(unittest.TestCase):
    def test_extract_all_ascii_unicode(self):
        # Test ASCII UTF8 and ASCII UNICODE parsing
        data = b"hello world\x00\x00a\x00b\x00c\x00d\x00\x00"
        result = binary2strings.extract_all_strings(data)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0], "hello world")
        self.assertEqual(result[0][1], "UTF8")
        self.assertEqual(result[1][0], "abcd")
        self.assertEqual(result[1][1], "WIDE_STRING")

    def test_extract_all_utf(self):
        # Test UTF8 international language parsing
        string = "\x00世界您好\x00"
        data = bytes(string, 'utf-8')
        result = binary2strings.extract_all_strings(data)
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
        result = binary2strings.extract_all_strings(data, min_chars=10)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "此外，使用口头报告是教师可以应用的一项很棒的活动，同时将读写技能与任何学科领域联系起来（Altieri，2010，154）。因此，学生可能需要研究词源，或研究一个词在不同语义和历史背景下的具体应用")
        self.assertEqual(result[0][1], "UTF8")

    def test_extract_single(self):
        # Test extraction of single strings
        string = "世界您好\x0f"
        data = bytes(string, 'utf-8')
        result = binary2strings.extract_string(data, min_chars=4)
        self.assertEqual(result[0], "世界您好")
        self.assertEqual(result[1], "UTF8")

        string = "世界您好\x0f"
        data = bytes(string, 'utf-8')
        result = binary2strings.extract_string(data, min_chars=6)
        self.assertEqual(result[0], "")

        string = "\x10世界您好\x0f"
        data = bytes(string, 'utf-8')
        result = binary2strings.extract_string(data, min_chars=2)
        self.assertEqual(result[0], "")
    
    def test_wide_char_international(self):
        # Test extraction of single strings
        string = "\x0f世界您好\x0f"
        data = bytes(string, 'utf_16')
        result = binary2strings.extract_all_strings(data, min_chars=4)
        self.assertEqual(result[0][0], "世界您好")
        # Note: Utf16 is a WIDE_STRING if characters are in basic multilingual plane
        self.assertEqual(result[0][1], "WIDE_STRING")

    def test_language_transition(self):
        # Test that a transition between two languages aborts for a WIDE_STRING
        string = "\x0f世界您好Привет, мир\x0f"
        data = bytes(string, 'utf_16')
        result = binary2strings.extract_all_strings(data)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0], "世界您好")
        self.assertEqual(result[1][0], "Привет, мир")

    def test_binary(self):
        # Test that a transition between two languages aborts for a WIDE_STRING
        with open("C:\\Windows\\System32\\cmd.exe", "rb") as f:
            data = f.read()
        result = binary2strings.extract_all_strings(data)
        print(len(result))
        print(result)
        #self.assertEqual(len(result), 2)
        #self.assertEqual(result[0][0], "世界您好")
        #self.assertEqual(result[1][0], "Привет, мир")



if __name__ == '__main__':
    unittest.main()