# binary2strings - Python module to extract strings from binary blobs
Python module to extract Ascii, Utf8, and wide strings from binary data. Supports Unicode characters. Fast wrapper around c++ compiled code. This is designed to extract strings from binary content such as compiled executables.

Supported extracting strings of formats:
* Utf8 (8-bit Unicode variable length characters)
* Wide-character strings (UCS-2 Unicode fixed 16-bit characters)

International language string extraction is supported for both Utf8 and wide-character string standards - for example Chinese simplified, Japanese, and Korean strings will be extracted.

Optionally uses a machine learning model to filter out erroneous junk strings.

## Installation
Recommended installation method:
```
pip install binary2strings
```

Alternatively, download the repo and run:
```
python setup.py install
```

## Documentation

Api:
```python
import binary2strings as b2s

[(string, encoding, span, is_interesting),] =
    b2s.extract_all_strings(buffer, min_chars=4, only_interesting=False)
```
Parameters:

* **buffer:**
A bytes array to extract strings from. All strings within this buffer will be extracted.
* **min_chars:**
(default 4) Minimum number of characters in a valid extracted string. Recommended minimum 4 to reduce noise.
* **only_interesting:** Boolean on whether only interesting strings should be returned. Interesting strings are non-gibberish strings, and a lightweight machine learning model is used for this identification. This will filter out the vast majority of junk strings, with a low risk of filtering out strings you care about.


Returns an array of tuples ordered according to the order in which they are located in the binary:
* **string:** The resulting string that was extracted in standard python string. All strings are converted to Utf8 here.
* **encoding:** "UTF8" | "WIDE_STRING". This is the encoding of the original string within the binary buffer.
* **span:** (start, end) tuple describing byte indices of where the string starts and ends within the buffer.
* **is_interesting:** Boolean describing whether the string is likely interesting. An interesting string is defined as non-gibberish. A machine learning model is used to compute this flag.

## Example usages

Example usage:
```python
import binary2strings as b2s

data = b"hello world\x00\x00a\x00b\x00c\x00d\x00\x00"
result = b2s.extract_all_strings(data, min_chars=4)
print(result)
# [
#   ('hello world', 'UTF8', (0, 10), True),
#   ('abcd', 'WIDE_STRING', (13, 19), False)
# ]
```

It also supports international languages, eg:
```python
import binary2strings as b2s

# "hello world" in Chinese simplified
string = "\x00世界您好\x00"
data = bytes(string, 'utf-8')

result = b2s.extract_all_strings(data, min_chars=4)
print(result)
# [
#   ('世界您好', 'UTF8', (1, 12), False)
# ]
```

Example extracting all strings from a binary file:
```python
import binary2strings as b2s

with open("C:\\Windows\\System32\\cmd.exe", "rb") as i:
    data = i.read()
    for (string, type, span, is_interesting) in b2s.extract_all_strings(data):
        print(f"{type}:{is_interesting}:{string}")
```


Example extracting only interesting strings from a binary file:
```python
import binary2strings as b2s

with open("C:\\Windows\\System32\\cmd.exe", "rb") as i:
    data = i.read()
    for (string, type, span, is_interesting) in b2s.extract_all_strings(data, only_interesting=True):
        print(f"{type}:{is_interesting}:{string}")
```
