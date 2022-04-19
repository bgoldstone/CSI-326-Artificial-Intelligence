import copy
import re
from typing import List, Union
from queue import LifoQueue

import requests

# contants
# regex for link and anchor tags. group 0 is rel, group 1 is absolute.
LINK_REGEX = re.compile(r'<link rel=.*href=\"(.+)\"|<a.*href="([^ ]*)"')


def add_forward_slash(url: str) -> str:
    """
        add_forward_slash Adds forward slash to url if not already present.

        Args:
            url (str): URL to check

        Returns:
            str: url with forward slash
        """
    return url if url[-1] == '/' else f'{url}/'


def scrape_data(first_url: str) -> List[List]:
    """
    scrape_data Scrapes the first 500 urls.

    Args:
        first_url (str): The url to start the web scrape from

    Returns:
        List[List]: list of each url in the following format: [url, # relative links(<link>), # anchor links(<a>), html contents, [**absolute links]].
    """
    # keeps track of visited urls.
    visited = set()
    # return value list.
    return_value = []
    # stack for DFS of urls.
    stack = LifoQueue()
    # first url to start the web scrape from.
    first_url = add_forward_slash(first_url)
    # gets domain and top level domain of url. Ex. 'example.com'
    domain = re.findall(r"https?:\/\/w*\.?([\w]+\.[\w]+)", first_url)[0]
    # gets full root url Ex. 'http://www.example.com/'
    root_url = f'http://www.{domain}/'
    # puts first url in stack to start.
    stack.put(first_url)
    # scrape until 500 urls are scraped.
    while(len(visited) <= 500):
        stack_url = stack.get()
        # if url not visited, scrape the url.
        if stack_url not in visited and not stack_url.endswith('.pdf'):
            print(
                f'Visited:{len(visited)} Stack: {stack.qsize()} URL: {stack_url}')
            # gets the url scraping.
            current_url = get_url(stack_url, root_url)
            # checks if urls was successfully visited.
            if current_url:
                # adds url to return list and visited stack.
                return_value.append(current_url)
                visited.add(stack_url)
                # for all of the absolute links, add them to the stack.
                for url in current_url[4]:
                    # makes sure urls is not visited, the url is part of current domain, and url is a absolute url.
                    if url not in visited and (domain in url and url.startswith("http")):
                        stack.put(url)
    return return_value


def get_url(base_url: str, root_url: str) -> Union[List, bool]:
    """
    get_url Scrapes teh url and returns a list of its findings.

    Args:
        base_url (str): URL to check.
        root_url (str): Root url of the domain.

    Returns:
        Union[List, bool]: URL findings in the format of [url, # relative links(<link>), # anchor links(<a>), html contents, [**absolute links]]. Returns False if url not successfully reachable.
    """

    # if url fails to resolve, return blank list.
    try:
        url = requests.get(base_url)
    except requests.exceptions.ConnectionError:
        print("site is not reachable", base_url)
        return False
    # sets html contents index.
    # url, number of relative links, number of anchor links, html contents, list of links.
    return_val = [base_url, 0, 0, url.text, []]
    return_val[3] = url.text
    # print(url.status_code, url.reason)
    # if url is successfully retrieved, get matches from regular expressions.
    for match in LINK_REGEX.findall(url.text):
        # if relative link.
        if match[0]:
            return_val[1] += 1
        # if absolute link.
        elif match[1]:
            current_match = str(match[1])
            # if id, ignore up to id.
            current_match = current_match[:current_match.find(
                "#")] if "#" in match[1] else current_match
            return_val[2] += 1
            # add to list of links if not relative link, or blank, else return root_url + (blank or relative url)
            return_val[4].append(current_match if not (current_match.startswith(
                '/') or current_match == "") else f'{root_url}{current_match[1:]}')
    # returns return_val if successful request.
    return return_val if url.status_code == 200 else False
