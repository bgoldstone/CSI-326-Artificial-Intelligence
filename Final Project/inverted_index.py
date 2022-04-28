import os
import json
import statistics
from typing import Dict


def create_inverted_index(input_path: str, output_path: str) -> None:
    """
    create_inverted_index Creates an inverted index given input_path and output_path.

    Args:
        input_path (str): path to find the scraped files from.
        output_path (str): path to write the inverted index, max_freq_wc, tf_idf, and list_of_words to.
    """
    # contains inverted index, max frequencies & word count, and term frequencies & inverted document frequency
    data = {'inverted_index': {}, 'max_freq_wc': [],
            'tf_idf': {}, 'list_of_words': {}, 'urls': [], 'idf': {}}
    if not os.path.isdir(output_path):
        os.makedirs(output_path)
    os.chdir(input_path)
    # for each page...
    document_number = 0
    for filename in os.listdir(input_path):
        if os.path.isdir(filename):
            continue
        current_words: str
        print(f'Processing document #{document_number}')
        with open(filename, 'r') as f:
            print(filename)
            lines = f.readlines()
            # if not text, skip.
            if len(lines) < 2:
                continue
            data['urls'].append(lines[0])
            current_words = lines[1].split(' ')
        # puts word into dictionary
        for word in current_words:
            word_parsed = word.replace('"', '')
            if word_parsed == '':
                continue
            # if dictionary key doesn't exist, create it.
            if not data['inverted_index'].get(word_parsed, None):
                data['inverted_index'][word_parsed] = {}
            # if word count doesn't exist, create it.
            if not data['inverted_index'][word_parsed].get(document_number, False):
                data['inverted_index'][word_parsed][document_number] = current_words.count(
                    word_parsed)
        # puts each document into a set of words
        data['list_of_words'][document_number] = list(set(current_words))
        # gets mode to get the maximum frequency & number of words in document.
        data['max_freq_wc'].append(current_words.count(
            statistics.mode(current_words)))
        document_number += 1
    data = get_tf_idf(data)
    # dumps json.
    os.chdir(output_path)
    for keys, values in data.items():
        with open(f'{keys}.json', 'w') as f:
            json.dump(values, f, sort_keys=True, indent=4)


def get_tf_idf(data: Dict,) -> Dict:
    """
    get_tf_idf Gets the TF idf data and returns the dictionary.

    Args:
        data (Dict): Dictionary containing inverted_index, max_freq_wc, and list_of_word keys.

    Returns:
        Dict: Dictionary containing given data, and tf_idf values.
    """
    NUMBER_OF_DOCUMENTS = len(data['max_freq_wc'])
    # for each document in the data.
    for document_number, freq_wc in enumerate(data['max_freq_wc']):
        print(f'Document #{document_number}')
        data['tf_idf'][document_number] = {}
        # for each word in the document.
        for word in data['list_of_words'][document_number]:
            word_parsed = word.replace('"', '')
            if word_parsed == '':
                continue
            if not data['idf'].get(word_parsed, False):
                data['idf'][word_parsed] = NUMBER_OF_DOCUMENTS / \
                    len(data['inverted_index'][word_parsed])
            data['tf_idf'][document_number][word_parsed] = (
                data['inverted_index'][word_parsed][document_number]/freq_wc*data['tf_idf'][word_parsed])
    return data
