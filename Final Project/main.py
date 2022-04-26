from scrape import scrape_data
import os
import re


def main() -> None:
    """
    main Main function for HW7.
    """
    urls = scrape_data("https://muhlenberg.edu/")
    # os.chdir(os.path.join(os.path.dirname(__file__), "output"))
    # for index, url in enumerate(urls):
    #     filename = f'URL{index}.txt'
    #     with open(filename, 'w') as f:
    #         f.write(f'URL: {url[0]}\n')
    #         f.write(f'Relative Links: {url[1]}\n')
    #         f.write(f'Absolute Links: {url[2]}\n')
    #         f.write(f'List of Absolute Links: {url[4]}\n')


if __name__ == "__main__":
    main()
