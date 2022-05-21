from os import walk
from binary2strings import binary2strings

# This script is used to generate the known_strings.h file.
paths = [
    "C:\\Windows\\",
    "C:\\Program Files\\",
    "C:\\Program Files (x86)\\",
    "C:\\ProgramData\\",
]

filenames_processed = {} # Only count files once
strings_db = {}

for path in paths:
    # Iterate directory
    for (dir_path, dir_names, file_names) in walk(path):
        for file in file_names:
            # Only process each filename once to better represent how common strings are
            if file not in filenames_processed:

                # Process this file
                print(dir_path + "\\" + file)
                try:
                    with open(dir_path + "\\" + file, "rb") as f:
                        data = f.read()
                except:
                    continue # Lacking permissions usually
                
                result = binary2strings.extract_all_strings(data)
                filenames_processed[file] = True

                # Add to database
                for (string, type, span) in result:
                    if string in strings_db:
                        strings_db[string] += 1
                    else:
                        strings_db[string] = 1

                print("Processed " + dir_path + "\\" + file + " (" + str(len(result)) + " strings)")