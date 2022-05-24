from binary2strings import binary2strings

with open("C:\\Windows\\System32\\cmd.exe", "rb") as i:
    data = i.read()
    
    # Write and print all results
    with open("cmd.exe.txt", "w", encoding="utf-8") as o:
        for (string, type, span, is_interesting) in binary2strings.extract_all_strings(data):
            print(f"{type}:{is_interesting}:{string}")
            o.write(f"{type}:{is_interesting}:{string}\n")

    # Write only the interesting string results
    with open("cmd.exe.interesting.txt", "w", encoding="utf-8") as o:
        for (string, type, span, is_interesting) in binary2strings.extract_all_strings(data, only_interesting=True):
            o.write(f"{string}\n")

    # Write only the not interesting string results
    with open("cmd.exe.not_interesting.txt", "w", encoding="utf-8") as o:
        for (string, type, span, is_interesting) in binary2strings.extract_all_strings(data):
            if not is_interesting:
                o.write(f"{string}\n")
