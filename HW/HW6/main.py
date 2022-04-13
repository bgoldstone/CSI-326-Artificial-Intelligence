import re
import time
from typing import List

from filter import filter_messages
from learn import get_words


def get_results(regex: re.Pattern, directory_list: List[str]) -> None:
    """
    get_results Gets the results from the knowledge jsons and prints it into a readable format.

    Args:
        regex (re.Pattern): patter to sort by.
        file_list (List[str]): list of files to filter.
    """
    print()
    line = '_' * 50
    for directory in directory_list:
        print(f'{directory.title()} Results\n{line}\n')
        result1 = filter_messages(directory, regex, False, False)
        print(
            f'No Improvements:\n\tAccuracy: {result1.get("accuracy",0)*100:.2f}%\n\tPrecision: {result1.get("precision",0)*100:.2f}%\n\tRecall: {result1.get("recall",0)*100:.2f}%\n')
        result2 = filter_messages(directory, regex, True, False)
        print(
            f'Stopwords:\n\tAccuracy: {result2.get("accuracy",0)*100:.2f}%\n\tPrecision: {result2.get("precision",0)*100:.2f}%\n\tRecall: {result2.get("recall",0)*100:.2f}%\n')
        result3 = filter_messages(directory, regex, False, True)
        print(
            f'Lemmatization:\n\tAccuracy: {result3.get("accuracy",0)*100:.2f}%\n\tPrecision: {result3.get("precision",0)*100:.2f}%\n\tRecall: {result3.get("recall",0)*100:.2f}%\n')
        result4 = filter_messages(directory, regex, True, True)
        print(
            f'Lemmatization and Stopwords:\n\tAccuracy: {result4.get("accuracy",0)*100:.2f}%\n\tPrecision: {result4.get("precision",0)*100:.2f}%\n\tRecall: {result4.get("recall",0)*100:.2f}%\n')


def main():
    """
    main Main runner function for Homework 6.
    """
    start = time.time()
    # group 1 is words group 2 is numbers
    regex = re.compile(
        r'([A-Za-z$!]+)|[$ ]+([0-9]+)')
    # Gets the words from the folder and "learns" them.

    # get_words('enron1', regex)
    # gets results with filter_messages
    # get_results(regex, ['enron2', 'enron3'])
    print(f'Time taken: {time.time() - start:.2f} seconds')


if __name__ == '__main__':
    main()
