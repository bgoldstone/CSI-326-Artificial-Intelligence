from scrape import scrape_data
from inverted_index import create_inverted_index
from query import query
import os
import re
import cProfile
import gc


def main() -> None:
    """
    main Main function for Final Project.
    """
    web_scrape = os.path.join(os.path.abspath(__file__), "..", "output")
    print(web_scrape)
    data = os.path.join(os.path.abspath(__file__), "..", "data")
    gc.enable()
    # scrape_data("https://muhlenberg.edu/", 10_000, web_scrape)
    create_inverted_index(web_scrape, data)
    # query(data)


if __name__ == "__main__":
    # cProfile.run("main()")
    main()
