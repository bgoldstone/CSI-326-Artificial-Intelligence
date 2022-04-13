"""
    learns using the existing spam/ham files and gathers counts of how many words occur in total using the function get_knowledge().
    
    Name: Ben Goldstone
    Professor: Dr. Jorge Silveyra
    Date: 04/13/2022
"""
import json
import os
import re
import time
from typing import Dict, Tuple

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# ------------------------------------------------CONSTANTS----------------------------------
"""ENGLISH_STOPWORDS (Dict): Dictionary of stopwords for the english language."""
ENGLISH_STOPWORDS = set(stopwords.words('english'))

# adds 'subject' to stopwords
ENGLISH_STOPWORDS.add('subject')

"""LEMMATIZER (WordNetLemmatizer): object to lemmatize words"""
LEMMATIZER = WordNetLemmatizer()
# ---------------------------------------------END CONSTANTS--------------------------------


def __combine_into_one_dictionary(unique_words: int, spam: Dict[str, int], ham: Dict[str, int], total_ham_files: int, spam_lemmatization: Dict[str, int], ham_lemmatization: Dict[str, int], unique_words_lemmatization: int, spam_stopwords: Dict[str, int], ham_stopwords: Dict[str, int], unique_words_stopwords: int, spam_lemmatization_stopwords: Dict[str, int], ham_lemmatization_stopwords: Dict[str, int], unique_words_lemmatization_stopwords: int) -> Tuple[Dict[str, int], Dict[str, int], Dict[str, int], Dict[str, int]]:
    """
    combine_into_one_dictionary combine dictionaries into one dictionary to put into the json file

    Args:
        unique_words (int): number of unique words in regular knowledge
        spam (Dict[str,int]): regular spam dictionary
        ham (Dict[str,int]): regular ham dictionary
        total_ham_files (int): total number of ham files
        spam_lemmatization (Dict[str,int]): lemmatization spam dictionary
        ham_lemmatization (Dict[str,int]): lemmatization ham dictionary
        unique_words_lemmatization (int): number of unique words in lemmatization knowledge
        spam_stopwords (Dict[str,int]): stopwords spam dictionary
        ham_stopwords (Dict[str,int]): stopwords ham dictionary
        unique_words_stopwords (int): number of unique words in stopwords knowledge
        spam_lemmatization_stopwords (Dict[str,int]): lemmatization stopwords spam dictionary
        ham_lemmatization_stopwords (Dict[str,int]): lemmatization stopwords ham dictionary
        unique_words_lemmatization_stopwords (int): number of unique words in lemmatization stopwords knowledge

    Returns:
        Tuple[Dict[str,int],Dict[str,int],Dict[str,int],Dict[str,int]]: knowledge, knowledge_lemmatization, knowledge_lemmatization_stopwords, knowledge_stopwords
    """
    ham['total_files'] = ham.get('total_files', 0) + total_ham_files
    ham_lemmatization['total_files'] = ham['total_files']
    spam_lemmatization['total_files'] = spam['total_files']
    ham_lemmatization_stopwords['total_files'] = ham['total_files']
    spam_lemmatization_stopwords['total_files'] = spam['total_files']
    ham_stopwords['total_files'] = ham['total_files']
    spam_stopwords['total_files'] = spam['total_files']

    # syncs number_of__numbers
    ham_lemmatization['number_of_numbers'] = ham['number_of_numbers']
    spam_lemmatization['number_of_numbers'] = spam['number_of_numbers']
    ham_lemmatization_stopwords['number_of_numbers'] = ham['number_of_numbers']
    spam_lemmatization_stopwords['number_of_numbers'] = spam['number_of_numbers']
    ham_stopwords['number_of_numbers'] = ham['number_of_numbers']
    spam_stopwords['number_of_numbers'] = spam['number_of_numbers']
    # puts ham and spam into one dictionary.
    knowledge = {"ham": ham, "spam": spam, 'unique_words': unique_words}
    knowledge_lemmatization = {"ham": ham_lemmatization,
                               "spam": spam_lemmatization, 'unique_words': unique_words_lemmatization}
    knowledge_lemmatization_stopwords = {"ham": ham_lemmatization_stopwords,
                                         "spam": spam_lemmatization_stopwords, 'unique_words': unique_words_lemmatization_stopwords}
    knowledge_stopwords = {"ham": ham_stopwords,
                           "spam": spam_stopwords, 'unique_words': unique_words_stopwords}

    return knowledge, knowledge_lemmatization, knowledge_lemmatization_stopwords, knowledge_stopwords


