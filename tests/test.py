import unittest
# import our `pybind11`-based extension module
import binary2strings
import os
import sys

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

    def test_min_chars(self):
        for min_chars in range(2,10):
            for test_string in ["a"*5, "한"*5]:
                for encoding in ["utf-8", "utf-16"]:
                    data = bytes(test_string, encoding)
                    
                    # Strip the BOM if present
                    if encoding == "utf-16":
                        data = data[2:]

                    description = f"min_chars={min_chars}, test_string={test_string}, encoding={encoding}, hex={data.hex()}"

                    # Test extraction of single strings
                    result = binary2strings.extract_all_strings(data, min_chars=min_chars)
                    if min_chars <= 5:
                        self.assertEqual(result[0][0], test_string, description)
                    else:
                        self.assertEqual(len(result), 0, description)

                    # Same test for extract_string
                    result = binary2strings.extract_string(data, min_chars=min_chars)
                    if min_chars <= 5:
                        self.assertEqual(result[0], test_string, description)
                    else:
                        self.assertEqual(result[0], "", description)
    
    def test_corner_cases(self):
        string = b"0000000000"
        result = binary2strings.extract_all_strings(string)
        self.assertEqual(len(result), 1, f"result={result}")

        for min_chars in [1,2,10,1000]:
            # String of nulls
            string = b"\x00\x00\x00\x00\x00"
            result = binary2strings.extract_all_strings(string, min_chars=min_chars)
            self.assertEqual(len(result), 0, f"min_chars={min_chars}, result={result}")
            result = binary2strings.extract_string(string, min_chars=min_chars)
            self.assertEqual(len(result[0]), 0, f"min_chars={min_chars}, result={result}")

            string = b"\x00"
            result = binary2strings.extract_all_strings(string, min_chars=min_chars)
            self.assertEqual(len(result), 0, f"min_chars={min_chars}, result={result}")
            result = binary2strings.extract_string(string, min_chars=min_chars)
            self.assertEqual(len(result[0]), 0, f"min_chars={min_chars}, result={result}")

            # Empty string
            string = b""
            result = binary2strings.extract_all_strings(string, min_chars=min_chars)
            self.assertEqual(len(result), 0, f"min_chars={min_chars}, result={result}")
            result = binary2strings.extract_string(string, min_chars=min_chars)
            self.assertEqual(len(result[0]), 0, f"min_chars={min_chars}, result={result}")

            # Short string
            string = b"aa"
            result = binary2strings.extract_all_strings(string, min_chars=min_chars)
            if min_chars <= 2:
                self.assertEqual(len(result), 1, f"min_chars={min_chars}, result={result}")
            else:
                self.assertEqual(len(result), 0, f"min_chars={min_chars}, result={result}")
            
            # Single character test
            for string in ['a', "한"]:
                for encoding in ["utf-8", "utf-16"]:
                    data = bytes(string, encoding)
                    result = binary2strings.extract_all_strings(data, min_chars=min_chars)
                    if min_chars <= 1:
                        self.assertEqual(len(result), 1, f"min_chars={min_chars}, result={result}")
                    else:
                        self.assertEqual(len(result), 0, f"min_chars={min_chars}, result={result}")
                    
                    # Strip the BOM if present
                    if encoding == "utf-16":
                        data = data[2:]
                    
                    result = binary2strings.extract_string(data, min_chars=min_chars)
                    if min_chars <= 1:
                        self.assertEqual(len(result[0]), 1, f"min_chars={min_chars}, result={result}")
                    else:
                        self.assertEqual(len(result[0]), 0, f"min_chars={min_chars}, result={result}")

    @unittest.skipIf(sys.platform != "win32", "requires Windows")
    def test_bulk_files(self):
        # Extract strings from exe's in %windir% to test for crashes
        N_FILES = 200 # Number of exe's to extract strings from for testing
        n_files = 0
        n_strings = 0
        for root, dirs, files in os.walk(os.environ["windir"]):
            for file in files:
                if file.endswith(".exe"):
                    path = os.path.join(root, file)
                    with open(path, "rb") as f:
                        data = f.read()
                    result = binary2strings.extract_all_strings(data)
                    self.assertGreater(len(result), 0, path)

                    n_files += 1
                    n_strings += len(result)
                    if n_files >= N_FILES:
                        # Actual value locally: 1,583,765
                        self.assertGreater(n_strings, 800000, "Not enough strings extracted")
                        return
        
        self.assertEqual(True, False, "Not enough files tested")



if __name__ == '__main__':
    unittest.main()