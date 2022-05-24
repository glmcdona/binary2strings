from genericpath import isfile
import json
import pickle
import random
import os
import re

if __name__ == '__main__':
    # This script leverages a GitHub dump to create a database of string constants. This is
    # used to train a model to identify strings that are likely to be interesting.
    # To download the dump, see:
    #   https://github.com/EleutherAI/github-downloader
    # This outputs "github_constants.json"

    file_exts = ["cpp", "cs", "h", "py", "c", "lua", "cc", "swift", "vbs"]

    # Gather all files matching theses extensions
    path = "./../github-downloader/output/"
    files = []
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            if filename.split(".")[-1].lower() in file_exts:
                files.append(os.path.join(root, filename))
    
    print(f"Found {len(files)} files")

    # Take a random sample of files
    files_sample = random.sample(files, min(500000, len(files)))

    # Extract string constants from the files
    strings_db = {}
    filenames = {}
    for i, file in enumerate(files_sample):
        if i % 1000 == 0:
            print(f"Processing file {i}/{len(files_sample)}: {file}")
        
        if file.lower() not in filenames:
            filenames[file.lower()] = True

            #print(f"Processing {file}...")
            with open(file, "r", encoding="utf-8") as f:
                try:
                    for line in f:
                        # Handle single an double quotes
                        r1 = re.findall(r"'(.*?)'", line, re.DOTALL)
                        r2 = re.findall(r"\"(.*?)\"", line, re.DOTALL)
                        for string in r1 + r2:
                            if len(string) < 100 and len(string) >= 4:
                                #print(f"Found string: {string}, Line: {line}")

                                if string in strings_db:
                                    strings_db[string] += 1
                                else:
                                    strings_db[string] = 1
                                
                                string_normalized = string.replace("\\r","\r").replace("\\n","\n")
                                if string_normalized != string:
                                    if string_normalized in strings_db:
                                        strings_db[string_normalized] += 1
                                    else:
                                        strings_db[string_normalized] = 1
                except:
                    pass # Utf-8 decode error usually

    print(f"Found {len(strings_db)} strings")

    # Write it to a json
    with open("github_constants.json", "w") as f:
        json.dump(strings_db, f)