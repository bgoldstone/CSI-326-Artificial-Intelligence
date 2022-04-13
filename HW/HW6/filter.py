import json
import math
import os
import re
from typing import Dict, Tuple


def calculate_word_count(knowledge: Dict[str, int]) -> Tuple[int, int]:
    spam = knowledge['spam']
    ham = knowledge['ham']
    number_of_spam_words = sum(
        [value for key, value in spam.items() if key != 'total_files'])
    number_of_ham_words = sum(
        [value for key, value in ham.items() if key != 'total_files'])
    return (number_of_spam_words, number_of_ham_words)


def get_findings(findings: Dict) -> Dict[str, float]:
    """
    get_findings get  the findings and puts it into a dictionary.

    Args:
        findings (Dict): dictionary of findings.
    """
    true_positive = 0
    true_negative = 0
    false_negative = 0
    false_positive = 0
    # for each value in findings, get total true positives and false negatives.
    for _, value in findings.items():
        if value[0] == 'ham' and value[1] == 'ham':
            true_negative += 1
        elif value[0] == 'spam' and value[1] == 'spam':
            true_positive += 1
        if value[1] == 'ham' and value[0] == 'spam':
            false_positive += 1
        elif value[1] == 'spam' and value[0] == 'ham':
            false_negative += 1
        total = true_positive + true_negative + false_positive + false_negative
    accuracy = float((true_negative+false_positive)/total)
    precision = float(true_positive/(true_positive+false_positive))
    recall = float(true_positive/(true_positive+false_negative))
    return {"accuracy": accuracy, "precision": precision, "recall": recall}


def __get_probability(file_findings: Dict, knowledge: Dict, number_of_spam_words: int, number_of_ham_words: int) -> str:
    """
    __get_probability Gets the probability of one spam/ham email file.

    Args:
        file_findings (Dict): findings from the email read.
        knowledge (Dict): current knowledge from the existing emails.

    Returns:
        str: Spam or Ham depending on the probability of the email being either spam or ham.
    """
    # puts in set since order is not important.
    spam_to_calculate = []
    ham_to_calculate = []
    total_number_of_files = int(knowledge['spam']
                                ['total_files']+knowledge['ham']['total_files'])
    # gets the probability of the email being spam.
    p_spam = float(knowledge['spam']['total_files'] / total_number_of_files)
    # gets the probability of the email being ham.
    p_ham = float(knowledge['ham']['total_files'] / total_number_of_files)
    # gets total number of unique words. This does subtract 1 because of total_files key.
    spam_unique_word_count = len(knowledge['spam'].values())-1
    ham_unique_word_count = len(knowledge['ham'].values())-1
    # get the total number of unique words.
    unique_words = knowledge['unique_words']
    # puts probability of ham/spam in the sets.
    spam_to_calculate.append(math.log(p_spam))
    ham_to_calculate.append(math.log(p_ham))
    # for each word, add the probability of the email being spam.
    for key, value in file_findings.items():
        # puts in ham set.
        # log(x^y) = y * log(x)
        ham_to_calculate.append(value *
                                math.log((knowledge['ham'].get(key, 0)+1)/(number_of_ham_words+unique_words)))
        # puts in spam set.
        spam_to_calculate.append(value * math.log((knowledge['spam'].get(
            key, 0)+1)/(number_of_spam_words+unique_words)))
    # calculates the probabilities.
    spam_probability = sum(spam_to_calculate)
    ham_probability = sum(ham_to_calculate)
    # returns ham or spam based on the probabilities.
    if spam_probability > ham_probability:
        return 'spam'
    return 'ham'


def filter_messages(directory_to_filter: str, find_by: re.Pattern, stopwords=False, lemmatization=False) -> Dict[str, float]:
    """
    filter_messages Filters messages given a specified directory to filter.

    Args:
        knowledge (str): Name of the json file with the knowledge to filter.
        find_by (re.Pattern): a pattern to match the words in the messages with.
        stopwords (bool): if true, stopwords is enabled
        lemmatization (bool): if true, lemmatization is enabled
    Returns:
        List: Dictionary of the findings of the messages.
    """
    knowledge_type = ""
    if stopwords and lemmatization:
        knowledge_type = "_lemmatization_stopwords"
    if stopwords:
        knowledge_type = "_stopwords"
    if lemmatization:
        knowledge_type = "_lemmatization"
    # generates email,spam and ham paths.
    email_path = os.path.join(os.path.dirname(__file__), directory_to_filter)
    spam_path = os.path.join(email_path, 'spam')
    ham_path = os.path.join(email_path, 'ham')
    knowledge_directory = os.path.join(os.path.dirname(__file__), 'knowledge')
    knowledge: Dict
    # changes to the knowledge directory.
    os.chdir(knowledge_directory)
    # gets knowledge from the knowledge file.
    knowledge_file = f'knowledge{knowledge_type}.json'
    with open(knowledge_file, 'r') as kf:
        knowledge = json.load(kf)
    # gets total number of words in spam and ham files.
    number_of_spam_words, number_of_ham_words = calculate_word_count(
        knowledge)
    # records findings.
    findings = {}
    # starts message count at zero.
    message_count = 1

    # filters through spam emails.
    os.chdir(spam_path)
    for filename in os.listdir(spam_path):
        # open the file in the iteration.
        with open(filename, 'r', errors='ignore') as f:
            file_findings = {}
            # gets all the words in the spam email.
            for word in re.findall(find_by, f.read()):
                # adds one to the word count.
                file_findings[word[0]] = file_findings.get(word[0], 0) + 1
                if word[1]:
                    file_findings['number_of_numbers'] = file_findings.get(
                        'number_of_numbers', 0) + 1
            # gets spam/ham email type.
            email_type = __get_probability(
                file_findings, knowledge, number_of_spam_words, number_of_ham_words)
            # records all findings.
            findings[str(message_count)] = [email_type, 'spam']
            message_count += 1

    # filters through ham emails.
    os.chdir(ham_path)
    for filename in os.listdir(ham_path):
        # open the file in the iteration.
        with open(filename, 'r', errors='ignore') as f:
            file_findings = {}
            # gets all the words in the ham email.
            for word in re.findall(find_by, f.read()):
                # adds one to the word count.
                file_findings[word[0]] = file_findings.get(word[0], 0) + 1
                # if number_of_numbers
                if word[1]:
                    file_findings['number_of_numbers'] = file_findings.get(
                        'number_of_numbers', 0) + 1
            # gets spam/ham email type.
            email_type = __get_probability(
                file_findings, knowledge, number_of_spam_words, number_of_ham_words)
            # records all findings.
            findings[message_count] = [email_type, 'ham']
            message_count += 1
    # prints all findings.
    return get_findings(findings)
