from operator import invert
import os
import json
import statistics


def create_inverted_index(input_path: str, output_path: str):
    inverted_index = {}
    max_frequencies = []
    if not os.path.isdir(output_path):
        os.makedirs(output_path)
    os.chdir(input_path)
    data_file = os.path.join(output_path, "data.json")
    # for each page.
    for index, filename in enumerate(os.listdir(input_path)):
        current_words: str
        with open(filename, 'r') as f:
            current_words = f.readlines()[1].split()
        # puts word into dictionary
        for word in current_words:
            # if dictionary key doesn't exist, create it.
            if not inverted_index.get(word, None):
                inverted_index[word] = {}
            # word count
            if not inverted_index[word].get(index, False):
                inverted_index[word][index] = current_words.count(
                    word)
        # gets mode to get the maximum frequency
        max_frequencies.append(current_words.count(
            statistics.mode(current_words)))
    # dumps json.
    with open(data_file, "w") as f:
        json.dump({"inverted_index": inverted_index,
                  "max_frequencies": max_frequencies}, f, sort_keys=True)
