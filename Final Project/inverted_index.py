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
    data = {"inverted_index": {}, "max_freq_wc": [],
            "tf_idf": {}, "list_of_words": {}}
    if not os.path.isdir(output_path):
        os.makedirs(output_path)
    os.chdir(input_path)
    # for each page...
    for document_number, filename in enumerate(os.listdir(input_path)):
        current_words: str
        with open(filename, 'r') as f:
            current_words = f.readlines()[1].split(" ")
        # puts word into dictionary
        for word in current_words:
            # if dictionary key doesn't exist, create it.
            if not data["inverted_index"].get(word, None):
                data["inverted_index"][word] = {}
            # if word count doesn't exist, create it.
            if not data["inverted_index"][word].get(document_number, False):
                data["inverted_index"][word][document_number] = current_words.count(
                    word)
        # puts each document into a set of words
        data["list_of_words"][document_number] = set(current_words)
        # gets mode to get the maximum frequency & number of words in document.
        data["max_freq_wc"].append(current_words.count(
            statistics.mode(current_words)))
    data = get_tf_idf(data)
    # dumps json.
    os.chdir(output_path)
    for keys, values in data.items():
        with open(f'{keys}'.json, 'w') as f:
            json.dump(values, f, sort_keys=True, indent=4)


def get_tf_idf(data: Dict,) -> Dict:
    """
    get_tf_idf Gets the TF idf data and returns the dictionary.

    Args:
        data (Dict): Dictionary containing inverted_index, max_freq_wc, and list_of_word keys.

    Returns:
        Dict: Dictionary containing given data, and tf_idf values.
    """
    NUMBER_OF_DOCUMENTS = len(data["max_freq_wc"])
    # for each document in the data.
    for document_number, freq_wc in enumerate(data["max_freq_wc"].items()):
        data["tf_idf"][document_number] = {}
        # for each word in the document.
        for word in data["list_of_words"][document_number]:
            data["tf_idf"][document_number][word] = (
                data["inverted_index"][word][document_number]/freq_wc)*(NUMBER_OF_DOCUMENTS/len(data["inverted_index"][word]))
    return data
