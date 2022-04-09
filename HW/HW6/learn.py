import json
import os
import re
import time


def get_words(directory: str, find_by: re.Pattern, output_file: str) -> None:
    """
    get_files Gets the spam and ham words from the files, and puts them into a json file in the root directory.

    Args:
        directory (str): Directory where the spam and ham files should be.
        find_by (re.Pattern): Regular expression to match the words by.
        output_file (str): File to write the spam and ham json to.
    """
    # binds root path with email directory.
    email_path = os.path.join(os.path.dirname(__file__), directory)
    # gets ham directory.
    ham_path = os.path.join(email_path, 'ham')
    # gets spam directory.
    spam_path = os.path.join(email_path, 'spam')
    unique_words = 0
    # changes directory to spam path.
    os.chdir(os.path.dirname(__file__))
    # declares empty spam/ham directory.
    spam = {}
    ham = {}
    # counts number of spam/ham files.
    total_spam_files = 0
    total_ham_files = 0
    # if knowledge exists..., add it to the spam
    if output_file in os.listdir():
        with open(output_file, 'r') as knowledge_file:
            knowledge = json.load(knowledge_file)
            spam = knowledge['spam']
            ham = knowledge['ham']
            total_spam_files = spam['total_files']
            total_ham_files = ham['total_files']
    print("Reading Spam files...")
    time.sleep(1)
    # for each spam file...
    os.chdir(spam_path)
    for filename in os.listdir(spam_path):
        # open file
        with open(filename, 'r', errors='ignore') as spam_file:
            # find all words in file.
            for word in re.findall(find_by, spam_file.read()):
                # checks if word is in current knowledge dictionary.
                if word not in spam or word not in ham:
                    unique_words += 1
                # puts word into spam dictionary.
                spam[word] = spam.get(word, 0) + 1
        total_spam_files += 1
    spam['total_files'] = spam.get('total_files', 0) + total_spam_files

    # Finds Ham Words
    os.chdir(ham_path)
    print("Reading Ham files...")
    time.sleep(1)
    # for each ham file...
    for filename in os.listdir(ham_path):
        # open file
        with open(filename, 'r', errors='ignore') as spam_file:
            # find all words in file.
            for word in re.findall(find_by, spam_file.read()):
                # checks if word is in current knowledge dictionary.
                if word not in spam or word not in ham:
                    unique_words += 1
                # puts word into ham dictionary.
                ham[word] = ham.get(word, 0) + 1
        total_ham_files += 1
    # total ham files read
    ham['total_files'] = ham.get('total_files', 0) + total_ham_files
    # puts ham and spam into one dictionary.
    knowledge = {"ham": ham, "spam": spam, 'unique_words': unique_words}
    del(ham)
    del(spam)
    # changes directory back to the same path as this file.
    os.chdir(os.path.dirname(__file__))
    # write json files
    with open(str(output_file), 'w') as spam_file:
        json.dump(knowledge, spam_file)
