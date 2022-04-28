import os
import json
import statistics
import math


def query(data_path: str):
    os.chdir(data_path)
    # keys: inverted_index, list_of_words, idf, max_freq_wc, tf_idf
    data = {}
    # for each file in data_path, put it in a dictionary.
    for filename in os.listdir(data_path):
        with open(os.path.join(data_path, filename)) as f:
            data[f'{filename[:filename.find(".")]}'] = json.load(f)
    query_term = 'SEARCH'
    while query_term != '':
        numerator = {}
        denominator = {}
        results = {}
        tf_query = {}
        query_term = input(
            'Welcome to the Muhlenberg Search\nHit the enter key if you wish to exit this program\nEnter a query term: ')
        if query_term == '':
            continue
        query_term = query_term.split(' ')
        unique_query_term = set(query_term)
        query_max_freq = query_term.count(
            statistics.mode(query_term))
        for word in unique_query_term:
            tf_query[word] = data['idf'].get(
                word, 1)*(query_term.count(word)/query_max_freq)
        del(query_max_freq)
        for word in unique_query_term:
            for document_number, freq in data['inverted_index'].get(word, {}):
                numerator[document_number] = numerator.get(
                    document_number, 0) + (data['tf_idf'][document_number].get(word, 0)*tf_idf_query[word])
                denominator[document_number] = denominator.get(document_number, 0) + data['tf_idf'][document_number].get(
                    word, 0)**2
        for word, value in denominator.items():
            idf = data['idf'].get(word, 1)
            try:
                results[word] = numerator[word] / \
                    (math.sqrt(value)*math.sqrt(tf_query[word]*idf)**2)
            except ZeroDivisionError:
                results[word] = 0

        results = sorted(
            results.items(), key=lambda item: item[1], reverse=True)
        results_urls = {key: data['url'][key] for key in results.keys()}
        print(results_urls[:4])
