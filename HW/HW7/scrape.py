from queue import LifoQueue
import re


def scrape_data(url: str):
    url_pattern = re.compile(r"$https?://(www\.)?[a-zA-Z0-9./]")
    visited = set()
    stack = LifoQueue(501)
    first_url = url_pattern.findall(url)[0]
    if first_url:
        stack.put(first_url)
        while(len(visited) <= 500):
            # TODO create algorithm.
            pass
    else:
        print("This link is not valid! Please check your url and try again.")
