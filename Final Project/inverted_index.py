import os
import json
import statistics
from typing import Dict
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


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
    data_stopwords = {'inverted_index': {}, 'max_freq_wc': [],
                      'tf_idf': {}, 'list_of_words': {}, 'urls': [], 'idf': {}}
    data_stemming = {'inverted_index': {}, 'max_freq_wc': [],
                     'tf_idf': {}, 'list_of_words': {}, 'urls': [], 'idf': {}}
    data_stopwords_stemming = {'inverted_index': {}, 'max_freq_wc': [],
                               'tf_idf': {}, 'list_of_words': {}, 'urls': [], 'idf': {}}
    all_data = {'': data, '_stopwords': data_stopwords,
                '_stemming': data_stemming, '_stopwords_stemming': data_stopwords_stemming}
    STEMMING = PorterStemmer()
    STOPWORDS = set(stopwords.words('english'))
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
        data_stopwords['urls'].append(lines[0])
        data_stemming['urls'].append(lines[0])
        data_stopwords_stemming['urls'].append(lines[0])
        current_words = lines[1].lower().split(' ')
        # puts word into dictionary
        for word in current_words:
            word_parsed = word.replace('"', '')
            if word_parsed == '':
                continue
            # if word count doesn't exist, create it.
            if not data['inverted_index'].get(word_parsed, False):
                data['inverted_index'][word_parsed] = {}
                data_stemming['inverted_index'][STEMMING.stem(
                    word_parsed)] = {}
                if word_parsed not in STOPWORDS:
                    data_stopwords['inverted_index'][word_parsed] = {}
                    data_stopwords_stemming['inverted_index'][STEMMING.stem(word_parsed)] = {
                    }
            # if document number doesn't exist, create it.
            if not data['inverted_index'][word_parsed].get(str(document_number), False):
                data['inverted_index'][word_parsed][str(document_number)] = current_words.count(
                    word_parsed)
                data_stemming['inverted_index'][STEMMING.stem(
                    word_parsed)][str(document_number)] = current_words.count(STEMMING.stem(word_parsed))
                if word_parsed not in STOPWORDS:
                    data_stopwords['inverted_index'][word_parsed][str(document_number)] = current_words.count(
                        word_parsed)
                    data_stopwords_stemming['inverted_index'][STEMMING.stem(word_parsed)][str(document_number)] = current_words.count(
                        STEMMING.stem(word_parsed))
        # puts each document into a set of words
        data['list_of_words'][str(document_number)] = [
            str(word) for word in set(current_words)]
        data_stopwords['list_of_words'][str(document_number)] = [
            str(stop_word) for stop_word in set(current_words) if stop_word not in STOPWORDS]
        data_stopwords_stemming['list_of_words'][str(document_number)] = [STEMMING.stem(
            str(stem_word)) for stem_word in data_stopwords['list_of_words'][str(document_number)]]
        data_stemming['list_of_words'][str(document_number)] = [
            STEMMING.stem(str(stem_word)) for stem_word in set(current_words)]
        # gets mode to get the maximum frequency & number of words in document.
        data['max_freq_wc'].append(current_words.count(
            statistics.mode(current_words)))
        data_stopwords['max_freq_wc'].append(data_stopwords['list_of_words'][str(document_number)].count(
            statistics.mode(data_stopwords['list_of_words'][str(document_number)])))
        data_stopwords_stemming['max_freq_wc'].append(data_stopwords_stemming['list_of_words'][str(document_number)].count(
            statistics.mode(data_stopwords_stemming['list_of_words'][str(document_number)])))
        data['max_freq_wc'].append(data_stemming['list_of_words'][str(document_number)].count(
            statistics.mode(data_stemming['list_of_words'][str(document_number)])))
        document_number += 1
    data = get_tf_idf(data)
    data_stopwords = get_tf_idf(data_stopwords)
    data_stopwords_stemming = get_tf_idf(data_stopwords_stemming)
    data_stemming = get_tf_idf(data_stemming)
    # dumps json.
    os.chdir(output_path)
    for file_extension, dataset in all_data.items():
        for keys, values in dataset.items():
            with open(f'{keys}{file_extension}.json', 'w') as f:
                json.dump(values, f, sort_keys=True, indent=4)


def get_tf_idf(data: Dict) -> Dict:
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
        data['tf_idf'][str(document_number)] = {}
        # for each word in the document.
        for word in data['list_of_words'][str(document_number)]:
            word_parsed = word.replace('"', '')
            if word_parsed == '':
                continue
            if not data['idf'].get(word_parsed, False):
                data['idf'][word_parsed] = NUMBER_OF_DOCUMENTS / \
                    len(data['inverted_index'][word_parsed])
            data['tf_idf'][str(document_number)][word_parsed] = ((
                data['inverted_index'][word_parsed][str(document_number)]/freq_wc)*(data['idf'][word_parsed]))
    return data