def __write_json(knowledge_directory: str, knowledge_json: str, knowledge: Dict[str, int], knowledge_lemmatization_json: str, knowledge_stopwords_json: str, knowledge_lemmatization_stopwords_json: str, knowledge_lemmatization: Dict[str, int], knowledge_lemmatization_stopwords: Dict[str, int], knowledge_stopwords: Dict[str, int]) -> None:
    """
    write_json Writes json to the files.

    Args:
        knowledge_directory (str): Directory to write the json to.
        knowledge_json (str): knowledge json file name.
        knowledge (Dict[str, int]): knowledge dictionary.
        knowledge_lemmatization_json (st): knowledge lemmatization json file name.
        knowledge_stopwords_json (str): knowledge stopwords json file name.
        knowledge_lemmatization_stopwords_json (str): knowledge lemmatization stopwords json file name.
        knowledge_lemmatization (Dict[str, int]): knowledge lemmatization dictionary
        knowledge_lemmatization_stopwords (Dict[str, int]): knowledge lemmatization stopwords dictionary
        knowledge_stopwords (Dict[str, int]): knowledge stopwords dictionary
    """
    os.chdir(knowledge_directory)
    # write json files
    with open(str(knowledge_json), 'w') as spam_file:
        json.dump(knowledge, spam_file)
    with open(str(knowledge_lemmatization_json), 'w') as spam_file:
        json.dump(knowledge_lemmatization, spam_file)
    with open(str(knowledge_stopwords_json), 'w') as spam_file:
        json.dump(knowledge_stopwords, spam_file)
    with open(str(knowledge_lemmatization_stopwords_json), 'w') as spam_file:
        json.dump(knowledge_lemmatization_stopwords, spam_file)


