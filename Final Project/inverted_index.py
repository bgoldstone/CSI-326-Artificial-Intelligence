import os
import json
import statistics
from typing import Dict
from nltk.stem import PorterStemmer


def create_inverted_index(input_path: str, output_path: str) -> None:
    """
    create_inverted_index Creates an inverted index given input_path and output_path.
    Args:
        input_path (str): path to find the scraped files from.
        output_path (str): path to write the inverted index, max_freq_wc, tf_idf, and list_of_words to.
    """
    # contains inverted index, max frequencies & word count, and term frequencies & inverted document frequency
    data = {"inverted_index": {}, "max_freq_wc": {},
            "tf_idf": {}, "list_of_words": {}, "urls": {}, "idf": {}}
    data_stopwords = {'inverted_index': {}, 'max_freq_wc': {},
                      'tf_idf': {}, 'list_of_words': {}, 'urls': {}, 'idf': {}}
    data_stemming = {'inverted_index': {}, 'max_freq_wc': {},
                     'tf_idf': {}, 'list_of_words': {}, 'urls': {}, 'idf': {}}
    data_stopwords_stemming = {'inverted_index': {}, 'max_freq_wc': {},
                               'tf_idf': {}, 'list_of_words': {}, 'urls': {}, 'idf': {}}
    all_data = {'': data, '_stopwords': data_stopwords,
                '_stemming': data_stemming, '_stopwords_stemming': data_stopwords_stemming}
    STEMMING = PorterStemmer()
    STOPWORDS: set
    with open(os.path.join(os.path.abspath(__file__), "..", "stopwords.txt"), 'r') as f:
        STOPWORDS = set([line.replace("\n", "") for line in f])
    if not os.path.isdir(output_path):
        os.makedirs(output_path)
    os.chdir(input_path)
    # for each page...
    for filename in os.listdir(input_path):
        if os.path.isdir(filename):
            continue
        document_number = filename[filename.find(
            "_")+1:filename.find(".")]
        current_words: str
        print(f"Processing document #{document_number}")
        with open(filename, 'r') as f:
            lines = f.readlines()
        # if not text, skip.
        if len(lines) < 2:
            continue
        # gets urls
        data["urls"][document_number] = lines[0]
        data_stopwords['urls'][document_number] = lines[0]
        data_stemming['urls'][document_number] = lines[0]
        data_stopwords_stemming['urls'][document_number] = lines[0]
        # gets words
        current_words = [current_word.lower()
                         for current_word in lines[1].split(" ")]
        # puts word into dictionary
        for word in current_words:
            if word == "":
                continue
            # if dictionary key doesn't exist, create it.
            if word not in data["inverted_index"].keys():
                data["inverted_index"][word] = {}
                data_stemming['inverted_index'][STEMMING.stem(
                    word)] = {}
                if word not in STOPWORDS:
                    data_stopwords['inverted_index'][word] = {}
                    data_stopwords_stemming['inverted_index'][STEMMING.stem(word)] = {
                    }
            # put word count in
            data["inverted_index"][word][document_number] = current_words.count(
                word)
            data_stemming['inverted_index'][STEMMING.stem(
                word)][document_number] = current_words.count(STEMMING.stem(word))
            if word not in STOPWORDS:
                data_stopwords['inverted_index'][word][document_number] = current_words.count(
                    word)
                data_stopwords_stemming['inverted_index'][STEMMING.stem(word)][document_number] = current_words.count(
                    STEMMING.stem(word))
        # puts each document into a set of words
        data["list_of_words"][document_number] = list(set(current_words))
        data_stopwords['list_of_words'][document_number] = [
            stop_word for stop_word in set(current_words) if stop_word not in STOPWORDS]
        data_stopwords_stemming['list_of_words'][document_number] = [STEMMING.stem(
            stem_word) for stem_word in data_stopwords['list_of_words'][document_number]]
        data_stemming['list_of_words'][document_number] = [
            STEMMING.stem(stem_word) for stem_word in set(current_words)]
        # gets mode to get the maximum frequency of the most common word.
        data["max_freq_wc"][document_number] = current_words.count(
            statistics.mode(current_words))
        data_stopwords['max_freq_wc'][document_number] = data_stopwords['list_of_words'][document_number].count(
            statistics.mode(data_stopwords['list_of_words'][document_number]))
        data_stopwords_stemming['max_freq_wc'][document_number] = data_stopwords_stemming['list_of_words'][document_number].count(
            statistics.mode(data_stopwords_stemming['list_of_words'][document_number]))
        data_stemming['max_freq_wc'][document_number] = data_stemming['list_of_words'][document_number].count(
            statistics.mode(data_stemming['list_of_words'][document_number]))
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
    NUMBER_OF_DOCUMENTS = len(data["max_freq_wc"])
    # for each document in the data.
    for document_number, freq_wc in data["max_freq_wc"].items():
        print(f'Document #{document_number}')
        # creates tf_idf dictionary at document_number
        data["tf_idf"][document_number] = {}
        # for each word in the document.
        for word in data["list_of_words"][document_number]:
            if word == "":
                continue
            if word not in data["idf"].keys():
                data["idf"][word] = NUMBER_OF_DOCUMENTS / \
                    len(data["inverted_index"][word])
            data["tf_idf"][document_number][word] = (
                data["inverted_index"][word][document_number]/freq_wc*data["idf"][word])
    return data
