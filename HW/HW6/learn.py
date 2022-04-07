import json
import os
import re
import time
from typing import Dict


def get_words(directory: str, find_by: re.Pattern, output_file: str) -> None:
    """
    get_files Gets the spam and ham words from the files, and puts them into a json file in the root directory.

    Args:
        directory (str): Directory where the spam and ham files should be.
        find_by (re.Pattern): Regular expression to match the words by.
        output_file (str): File to write the spam and ham json to.
    """
    enron1_path = os.path.join(os.path.dirname(__file__), directory)
    # gets ham directory
    ham_dir = os.path.join(enron1_path, 'ham')
    # gets spam directory
    spam_dir = os.path.join(enron1_path, 'spam')
    # regular expression to filter for in spam files.

    # Finds Spam Words
    os.chdir(spam_dir)
    spam = {}
    total_spam_files = 0
    print("Reading Spam files")
    time.sleep(1)
    for f in os.listdir(spam_dir):
        with open(f, 'r', errors='ignore') as f:
            print(f'Reading {f.name}')
            for word in re.findall(find_by, f.read()):
                # puts word into spam dictionary.
                spam[word] = spam.get(word, 0) + 1
        total_spam_files += 1
    # total number of words in spam files.
    spam['total_words'] = sum([value for value in spam.values()])
    # total spam files read
    spam['total_files'] = total_spam_files
    # Finds Ham Words
    os.chdir(ham_dir)
    ham = {}
    print("Reading Ham files")
    time.sleep(1)
    total_ham_files = 0
    for f in os.listdir(ham_dir):
        with open(f, 'r', errors='ignore') as f:
            print(f'Reading {f.name}')
            for word in re.findall(find_by, f.read()):
                # puts word into ham dictionary.
                ham[word] = ham.get(word, 0) + 1
        total_ham_files += 1
    # total number of words in ham files.
    ham['total_words'] = sum([value for value in ham.values()])
    # total ham files read
    ham['total_files'] = total_ham_files
    # puts ham and spam into one dictionary.
    knowledge = {"ham": ham, "spam": spam}
    del(ham)
    del(spam)
    # changes directory to same path as file.
    os.chdir(os.path.dirname(__file__))
    # write json files
    with open(str(output_file), 'w') as f:
        json.dump(knowledge, f)
