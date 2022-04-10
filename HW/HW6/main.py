import re
import time

from learn import get_words
from filter import filter_messages


def main():
    """
    main Main runner function for Homework 6.
    """
    # get_words('enron1', re.compile(r'[A-Za-z$]+[0-9]?'), 'knowledge.json')
    start = time.time()
    filter_messages('enron2', re.compile(
        r'[A-Za-z$]+[0-9]?'), 'knowledge.json')
    print(f'{time.time() - start:.2f} seconds')


if __name__ == '__main__':
    main()
