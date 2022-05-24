from genericpath import isfile
from os import walk
from binary2strings import binary2strings
import json
import random

def build_string_counts(paths, sampling_per_group=1000):
    filenames_processed = {} # Only count files once
    strings_db = {}

    for path in paths:
        # Iterate directory
        files = []
        for (dir_path, dir_names, file_names) in walk(path):
            for file in file_names:
                # Only process each filename once to better represent how common strings are
                if file not in filenames_processed:
                    files.append(dir_path + "\\" + file)
                    filenames_processed[file] = True
        files = random.sample(files, min(sampling_per_group, len(files)))

        print(f"Processing {len(files)} files in {path}...")

        for i, file in enumerate(files):
            # Process this file
            try:
                with open(file, "rb") as f:
                    data = f.read()
            except:
                continue # Lacking permissions usually
            
            result = binary2strings.extract_all_strings(data)

            # Set of strings already added for this file
            strings_processed_this_file = {}

            # Must contain at least 10 strings, mostly a filter to exclude all-string files
            if len(result) >= 10:
                for (string, type, span, is_interesting) in result:
                    # Maximum size for strings
                    if len(string) < 4000:
                        # Only count a string once from a single file
                        if string not in strings_processed_this_file:
                            strings_processed_this_file[string] = True

                            if string in strings_db:
                                strings_db[string] += 1
                            else:
                                strings_db[string] = 1

            print(f"progress={i} of {len(files)}, total_strings={len(strings_db)}, strings_in_file={len(result)}, {file}")
    
    return strings_db


if __name__ == '__main__':
    # This script is used to generate the strings_db.json string profile database
    paths = [
        "C:\\Windows\\",
        "C:\\Program Files\\",
        "C:\\Program Files (x86)\\",
        "C:\\ProgramData\\",
    ]


    strings_db = build_string_counts(paths, sampling_per_group=10000)

    # Write the strings db to a json file
    with open("strings_db.json", "w") as f:
        json.dump(strings_db, f)
    print(f"Wrote {len(strings_db)} strings to known_strings.json")
