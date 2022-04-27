from scrape import scrape_data
from inverted_index import create_inverted_index
import os
import re
import cProfile


def main() -> None:
    """
    main Main function for HW7.
    """
    output = os.path.join(os.path.dirname(__file__), "output")
    data = os.path.join(os.path.dirname(__file__), "data")
    scrape_data("https://muhlenberg.edu/", 10_000, output)
    create_inverted_index(output, data)


if __name__ == "__main__":
    # cProfile.run("main()")
    main()
