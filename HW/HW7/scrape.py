import copy
import os
import re
import time
from typing import List, Union, Dict
from queue import LifoQueue

import requests

# contants
# regex for link and anchor tags. group 0 is link, group 1 is href.
LINK_REGEX = re.compile(
    r'<a[^>]*href=["\']([A-Za-z\d/_#-;?=@]*)["\']')
ROOT_URL_REGEX = re.compile(r"w*\.?[\w]+\.[.\w]+\/?")


def add_forward_slash(url: str) -> str:
    """
        add_forward_slash Adds a forward slash to url if not already present.

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
    domain = re.findall(r"https?:\/\/w*\.?([\w]+\.[.\w]+)\/?", first_url)[0]
    # gets full root url Ex. 'http://www.example.com/'
    root_url = f'http://{re.findall(ROOT_URL_REGEX, first_url)[0]}'
    root_url = add_forward_slash(root_url)
    print(root_url)
    # puts first url in stack to start.
    # gets robots.txt file
    robots = get_robots_txt(root_url)
    robots = robots if not None else None
    # time.sleep(2)
    stack.put(first_url)
    # scrape until 500 urls are scraped and more links to parse...
    while(len(visited) < 500 and not stack.empty()):
        stack_url = stack.get()
        # if url not visited and not a pdf, scrape the url.
        if stack_url not in visited and not stack_url.endswith('.pdf'):
            # gets the url scraping.
            current_url = get_url(stack_url, root_url)
            print(
                f'Visited:{len(visited) if current_url else "404 Not Found"} Stack: {stack.qsize()} URL: {stack_url}')
            # checks if urls was successfully visited.
            if current_url:
                # adds url to return list and visited stack.
                os.chdir(os.path.join(os.path.dirname(__file__), 'output'))
                with open(f'URL_{len(visited)}.txt', 'w', errors='ignore') as f:
                    # url, number of relative links, number of anchor links, html contents, list of links.
                    f.write(f'{current_url[0]}\n')
                    f.write(f'\n\nRelative Link Count: {current_url[1]}')
                    f.write(f'\n\nAbsolute Link Count: {current_url[2]}')
                    f.write(f'\n\nList of Links:\n\n{current_url[4]}')
                    f.write(f'\n\nContents:\n\n{current_url[3]}')
                return_value.append(current_url)
                visited.add(stack_url)
                # for all of the absolute links, add them to the stack.
                for url in current_url[4]:
                    # makes sure urls is not visited, the url is part of current domain, url is a absolute url, and is not disallowable by robots.txt.
                    if url not in visited and (domain in url and url.startswith("http")):
                        # if robots regex is found, check against that.
                        if robots:
                            if len(re.findall(robots, url)) == 0:
                                stack.put(url)
                        else:
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

    # if url fails to resolve, return False.
    try:
        # added headers because some websites require them.
        url = requests.get(base_url, headers={"User-Agent": "*"})
    except requests.exceptions.ConnectionError:
        print("site is not reachable", base_url)
        return False
    # url, number of relative links, number of anchor links, html contents, list of links.
    return_val = [base_url, 0, 0, url.text, []]
    # sets html contents index.
    return_val[3] = url.text
    # if url is successfully retrieved, get matches from regular expressions.
    for match in LINK_REGEX.findall(url.text):
        # if relative link.
        if match and match.startswith("/"):
            return_val[1] += 1
            try:
                index = current_match.index(match) == -1
                return_val[4].append(f'{root_url}{current_match[1:index]}')
            except ValueError:
                return_val[4].append(f'{root_url}{current_match[1:]}')
        # if absolute link.
        elif match and match.startswith("http"):
            current_match = str(match)
            # if id, ignore up to id.
            current_match = current_match[:current_match.find(
                "#")] if "#" in match else current_match
            return_val[2] += 1
            # add to list of links if not relative link, or blank, else return root_url + (blank or relative url)
            return_val[4].append(current_match)
    # returns return_val if successful request.
    return return_val if url.status_code == 200 else False


def get_robots_txt(domain: re.Pattern) -> Union[re.Pattern, None]:
    """
    get_robots_txt gets robots.txt from the domain.

    Args:
        domain (str): domain of website.

    Returns:
       Union[re.Pattern, None]: regex for disallowed links. None if user_agent does not exist.
    """
    # keeps list of not visitable links.
    not_visitable = []
    # finds user agent.
    find_by = 'user-agent: *'
    # request robots.txt
    request = requests.get(f'{domain}robots.txt')
    # all lines split by new line or carriage return.
    lines = [line.lower() for line in re.split(r'\n|\r', request.text)]
    # if no user agent is found, return None.
    try:
        index = lines.index(find_by)
    except ValueError:
        return None
    blank_lines = 0
    # for each line starting at 'User-Agent: *'
    for line in lines[index:]:
        if line == '':
            blank_lines += 1
            if blank_lines >= 2:
                # parsees into one string to compile in regex
                return_val = "|".join(not_visitable)
                return re.compile(return_val) if return_val else None

        else:
            blank_lines = 0
        # if not allowed to visit page, append to not_visitable list.
        if line.startswith('disallow'):
            not_visitable.append(line[line.index(':')+2:])
