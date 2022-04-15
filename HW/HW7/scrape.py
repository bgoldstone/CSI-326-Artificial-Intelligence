import re
import sys
from queue import LifoQueue

import requests


def scrape_data(first_url: str):
    visited = set()
    return_value = []
    stack = LifoQueue(501)
    first_url = first_url if first_url[-1] == '/' else f'{first_url}/'
    root_url = re.findall(r'\.([\w\d]+\.[\w\d]{3})', first_url)[0]
    stack.put(first_url)
    while(len(visited) <= 500):
        stack_url = stack.get()
        stack_url = stack_url if stack_url[-1] == '/' else f'{stack_url}/'
        print(f'{len(visited)} {stack_url}')
        if stack_url not in visited:
            current_url = get_url(stack_url)
            return_value.append(current_url[0:4])
            visited.add(stack_url)
            for url in current_url[4]:
                if url not in visited and root_url in url and (url.startswith("http") or url.startswith("/")):
                    stack.put(url)
    return return_value


def get_url(base_url: str):
    url = ''
    try:
        url = requests.get(base_url)
    except requests.exceptions.ConnectionError:
        print("site is not reachable", base_url)
        return [base_url, 0, 0, "", []]
    # 0 is rel, 1 is absolute
    link_regex = re.compile(r'<link rel=.*href=\"(.+)\"|<a.*href="([^ ]*)"')
    # url, number of relative links, number of absolute links, html contents, list of links
    return_val = [base_url, 0, 0, url.text, []]
    if url.status_code == 200:
        for match in link_regex.findall(url.text):
            if match[0]:
                return_val[1] += 1
            elif match[1]:
                current_match = str(match[1])
                if "#" in match[1]:
                    current_match = current_match[:current_match.find("#")]

                return_val[2] += 1
                if current_match.find("#") == 0:
                    continue
                return_val[4].append(current_match if not (current_match.startswith(
                    '/') or current_match == "") else f'{base_url}{current_match[1:]}')
    return return_val
