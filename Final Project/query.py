import json
import math
import os
import statistics
from typing import List, Tuple


def query(data_path: str, postfix: str, query_terms: str) -> List[Tuple[str, str]]:
    """
    query gets results from urls given a query.

    Args:
        data_path (str): path to data json.
        postfix (str): string exression for improvements ex.('','_stopwords','_stemming','_stopwords_stemming')
        query_term (str): query string.

    Returns:
        List[Tuple[str, str]]: List from highest to lowest based on tf_idf with a tuples of (title, url).
    """
    os.chdir(data_path)
    # keys: inverted_index, list_of_words, idf, max_freq_wc, tf_idf
    data = {}
    # for each file in data_path, put it in a dictionary.
    for filename in os.listdir(data_path):
        # skips files that are not stemming,stopwords,etc specified by user.
        if (postfix == '' and (filename.find('stemming') != -1 or filename.find('stopwords') != -1)) or filename.find(postfix) == -1:
            continue
        # reads data.
        with open(os.path.join(data_path, filename)) as f:
            data[f'{filename[:filename.find(f"{postfix}.json")]}'] = json.load(
                f)
    numerator = {}
    denominator = {}
    results = {}
    tf_idf_query = {}
    # splits query into tokens
    query_terms = query_terms.split(' ')
    # gets unique tokens
    unique_query_term = set(query_terms)
    # finds most common word mex frequency
    query_max_freq = query_terms.count(
        statistics.mode(query_terms))
    # for each word in query terms, get tf_idf
    for word in unique_query_term:
        tf_idf_query[word] = data['idf'].get(
            word, 1)*(query_terms.count(word)/query_max_freq)
        # for each document in inverted_index that matches terms, get numerators
        for document_number in data['inverted_index'].get(word, {}).keys():
            # calculates numerator for each document.
            numerator[document_number] = numerator.get(
                document_number, 0) + (data['tf_idf'][document_number].get(word, 0)*tf_idf_query[word])
            # calculates denominator for each document.
            denominator[document_number] = denominator.get(document_number, 0) + (tf_idf_query[word] * data['tf_idf'][document_number].get(
                word, 0)**2)
    del(query_max_freq)
    results = {}
    # for all values, divide numerator by denominator and put in results.
    for key, value in numerator.items():
        results[key] = value/denominator[key]
    # sorts results
    results = sorted(
        results.items(), key=lambda item: item[1], reverse=True)
    # maps title to url.
    results_urls = [(data['title'][key[0]].replace("\n", ""), data['urls'][key[0]].replace("\n", ""))
                    for key in results]
    return results_urls
