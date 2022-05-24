from binary2strings import binary2strings
import os
import pandas as pd
import random

if __name__ == "__main__":
    # Creates csv files for manual grading of interesting strings.
    
    # Gather all files in
    paths = [
        "C:\\Windows\\",
        "C:\\Program Files\\",
        "C:\\Program Files (x86)\\",
    ]

    files = []
    for path in paths:
        files_in_path = []
        for (dir_path, dir_names, file_names) in os.walk(path):
            for file in file_names:
                if file.split(".")[-1].lower() in ["exe","dll"]:
                    # Only process large files
                    full_path = os.path.join(dir_path, file)
                    if os.path.getsize(full_path) > 1000000:
                        files_in_path.append(full_path)
    
        # Sample a few random files
        files_in_path = random.sample(files_in_path, min(10, len(files_in_path)))
        files.extend(files_in_path)

    # Process each file
    strings = []
    for file in files:
        # Process this file
        print(f"Processing {file}...")
        try:
            with open(file, "rb") as f:
                data = f.read()
        except:
            continue # Lacking permissions usually
        
        result = binary2strings.extract_all_strings(data)
        for (string, type, span, is_interesting) in result:
            strings.append(string)
    
    # Create dataframe with fixed target and strings
    df = pd.DataFrame(data={
            "target": [1.0]*len(strings),
            "string": strings
        }
    )

    # Save to csv for manual grading
    df["target"] = 1.0
    df.to_csv("data/ungraded_strings_interesting.csv", index=False)
    df["target"] = 0.0
    df.to_csv("data/ungraded_strings_not_interesting.csv", index=False)