import json
import os
import re
from typing import Dict
from webbrowser import get


def get_files(directory: str) -> None:
    """
    get_files Gets the spam and ham files and puts them into a json file in the root directory.

    Args:
        directory (str): _description_
    """
    enron1_path = os.path.join(os.path.dirname(__file__), directory)
    # gets ham directory
    ham_dir = os.path.join(enron1_path, 'ham')
    # gets spam directory
    spam_dir = os.path.join(enron1_path, 'spam')
    # regular expression to filter for in spam files.
    find_by = re.compile(r'[A-Za-z$]+[0-9]?')

    # Finds Spam Words
    os.chdir(spam_dir)
    spam = {}
    for f in os.listdir(spam_dir):
        with open(f, 'r', errors='ignore') as f:
            print(f)
            for word in re.findall(find_by, f.read()):
                # puts word into spam dictionary.
                spam[word] = spam.get(word, 0) + 1

    # Finds Ham Words
    os.chdir(ham_dir)
    ham = {}
    for f in os.listdir(ham_dir):
        with open(f, 'r', errors='ignore') as f:
            print(f)
            for word in re.findall(find_by, f.read()):
                # puts word into ham dictionary.
                ham[word] = ham.get(word, 0) + 1

    # changes directory to same path as file.
    os.chdir(os.path.dirname(__file__))
    # write json files
    with open(f'ham_{directory}.json', 'w') as f:
        json.dump(ham, f)
    with open(f'spam_{directory}.json', 'w') as f:
        json.dump(spam, f)
