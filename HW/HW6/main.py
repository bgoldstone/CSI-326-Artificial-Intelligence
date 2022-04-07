import re

from parse_data import get_files


def main():
    """
    main Main runner function for Homework 6.
    """
    get_files('enron1', re.compile(r'[A-Za-z$]+[0-9]?'))


if __name__ == '__main__':
    main()
