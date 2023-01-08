from genericpath import isfile
import json
import pickle
import random
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import *
from sklearn.metrics import classification_report, precision_score, recall_score, f1_score, precision_recall_fscore_support
from sklearn.linear_model import LogisticRegression
from scipy import sparse

if __name__ == '__main__':
    # Strings within this character range in length should
    # be processed by a model before they are considered
    # interesting. This is to filter out gibberish.
    min_chars = 4
    max_chars = 16
    sample_interesting = 2000000
    sample_not_interesting = 2000000

    # Load the string frequency database
    if not isfile("./data/train.csv"):
        # Create the training data

        # Load the string frequency database
        if not isfile("./data/strings_db.json"):
            raise Exception("No strings_db.json file found")

        print("Loading string count database...")
        with open("./data/strings_db.json", "r") as f:
            strings_db = json.load(f)
        print(f"Loaded {len(strings_db)} strings from strings_db.json")

        # Load the github string constant database
        if not isfile("./data/github_constants.json"):
            raise Exception("No github_constants.json file found")

        print("Loading string count database...")
        with open("./data/github_constants.json", "r") as f:
            github_constants = json.load(f)
        print(f"Loaded {len(github_constants)} strings from github_constants.json")

        # Build a list of of interesting strings based on github constants
        strings_interesting = []
        strings_interesting_fragments = {}
        for string, value in github_constants.items():
            if value >= 2:
                strings_interesting.append(string)

                # Add the shortened fragments
                for l in range(min_chars,max_chars): # Process strings of length 4 to 8
                    for j in range(0, len(string) - l):
                        fragment = string[j:j+l]
                        if len(fragment) >= min_chars and len(fragment) <= max_chars:
                            if fragment not in strings_interesting_fragments:
                                strings_interesting_fragments[fragment] = True
        print(f"Found {len(strings_interesting)} interesting strings")
        
        # Build a list of not-interesting strings based on strings_db
        strings_not_interesting = []
        for string in strings_db.keys():
            if( len(string) >= min_chars and len(string) <= max_chars and strings_db[string] <= 1 ):
                if string not in strings_interesting_fragments:
                    # Validate that no sub-strings are considered interesting
                    interesting = False
                    for i in range(min_chars,max_chars):
                        for n in range(0, len(string) - min_chars):
                            fragment = string[n:n+i]
                            if fragment in strings_interesting_fragments:
                                interesting = True
                                break
                    
                    if not interesting:
                        strings_not_interesting.append(string)
        print(f"Found {len(strings_not_interesting)} not-interesting strings")

        # Sample the strings
        strings_interesting_fragments_sampled = random.sample(strings_interesting_fragments.keys(), min(sample_interesting, len(strings_interesting_fragments)))
        strings_not_interesting_sampled = random.sample(strings_not_interesting, min(sample_not_interesting, len(strings_not_interesting)))
        print(f"Sampled {len(strings_interesting_fragments_sampled)} interesting and {len(strings_not_interesting_sampled)} not-interesting strings")

        # Now create the training dataframe
        print("Creating training dataframe...")
        df = pd.DataFrame(data={
                    "target": [1.0]*len(strings_interesting_fragments_sampled) + [0.0]*len(strings_not_interesting_sampled),
                    "string": strings_interesting_fragments_sampled + strings_not_interesting_sampled
                })
        
        # Write to disk
        print("Writing training dataframe 'train.csv'...")
        df.to_csv("./data/train.csv", index=False)
    
    # Train the model
    print("Training model...")

    # Load the training data
    print("Loading training data...")
    df = pd.read_csv("./data/train.csv")
    

    # Merge the training data with the manually graded training data
    print("Merging manually graded training data...")
    df_graded = pd.read_csv("./data/graded_strings_interesting.csv", error_bad_lines=False)
    df_graded.target = pd.to_numeric(df_graded.target,errors='coerce')
    df_graded = df_graded.dropna()
    df_graded.target = 1.0
    print(f"Loaded {len(df_graded)} manually interesting graded strings")

    df = df.append(df_graded)
    df_graded = pd.read_csv("./data/graded_strings_not_interesting.csv", error_bad_lines=False)
    df_graded.target = pd.to_numeric(df_graded.target,errors='coerce')
    print(f"Loaded {len(df_graded)} manually not interesting graded strings")

    df = df.append(df_graded)
    df.to_csv("./data/train_with_graded.csv", index=False)

    # Force the target to be numeric
    df["target"] = df["target"].astype(float)
    df = df.dropna()
    
    # Randomly sample the rows to speed up training
    print("Randomly sampling training data...")
    df = df.sample(frac=1.0)

    x_train, x_test, y_train, y_test = train_test_split(df["string"], df["target"], test_size=0.2, random_state=42)

    def character_ngram_counts(x):
        # Create a scipy.sparse array of character ngram counts
        # Feature format:
        #   118 character unigrams (character ranges 0x9 to 0x7e)
        #   118*118 character bigrams
        #   1 for the total number of characters in string
        #   1 for the total number of > 0x128 ascii code
        #   1 distinct character count
        csr = sparse.lil_matrix((len(x), 118+118+118*118+1+1+1), dtype=np.float32)

        # Count the character ngrams
        for i in range(0, len(x)):
            if i % 1000 == 0:
                print(f"Processing string {i} of {len(x)}")
            
            string = x[i]
            
            # Set the character count
            csr[i, 118 + 118 + 118*118 + 0] = len(string)

            # Set the distinct character count
            csr[i, 118 + 118 + 118*118 + 2] = len(set(string))

            # Unigram and bigram counts
            for j in range(0, len(string)):
                char_ord = ord(string[j])
                if char_ord >= 0x9 and char_ord <=  0x7E:
                    csr[i, char_ord-0x9] += 1
                    if j + 1 < len(string):
                        next_char_ord = ord(string[j+1])
                        if next_char_ord >= 0x9 and next_char_ord <=  0x7E:
                            csr[i, 118 + (char_ord-0x9) + 118*(next_char_ord-0x9) ] += 1
                else:
                    # Non-latin unicode character count
                    csr[i, 118 + 118 + 118*118 + 1] += 1
        
        return csr

    print("Character ngrams...")
    dataset = character_ngram_counts(x_train.tolist())

    # Preview the first few rows before and after featurization
    print(x_train.head(10))
    print(dataset[0:10])

    # Print the dataset statistics
    print(f"Dataset shape: {dataset.shape}")

    # Train sklearn Logistic Regression model
    print("Training sklearn Logistic Regression model...")
    model = LogisticRegression(solver='lbfgs', max_iter=3000)
    model.fit(dataset, y_train)

    # Print the model metrics on test data
    x_test_featurized = character_ngram_counts(x_test.tolist())
    y_preds = model.predict(x_test_featurized)
    print(classification_report(y_test, y_preds))
    print(f"Precision: {precision_score(y_test, y_preds)}")
    print(f"Recall: {recall_score(y_test, y_preds)}")
    print(f"F1: {f1_score(y_test, y_preds)}")

    # Export the bias and weights to a model.h file for use in C++
    print("Exporting model to model.h...")
    with open("string_model.hpp", "w") as f:
        f.write("#pragma once\n\n")
        f.write("namespace string_model {\n\n")
        f.write(f"\tconstexpr float bias = {model.intercept_[0]};\n")
        f.write("\tconstexpr float weights[118+118+118*118+1+1+1] = {\n\t\t")
        for i in range(0, 118+118+118*118+1+1+1):
            if i > 0:
                f.write(", ")
            if i % 16 == 15:
                f.write("\n\t\t")
            f.write("{:.6f}".format(model.coef_[0][i]))
        f.write("};\n")
        f.write("} // namespace string_model\n\n")

