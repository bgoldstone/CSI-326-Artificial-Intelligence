import re
import time
from learn import get_words
from filter import filter_messages
from nltk.corpus import stopwords


def main():
    """
    main Main runner function for Homework 6.
    """
    regex = re.compile(
        r'([A-Za-z$!]+)|[$ ]?([0-9]+)')
    get_words('enron1', regex)
    start = time.time()
    # filter_messages('enron2', regex)
    print(f'{time.time() - start:.2f} seconds')


if __name__ == '__main__':
    main()
