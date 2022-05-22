from binary2strings import binary2strings

with open("C:\\Windows\\System32\\cmd.exe", "rb") as i:
    data = i.read()
    
    # Print only the uncommon string results
    print("--- Uncommon strings ----")
    for (string, type, span, is_uncommon) in binary2strings.extract_all_strings(data, only_uncommon=True):
        print(f"{type}:{string}")

    # Get all strings, and only print the common string results
    print("--- Common strings ----")
    for (string, type, span, is_uncommon) in binary2strings.extract_all_strings(data):
        if not is_uncommon:
            print(f"{type}:{string}")

