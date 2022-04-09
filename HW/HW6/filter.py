import json
import math
import os
import re
from typing import Dict, List


def print_findings(findings: Dict) -> None:
    """
    print_findings Prints the findings as fractions and decimals.

    Args:
        findings (Dict): dictionary of findings.
    """
    guess_spam = 0
    guess_ham = 0
    real_spam = 0
    real_ham = 0
    for _, value in findings.items():
        if value[0] == 'ham':
            guess_ham += 1
        else:
            guess_spam += 1
        if value[1] == 'ham':
            real_ham += 1
        else:
            real_spam += 1
    print(f'Spam Caught:{guess_spam}/{real_spam}({guess_spam/real_spam})')
    print(f'Ham Caught:{guess_ham}/{real_ham}({guess_ham/real_ham})')


def __get_probability(file_findings: Dict, knowledge: Dict) -> str:
    """
    __get_probability Gets the probability of one spam/ham email file.

    Args:
        file_findings (Dict): findings from the email read.
        knowledge (Dict): current knowledge from the existing emails.

    Returns:
        str: Spam or Ham depending on the probability of the email being either spam or ham.
    """
    # puts in set since order is not important.
    spam_to_calculate = set()
    ham_to_calculate = set()
    # gets the probability of the email being spam.
    p_spam = float(knowledge['spam']['total_files'] / int(knowledge['spam']
                   ['total_files']+knowledge['spam']['total_files']))
    # gets the probability of the email being ham.
    p_ham = float(knowledge['ham']['total_files'] / int(knowledge['ham']
                  ['total_files']+knowledge['ham']['total_files']))
    # gets total number of unique words. This does subtract 1 because of total_files key.
    spam_unique_word_count = len(knowledge['spam'].values())-1
    ham_unique_word_count = len(knowledge['ham'].values())-1
    # get the total number of unique words.
    unique_words = knowledge['unique_words']
    # puts probability of ham/spam in the sets.
    spam_to_calculate.add(math.log(p_spam))
    ham_to_calculate.add(math.log(p_ham))
    # for each word, add the probability of the email being spam.
    for key, _ in file_findings.items():
        # puts in ham set.
        ham_to_calculate.add(
            math.log((knowledge['ham'].get(key, 0)+1)/(ham_unique_word_count+unique_words)))
        # puts in spam set.
        spam_to_calculate.add(math.log((knowledge['spam'].get(
            key, 0)+1)/(spam_unique_word_count+unique_words)))
    # calculates the probabilities.
    spam_probability = sum(spam_to_calculate)
    ham_probability = sum(ham_to_calculate)
    # returns ham or spam based on the probabilities.
    if spam_probability > ham_probability:
        return 'spam'
    return 'ham'


def filter_messages(directory_to_filter: str, find_by: re.Pattern, knowledge_file: str) -> Dict:
    """
    filter_messages Filters messages given a specified directory to filter.

    Args:
        knowledge (str): Name of the json file with the knowledge to filter.
        find_by (re.Pattern): a pattern to match the words in the messages with.
        directory_to_filter (str): directory name to filter messages.
    Returns:
        List: Dictionary of the findings of the messages.
    """
    # changes to the current directory.
    os.chdir(os.path.dirname(__file__))
    # generates email,spam and ham paths.
    email_path = os.path.join(os.path.dirname(__file__), directory_to_filter)
    spam_path = os.path.join(email_path, 'spam')
    ham_path = os.path.join(email_path, 'ham')
    knowledge: Dict
    # gets knowledge from the knowledge file.
    with open(knowledge_file, 'r') as kf:
        knowledge = json.load(kf)
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
                file_findings[word] = file_findings.get(word, 0) + 1
            # gets spam/ham email type.
            email_type = __get_probability(file_findings, knowledge)
            # records all findings.
            findings[message_count] = [email_type, 'spam']
            message_count += 1

    # filters through ham emails.
    os.chdir(ham_path)
    for filename in os.listdir(ham_path):
        # open the file in the iteration.
        with open(filename, 'r', errors='ignore') as f:
            # gets all the words in the ham email.
            for word in re.findall(find_by, f.read()):
                # adds one to the word count.
                file_findings[word] = file_findings.get(word, 0) + 1
            # gets spam/ham email type.
            email_type = __get_probability(file_findings, knowledge)
            # records all findings.
            findings[message_count] = [email_type, 'ham']
            message_count += 1
    # prints all findings.
    # print([finding for finding in findings.values()])
    print_findings(findings)

    return findings
