from scrape import scrape_data
from inverted_index import create_inverted_index
import os
import re
import cProfile
import gc


def main() -> None:
    """
    main Main function for HW7.
    """
    web_scrape = os.path.join(os.path.abspath(__file__), "..", "output")
    print(web_scrape)
    data = os.path.join(os.path.abspath(__file__), "..", "data")
    gc.enable()
    scrape_data("https://muhlenberg.edu/", 10_000, web_scrape)
    # create_inverted_index(output, data)


if __name__ == "__main__":
    # cProfile.run("main()")
    main()
