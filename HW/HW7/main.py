from scrape import scrape_data


def main():
    urls = scrape_data("http://www.muhlenberg.edu/")
    for url in urls:
        print(url)


if __name__ == "__main__":
    main()