def get_knowledge(directory: str, find_by: re.Pattern) -> None:
    """
    get_files Gets the spam and ham words from the files, and puts them into a json file in the root directory.

    Args:
        directory (str): Directory where the spam and ham files should be.
        find_by (re.Pattern): Regular expression to match the words by.
    """
    # binds root path with email directory.
    email_path = os.path.join(os.path.dirname(__file__), directory)
    # gets ham directory.
    ham_path = os.path.join(email_path, 'ham')
    # gets spam directory.
    spam_path = os.path.join(email_path, 'spam')
    knowledge_directory = os.path.join(os.path.dirname(__file__), 'knowledge')
    unique_words = 0
    # changes directory to spam path.
    os.chdir(knowledge_directory)
    # declares variables.
    spam = {}
    ham = {}
    total_spam_files = 0
    total_ham_files = 0
    unique_words = 0
    spam_lemmatization = {}
    ham_lemmatization = {}
    unique_words_lemmatization = 0
    spam_stopwords = {}
    ham_stopwords = {}
    unique_words_stopwords = 0
    spam_lemmatization_stopwords = {}
    ham_lemmatization_stopwords = {}
    unique_words_lemmatization_stopwords = 0
    # counts number of spam/ham files.

    # import all existing knowledge
    knowledge_json = 'knowledge.json'
    if knowledge_json in os.listdir():
        with open(knowledge_json, 'r') as knowledge_file:
            knowledge = json.load(knowledge_file)
            spam = knowledge['spam']
            ham = knowledge['ham']
            total_spam_files = spam['total_files']
            total_ham_files = ham['total_files']
            unique_words = knowledge['unique_words']
    knowledge_lemmatization_json = 'knowledge_lemmatization.json'
    if knowledge_lemmatization_json in os.listdir():
        with open(knowledge_lemmatization_json, 'r') as knowledge_file:
            knowledge = json.load(knowledge_file)
            spam_lemmatization = knowledge['spam']
            ham_lemmatization = knowledge['ham']
            unique_words_lemmatization = knowledge['unique_words']
    knowledge_stopwords_json = 'knowledge_stopwords.json'
    if knowledge_stopwords_json in os.listdir():
        with open(knowledge_stopwords_json, 'r') as knowledge_file:
            knowledge = json.load(knowledge_file)
            spam_stopwords = knowledge['spam']
            ham_stopwords = knowledge['ham']
            unique_words_stopwords = knowledge['unique_words']
    knowledge_lemmatization_stopwords_json = 'knowledge_lemmatization_stopwords.json'
    if knowledge_lemmatization_stopwords_json in os.listdir():
        with open(knowledge_lemmatization_stopwords_json, 'r') as knowledge_file:
            knowledge = json.load(knowledge_file)
            spam_lemmatization_stopwords = knowledge['spam']
            ham_lemmatization_stopwords = knowledge['ham']
            unique_words_lemmatization_stopwords = knowledge['unique_words']
    
    # list to iterate over reading files.
    read_file_parameters = [
        (spam_path, spam, spam_stopwords, spam_lemmatization,
            spam_lemmatization_stopwords, total_spam_files),
        (ham_path, ham, ham_stopwords, ham_lemmatization,
            ham_lemmatization_stopwords, total_ham_files),
    ]
    print("Reading files...")
    time.sleep(1)
    # for each type of email.
    for path, email_type, stopwords, lemmatization, lemmatization_stopwords, total_files in read_file_parameters:
        os.chdir(path)
        for filename in os.listdir(path):
            # open file
            with open(filename, 'r', errors='ignore') as f:
                # find all words in file.
                for word in re.findall(find_by, f.read()):
                    # checks if word is in current knowledge dictionary.
                    if word[0] not in spam or word[0] not in ham:
                        unique_words += 1
                    # puts word into spam dictionary.
                    if word[1]:
                        email_type['number_of_numbers'] = email_type.get(
                            'number_of_numbers', 0) + 1
                    elif word[0] != "":
                        email_type[word[0]] = email_type.get(word[0], 0) + 1
                    # gets a lemmatized_word
                    lemmatized_word = LEMMATIZER.lemmatize(word[0])
                    # stopwords
                    if word[0].lower() not in ENGLISH_STOPWORDS:
                        stopwords[word[0]] = stopwords.get(
                            word[0], 0) + 1
                        # lemmatization and stopwords
                        lemmatization_stopwords[lemmatized_word] = lemmatization_stopwords.get(
                            lemmatized_word, 0)+1

                    # lemmatization
                    lemmatization[lemmatized_word] = lemmatization.get(
                        lemmatized_word, 0) + 1
            total_files += 1
        email_type['total_files'] = email_type.get(
            'total_files', 0) + total_files
    # combines ham and spam into one dictionary for each type.
    knowledge, knowledge_lemmatization, knowledge_lemmatization_stopwords, knowledge_stopwords = __combine_into_one_dictionary(
        unique_words, spam, ham, total_ham_files, spam_lemmatization, ham_lemmatization, unique_words_lemmatization, spam_stopwords, ham_stopwords, unique_words_stopwords, spam_lemmatization_stopwords, ham_lemmatization_stopwords, unique_words_lemmatization_stopwords)
    del(ham)
    del(spam)
    # changes directory back to the same path as this file.
    __write_json(knowledge_directory, knowledge_json, knowledge, knowledge_lemmatization_json, knowledge_stopwords_json,
                 knowledge_lemmatization_stopwords_json, knowledge_lemmatization, knowledge_lemmatization_stopwords, knowledge_stopwords)
