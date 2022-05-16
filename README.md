# binary2strings - Python module to extract strings from binary blobs
Work-in-progress python module to extract Ascii, Utf8, and Unicode strings from binary data. Lightning fast wrapper around c++ compiled code.

Supported string formats:
* Utf8
* Unicode wide-character strings

International language string extraction is supported for both Utf8 and Unicode wide-character string format.

Example usage:
```python
from binary2strings import binary2strings

data = b"hello world\x00\x00a\x00b\x00c\x00d\x00\x00"
result = binary2strings.extract_all_strings(data, 4)
print(result) # [('hello world', 'UTF8', (0, 10)), ('abcd', 'UNICODE', (13, 19))]
```

It also supports international languages, eg:
```python
from binary2strings import binary2strings

string = "\x00世界您好\x00"
data = bytes(string, 'utf-8')

result = binary2strings.extract_all_strings(data, 4)
print(result) # [('世界您好', 'UTF8', (1, 12))]
```