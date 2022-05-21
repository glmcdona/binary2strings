# binary2strings - Python module to extract strings from binary blobs
Work-in-progress python module to extract Ascii, Utf8, and wide strings from binary data. Supports Unicode characters. Fast wrapper around c++ compiled code.

Supported string formats:
* Utf8 (8-bit Unicode variable length characters)
* Wide-character strings (UCS-2 Unicode fixed 16-bit characters)

International language string extraction is supported for both Utf8 and wide-character string standards.

Example usage:
```python
from binary2strings import binary2strings

data = b"hello world\x00\x00a\x00b\x00c\x00d\x00\x00"
result = binary2strings.extract_all_strings(data, min_chars=4)
print(result)
# [('hello world', 'UTF8', (0, 10)), ('abcd', 'WIDE_STRING', (13, 19))]
```

It also supports international languages, eg:
```python
from binary2strings import binary2strings

string = "\x00世界您好\x00"
data = bytes(string, 'utf-8')

result = binary2strings.extract_all_strings(data, min_chars=4)
print(result)
# [('世界您好', 'UTF8', (1, 12))]
```