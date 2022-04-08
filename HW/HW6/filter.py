import json
import re
import os
import enum
import math
from typing import Dict


class EmailType(enum.Enum):
    spam = 0
    ham = 1


def get_probability(file_findings: Dict, knowledge: Dict) -> str:
    spam_to_calculate = set()
    ham_to_calculate = set()
    p_spam = float(knowledge['spam']['total_files'] / int(knowledge['spam']
                   ['total_files']+knowledge['spam']['total_files']))
    p_ham = float(knowledge['ham']['total_files'] / int(knowledge['ham']
                  ['total_files']+knowledge['ham']['total_files']))
    spam_unique_word_count = knowledge['spam']['total_words']
    ham_unique_word_count = knowledge['ham']['total_words']
    unique_words = knowledge['unique_words']
    spam_to_calculate.add(math.log(p_spam))
    ham_to_calculate.add(math.log(p_ham))
    for key, value in file_findings.items():
        ham_to_calculate.add(
            math.log((knowledge['ham'].get(key, 0)+1)/(ham_unique_word_count+unique_words)))
        spam_to_calculate.add(math.log((knowledge['spam'].get(
            key, 0)+1)/(spam_unique_word_count+unique_words)))
    spam_calculation = sum(spam_to_calculate)
    ham_calculation = sum(ham_to_calculate)
    if spam_calculation > ham_calculation:
        return "Spam"
    else:
        return "Ham"


def filter_messages(knowledge_file: str, find_by: re.Pattern, directory_to_filter: str):
    """
    filter_messages Filters messages given a specified directory to filter.

    Args:
        knowledge (str): Name of the json file with the knowledge to filter.
        find_by (re.Pattern): a pattern to match the words in the messages with.
        directory_to_filter (str): directory name to filter messages.
    """
    email_path = os.path.join(os.path.dirname(__file__), directory_to_filter)
    spam_path = os.path.join(email_path, 'spam')
    ham_path = os.path.join(email_path, 'ham')
    knowledge: Dict
    with open(knowledge_file, 'r') as kf:
        knowledge = json.load(kf)
    findings = []
    message_count = 0

    # filters through spam emails.
    for filename in os.listdir(spam_path):
        with open(filename, 'r') as f:
            file_findings = {}
            for word in re.findall(find_by, f.readline):
                file_findings[word] = file_findings.get(word, 0) + 1
            email_type = get_probability(file_findings, knowledge)
            findings.append(
                f'Message {message_count}: {email_type}. Real: Spam')
            message_count += 1
            # filters through ham emails.
    for filename in os.listdir(ham_path):
        with open(filename, 'r') as f:
            file_findings[word] = file_findings.get(word, 0) + 1
            email_type = get_probability(file_findings, knowledge)
            findings.append(
                f'Message {message_count}: {email_type}. Real: Ham')
            message_count += 1
    print("\n\n".join([finding for finding in findings]))
