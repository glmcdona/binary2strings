import unittest
# import our `pybind11`-based extension module
import binary2strings

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

    def test_two_languages(self):
        # Test that a transition between two languages aborts for a WIDE_STRING
        string = "\x0f世界您好\x00Привет, мир\x0f"
        data = bytes(string, 'utf_16')
        result = binary2strings.extract_all_strings(data)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0], "世界您好")
        self.assertEqual(result[1][0], "Привет, мир")

    def test_utf8_three_byte_decoding(self):
        # Test extraction of three byte character utf8
        data = b"\xe0\xa4\xb9\xe0\xa4\xb9\xe0\xa4\xb9\xe0\xa4\xb9"
        result = binary2strings.extract_string(data, min_chars=2)
        self.assertEqual(result[0], "हहहह")

        data = b"\xe2\x82\xac\xe2\x82\xac\xe2\x82\xac\xe2\x82\xac"
        result = binary2strings.extract_string(data, min_chars=2)
        self.assertEqual(result[0], "€€€€")

        data = b"\xed\x95\x9c\xed\x95\x9c\xed\x95\x9c\xed\x95\x9c"
        result = binary2strings.extract_string(data, min_chars=2)
        self.assertEqual(result[0], "한한한한")

    def test_utf8_three_byte_overlong(self):
        # Test extraction of three byte character utf8
        data = b"\xe0\x81\x81\xe0\x81\x81\xe0\x81\x81\xe0\x81\x81" # "AAAA" in overlong format
        result = binary2strings.extract_string(data, min_chars=2)
        self.assertEqual(result[0], "")

    def test_is_interesting(self):
        interesting_strings = ["error","DllGetActivationFactory","NtOpenFile","magic_number"]
        not_interesting_strings = ["xQVV","|$ UATAUAVAWH","XXX8Pvh8v"]

        # Test not interesting strings
        for string in not_interesting_strings:
            data = bytes(string, 'utf-8')
            result = binary2strings.extract_all_strings(data)
            self.assertEqual(len(result), 1, str(result) + " - " + string)
            self.assertEqual(result[0][3], False, str(result) + " - " + string)

            data = bytes(string, 'utf-16')
            result = binary2strings.extract_all_strings(data)
            self.assertEqual(len(result), 1, str(result) + " - " + string)
            self.assertEqual(result[0][3], False, str(result) + " - " + string)
        
        # Test interesting strings
        for string in interesting_strings:
            data = bytes(string, 'utf-8')
            result = binary2strings.extract_all_strings(data)
            self.assertEqual(len(result), 1, str(result) + " - " + string)
            self.assertEqual(result[0][3], True, str(result) + " - " + string)

            data = bytes(string, 'utf-16')
            result = binary2strings.extract_all_strings(data)
            self.assertEqual(len(result), 1, str(result) + " - " + string)
            self.assertEqual(result[0][3], True, str(result) + " - " + string)

        # Test only returning interesting strings
        string = "\x00".join(interesting_strings*10 + not_interesting_strings*10)
        data = bytes(string, 'utf-8')
        result = binary2strings.extract_all_strings(data, only_interesting=True)
        self.assertGreaterEqual(len(result), len(interesting_strings)*10*0.9)
        for i in range(len(interesting_strings)):
            self.assertEqual(result[i][0], interesting_strings[i])
            self.assertEqual(result[i][3], True)



if __name__ == '__main__':
    unittest.main()