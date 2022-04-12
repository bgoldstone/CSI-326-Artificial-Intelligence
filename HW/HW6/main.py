import re
import time
from learn import get_words
from filter import filter_messages


def main():
    """
    main Main runner function for Homework 6.
    """
    start = time.time()
    # group 1 is words group 2 is numbers
    regex = re.compile(
        r'([A-Za-z$!]+)|[$ ]?([0-9]+)')
    get_words('enron1', regex)
    # filter_messages('enron2', regex)
    print(f'{time.time() - start:.2f} seconds')


if __name__ == '__main__':
    main()
