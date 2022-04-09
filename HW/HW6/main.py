import re

from learn import get_words
from filter import filter_messages


def main():
    """
    main Main runner function for Homework 6.
    """
    get_words('enron1', re.compile(r'[A-Za-z$]+[0-9]?'), 'knowledge.json')
    filter_messages('enron1', re.compile(
        r'[A-Za-z$]+[0-9]?'), 'knowledge.json')


if __name__ == '__main__':
    main()
