import json
import os
import re
import time
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
# constants
LEMMATIZER = WordNetLemmatizer()
ENGLISH_STOPWORDS = set(stopwords.words('english'))
# add subject to stopwords
ENGLISH_STOPWORDS.add('subject')


def get_words(directory: str, find_by: re.Pattern) -> None:
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
    # declares empty spam/ham directory.
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
    knowledge_lemmatization = 'knowledge_lemmatization.json'
    if knowledge_lemmatization in os.listdir():
        with open( knowledge_lemmatization, 'r') as knowledge_file:
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
                if word[0] not in spam or word[0] not in ham:
                    unique_words += 1
                # puts word into spam dictionary.
                spam[word[0]] = spam.get(word[0], 0) + 1
                if word[1]:
                    spam['number_of_numbers'] = spam.get(
                        'number_of_numbers', 0) + 1
                lemmatized_word = LEMMATIZER.lemmatize(word[0])
                # stopwords
                if word[0].lower() not in ENGLISH_STOPWORDS:
                    spam_stopwords[word[0]] = spam_stopwords.get(
                        word[0], 0) + 1
                    # lemmatization and stopwords
                    spam_lemmatization_stopwords[lemmatized_word] = spam_lemmatization_stopwords.get(
                        lemmatized_word, 0)+1

                # lemmatization
                spam_lemmatization[lemmatized_word] = spam_lemmatization.get(
                    lemmatized_word, 0) + 1
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
                if word[0] not in spam:
                    unique_words += 1
                # puts word into ham dictionary.
                ham[word[0]] = ham.get(word[0], 0) + 1
                if word[1]:
                    ham['number_of_numbers'] = ham.get(
                        'number_of_numbers', 0) + 1
                lemmatized_word = LEMMATIZER.lemmatize(word[0])
                # stopwords
                if word[0].lower() not in ENGLISH_STOPWORDS:
                    ham_stopwords[word[0]] = ham_stopwords.get(word[0], 0) + 1
                    # lemmatization and stopwords
                    ham_lemmatization_stopwords[lemmatized_word] = ham_lemmatization_stopwords.get(
                        lemmatized_word, 0) + 1
                    if word[0] not in spam_lemmatization_stopwords:
                        unique_words_lemmatization_stopwords += 1
                    if word[0] not in spam_stopwords:
                        unique_words_stopwords += 1

                # lemmatization
                ham_lemmatization[lemmatized_word] = ham_lemmatization.get(
                    lemmatized_word, 0)+1
                if word[0] not in ham_lemmatization:
                    unique_words_lemmatization += 1
        total_ham_files += 1
    # total ham files read
    # syncs number of files read
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
    del(ham)
    del(spam)
    # changes directory back to the same path as this file.
    os.chdir(knowledge_directory)
    # write json files
    with open(str(knowledge_json), 'w') as spam_file:
        json.dump(knowledge, spam_file)
    with open(str( knowledge_lemmatization), 'w') as spam_file:
        json.dump(knowledge_lemmatization, spam_file)
    with open(str(knowledge_stopwords_json), 'w') as spam_file:
        json.dump(knowledge_stopwords, spam_file)
    with open(str(knowledge_lemmatization_stopwords_json), 'w') as spam_file:
        json.dump(knowledge_lemmatization_stopwords, spam_file)
