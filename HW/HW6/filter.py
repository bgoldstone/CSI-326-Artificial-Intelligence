import json
import math
import os
import re
from typing import Dict


def __get_probability(file_findings: Dict, knowledge: Dict) -> str:
    spam_to_calculate = set()
    ham_to_calculate = set()
    p_spam = float(knowledge['spam']['total_files'] / int(knowledge['spam']
                   ['total_files']+knowledge['spam']['total_files']))
    p_ham = float(knowledge['ham']['total_files'] / int(knowledge['ham']
                  ['total_files']+knowledge['ham']['total_files']))
    # gets total words. does "-1" because of total_files key
    spam_unique_word_count = len(knowledge['spam'].values()-1)
    ham_unique_word_count = len(knowledge['ham'].values()-1)
    unique_words = knowledge['unique_words']
    spam_to_calculate.add(math.log(p_spam))
    ham_to_calculate.add(math.log(p_ham))
    for key, _ in file_findings.items():
        ham_to_calculate.add(
            math.log((knowledge['ham'].get(key, 0)+1)/(ham_unique_word_count+unique_words)))
        spam_to_calculate.add(math.log((knowledge['spam'].get(
            key, 0)+1)/(spam_unique_word_count+unique_words)))
    spam_probability = sum(spam_to_calculate)
    ham_probability = sum(ham_to_calculate)
    if spam_probability > ham_probability:
        return "Spam"
    else:
        return "Ham"


def filter_messages(directory_to_filter: str, find_by: re.Pattern, knowledge_file: str):
    """
    filter_messages Filters messages given a specified directory to filter.

    Args:
        knowledge (str): Name of the json file with the knowledge to filter.
        find_by (re.Pattern): a pattern to match the words in the messages with.
        directory_to_filter (str): directory name to filter messages.
    """
    os.chdir(os.path.dirname(__file__))
    email_path = os.path.join(os.path.dirname(__file__), directory_to_filter)
    spam_path = os.path.join(email_path, 'spam')
    ham_path = os.path.join(email_path, 'ham')
    knowledge: Dict
    with open(knowledge_file, 'r') as kf:
        knowledge = json.load(kf)
    findings = []
    message_count = 0

    # filters through spam emails.
    os.chdir(spam_path)
    for filename in os.listdir(spam_path):
        with open(filename, 'r', errors='ignore') as f:
            file_findings = {}
            print(filename)
            for word in re.findall(find_by, f.read()):
                file_findings[word] = file_findings.get(word, 0) + 1
            email_type = __get_probability(file_findings, knowledge)
            findings.append(
                f'Message {message_count}: {email_type}. Real: Spam')
            message_count += 1

    # filters through ham emails.
    os.chdir(ham_path)
    for filename in os.listdir(ham_path):
        with open(filename, 'r', errors='ignore') as f:
            print(filename)
            for word in re.findall(find_by, f.read()):
                file_findings[word] = file_findings.get(word, 0) + 1
            email_type = __get_probability(file_findings, knowledge)
            findings.append(
                f'Message {message_count}: {email_type}. Real: Ham')
            message_count += 1
    print("\n\n".join([finding for finding in findings]))
